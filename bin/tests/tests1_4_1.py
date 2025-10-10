#!/usr/bin/python

# https://www.mattcrampton.com/blog/a_list_of_all_python_assert_methods/

import unittest
from importlib import util
import json
import shutil
import os, pathlib
from jsonschema import ValidationError, Draft4Validator
import re
import logging
import tempfile
from copy import deepcopy
import uuid
from pprint import pprint

##TODO: Update this reference PL priority
#Actually fix this or just jank patch it?
#veris = os.path.expanduser("~/Documents/Development/vzrisk/veris/")
veris = str(pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve())
cfg = {
    "log_level": "error",
    "log_file": "./unittest.log",
    'provide_context': True,
    'input': "./",
    'output': "./",
    'force_analyst': False,
    'check': False,
    'update': True,
    'analyst': "unittest",
    'veris': veris,
    'version': "1.4.1",
    'countryfile': veris.rstrip("/") + "/bin/all.json",
#    'report': report,
#    'year': year,
    'test': 'BLUE',
    'vcdb': False,
    'year': 2026
}

# import rules.py
spec = util.spec_from_file_location("rules", veris.rstrip("/") + "/bin/rules.py")
rules = util.module_from_spec(spec)
spec.loader.exec_module(rules)
Rules = rules.Rules(cfg)

# import convert_1.3.7_to_1.4.0.py
spec = util.spec_from_file_location("convert", veris.rstrip("/") + "/bin/convert_1.4.0_to_1.4.1.py")
convert = util.module_from_spec(spec)
spec.loader.exec_module(convert)

# import checkValidity
spec = util.spec_from_file_location("checkValidity", cfg.get("veris", "../").rstrip("/") + "/bin/checkValidity.py")
checkValidity = util.module_from_spec(spec)
spec.loader.exec_module(checkValidity)

# create validator
with open(veris.rstrip("/") + "/verisc-merged.json") as filehandle:
    validator = Draft4Validator(json.load(filehandle))


# Used to apply convert script to json
def apply_convert(in_incident, updater, cfg=cfg):
  with tempfile.TemporaryDirectory() as tmpdirname:
    filename = os.path.join(tmpdirname, str(uuid.uuid4()).upper() + ".json")
    with open(filename, 'w') as filehandle:
        json.dump(in_incident, filehandle)
    updater.main(dict(cfg, **{'input': tmpdirname, 'output':tmpdirname}))
    with open(filename, 'r') as filehandle:
        return(json.load(filehandle))

# Import a base 1.3.6 incident
filename = str(pathlib.Path(__file__).parent.resolve())+"/veris-{}-test1.JSON".format(cfg['version'].replace(".","_"))
with open(filename, 'r') as filehandle:
  base_incident = json.load(filehandle)


class TestConvert(unittest.TestCase):
    def test496_1(self):
        in_incident = deepcopy(base_incident)
        in_incident["schema_version"] = "1.4.0"
        #we skip adding the fields, since the test file has the fields required

        in_incident['plus']["attribute"] ={"confidentiality":{"partner_number":10, "partner_data":"Yes"}}
        out_incident = apply_convert(in_incident, convert)

        #verify that we dropped these fields
        self.assertNotIn("partner_data", out_incident["plus"].get("attribute",{}).get("confidentiality",{}))
        self.assertNotIn("partner_number", out_incident["plus"].get("attribute",{}).get("confidentiality",{}))

        # we also should have trimmed out the confidentiality branch in plus
        #self.assertNotIn("confidentiality", out_incident['plus'].get('attribute',{}))

        # Verify that we properly added the partner to data victim
        self.assertIn("Partner", out_incident["attribute"]["confidentiality"]['data_victim'])

        #now we need to assure that we've properly added the values to data total

        partner_number = in_incident.get("plus",{}).get("attribute",{}).get("confidentiality",{}).get("partner_number","")
        data_total = in_incident.get("attribute",{}).get("confidentiality",{}).get("data_total","")

        if partner_number != data_total:
            data_total_out = out_incident["attribute"]['confidentiality']['data_total']
            data_tota_in_add = partner_number +data_total
            self.assertEqual(data_total_out,data_tota_in_add)
        else:
            data_total_out = out_incident["attribute"]['confidentiality']['data_total']
            self.assertEqual(data_total_out,data_total)

        for error in validator.iter_errors(out_incident):
            raise error

    #493 Change "S - Remote Access" to an "N - Remote access" asset
    def test493_1(self):
        # This test is focused on just verifying the replacement of S - Remote acccess + the Addition of Network
        in_incident = deepcopy(base_incident)
        in_incident["schema_version"] = "1.4.0"
        # we skip adding the fields, since the test file has the fields required
        in_incident['asset']['assets'].append({"variety": "S - Remote access"})
        out_incident = apply_convert(in_incident, convert)


        #Verify N - Remote Access is there
        self.assertIn("N - Remote access", [item.get("variety", "") for item in out_incident['asset']['assets']])
        #self.assertIn("Network", out_incident["asset"]["variety"])
        self.assertNotIn("S - Remote access", [item.get("variety", "") for item in out_incident['asset']['assets']])

        # We need to make sure that if there's no other Servers in asset

        for error in validator.iter_errors(out_incident):
            raise error

    # def test493_2(self):
    #     # Test network is adde d
    #     in_incident = deepcopy(base_incident)
    #     in_incident["schema_version"] = "1.4.0"
    #
    #     # Ok we add AN EXTRA Server to ASSURE that server is value is kept
    #
    #     in_incident['asset']['assets'].append({'variety': "S - Web app"})
    #     in_incident['asset']['variety'] = "Server"
    #     out_incident = apply_convert(in_incident, convert)
    #
    #     self.assertIn("Server", out_incident['asset']['variety'])
    #     # Assert that we've added network
    #     self.assertIn("Network", out_incident['asset']['variety'])
    #
    #     for error in validator.iter_errors(out_incident):
    #         raise error
    #
    # def test493_3(self):
    #     # last test for this one, assure that if we ONLY have the one server, that server variety gets removed
    #     in_incident = deepcopy(base_incident)
    #     in_incident["schema_version"] = "1.4.0"
    #
    #     # ok we want to make sure if we ONLY have S - Remote access that server
    #     in_incident['asset']['assets'].clear()
    #     in_incident['asset']['assets'].append({"variety":"S - Remote Access"})
    #     #
    # 486 Create a new Server asset variety for a Secrets Vault and convert N - HSM to S - Secrets Vault
    def test486(self):
        in_incident = deepcopy(base_incident)

        in_incident["schema_version"] = "1.4.0"

        in_incident['asset']['assets'].append({"variety":"N - HSM"})
        out_incident = apply_convert(in_incident, convert)

        self.assertIn("S - Secrets vault", [item.get("variety", "") for item in out_incident['asset']['assets']])

        self.assertNotIn("N - HSM",[item.get("variety", "") for item in out_incident['asset']['assets']] )

        for error in validator.iter_errors(out_incident):
            raise error

class TestRules(unittest.TestCase):
#    # vz-risk/veris issue #263
#    def test263_1(self):
#        self.assertIn('U - Desktop or laptop', [item.get("variety", "") for item in incident1['asset']['assets']])

    def test_rules_271_1(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"malware": {"variety": ["DoS"], "vector":["Unknown"]}}
        in_incident["actor"] = {"internal": {"variety": ["Unknown"]}}
        out_incident = Rules.addRules(in_incident)
        motives = list(set(
            out_incident['actor'].get('external', {}).get('motive', []) +
            out_incident['actor'].get('internal', {}).get('motive', []) +
            out_incident['actor'].get('partner', {}).get('motive', [])
        ))
        #pprint(out_incident)
        self.assertIn('Secondary', motives)
        for error in validator.iter_errors(out_incident):
            raise error

    # vz-risk/veris/issues/492 create hierarchy between register MFA device + create account to "Modiy Authentication"
    def test_rules_492_1(self):
        in_incident = deepcopy(base_incident)
        in_incident['attribute']={'integrity':{'variety':["Register MFA device"]}}

        out_incident = Rules.addRules(in_incident)

        self.assertIn("Modify authentication", out_incident.get("attribute",{}).get("integrity",{}).get("variety",[]))

        for error in validator.iter_errors(out_incident):
            raise error

    def test_rules_492_2(self):
        in_incident = deepcopy(base_incident)
        in_incident['attribute']={'integrity':{'variety':["Created account"]}}

        out_incident = Rules.addRules(in_incident)

        self.assertIn("Modify authentication", out_incident.get("attribute",{}).get("integrity",{}).get("variety",[]))

        for error in validator.iter_errors(out_incident):
            raise error

    def test_rules_500_1(self):
        personal_data_types = ["Medical", "Sensitive Personal", "Bank", "Payment"]
        for p_type in personal_data_types:
            in_incident = deepcopy(base_incident)
            in_incident['attribute']['confidentiality']['data'].append({"variety": p_type})

            out_incident = Rules.addRules(in_incident)
            self.assertIn("Personal", [data.get("variety") for data in
                                          out_incident.get("attribute", {}).get("confidentiality", {}).get("data", [])])
            for error in validator.iter_errors(out_incident):
                raise error

    def test_rules_495(self):
        types_of_Yes= ["Yes - Data ransomed","Yes - Identity theft","Yes - Financial fraud","Yes - Posted on personal forum"]
        for p_type in types_of_Yes:
            in_incident = deepcopy(base_incident)
            in_incident['plus']['attribute'] ={'confidentiality':{'data_abuse': p_type}}

            out_incident = Rules.addRules(in_incident)
            self.assertIn("Yes", out_incident['plus']['attribute']['confidentiality']['data_abuse'])
            for error in validator.iter_errors(out_incident):
                raise error



    # Hierarhcy between the credential types (probably excessive to do it for each one rather than iterate it through
    # vz-risk/veris/501
    def test_rules_501_1(self):
        in_incident = deepcopy(base_incident)
        in_incident['attribute']['confidentiality']['data'].append({"variety":"API key"})

        out_incident = Rules.addRules(in_incident)

        self.assertIn("Credentials", [data.get("variety") for data in out_incident.get("attribute",{}).get("confidentiality",{}).get("data",[])])

        for error in validator.iter_errors(out_incident):
            raise error

    def test_rules_501_2(self):
        in_incident = deepcopy(base_incident)
        in_incident['attribute']['confidentiality']['data'].append({"variety":"Digital certificate"})

        out_incident = Rules.addRules(in_incident)

        self.assertIn("Credentials", [data.get("variety") for data in out_incident.get("attribute",{}).get("confidentiality",{}).get("data",[])])

        for error in validator.iter_errors(out_incident):
            raise error
    def test_rules_501_3(self):
        in_incident = deepcopy(base_incident)
        in_incident['attribute']['confidentiality']['data'].append({"variety":"Multi-factor credential"})

        out_incident = Rules.addRules(in_incident)

        self.assertIn("Credentials", [data.get("variety") for data in out_incident.get("attribute",{}).get("confidentiality",{}).get("data",[])])

        for error in validator.iter_errors(out_incident):
            raise error
    def test_rules_501_4(self):
        in_incident = deepcopy(base_incident)
        in_incident['attribute']['confidentiality']['data'].append({"variety":"Session key"})

        out_incident = Rules.addRules(in_incident)

        self.assertIn("Credentials", [data.get("variety") for data in out_incident.get("attribute",{}).get("confidentiality",{}).get("data",[])])

        for error in validator.iter_errors(out_incident):
            raise error

class TestValidation(unittest.TestCase):
    def test_validation_180_1(self):
        regions = {
            "002": ["011", "014", "017", "018", "015"], # Africa
            "010": ["000"], # Antarctica
            "019": ["021", "005", "013", "029", "419"], # America
            "419": ["005", "013", "029"], # Latin America and Caribbean
            "142": ["030", "034", "035", "143", "145"], # Asia
            "150": ["039", "151", "154", "830", "155"], # Europe
            "009": ["053", "054", "057", "061"] # Oceania
        }
        good_regions = []
        for region in regions.keys():
            good_regions += [region + v for v in regions[region]]
        in_incident = deepcopy(base_incident)
        in_incident["victim"]['region'] = good_regions # legitimate regions
        for error in checkValidity.main(in_incident):
            raise error
    def test_validation_180_2(self):
        in_incident = deepcopy(base_incident)
        in_incident["victim"]['region'] = ["001000", "020001", "003021"] # unused super-regions
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_180_3(self):
        in_incident = deepcopy(base_incident)
        in_incident["victim"]['region'] = ["019011"] # incorrect pairing
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error

    def test_validation_407_1(self):
        in_incident = deepcopy(base_incident)
        in_incident["victim"]['secondary'] = {"victim_id": ['victim2', 'victim3', 'victim4'], "amount": 3}  # no error
        for error in checkValidity.main(in_incident):
            raise error
    def test_validation_407_2(self):
        in_incident = deepcopy(base_incident)
        in_incident["victim"]['secondary'] = {"victim_id": ['victim2', 'victim3', 'victim4'], "amount": 0}  # error
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_407_3(self):
        in_incident = deepcopy(base_incident)
        in_incident["victim"]['secondary'] = {"victim_id": ['victim2', 'victim3', 'victim4']}  # error
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error

    # Validation
    def test_validation_400_1(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"social": {"variety": ['Phishing'], "vector": ["Unknown"], "target": ["Unknown"]}}
        in_incident["value_chain"] = {"targeting": {"variety": "Email addresses"}}
        in_incident["attribute"] = {"integrity": {"variety": "Alter behavior"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_2(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"social": {"variety": ['Phishing'], "vector": ["Unknown"], "target": ["Unknown"]}}
        in_incident["value_chain"] = {"development": {"variety": "Email"}}
        in_incident["attribute"] = {"integrity": {"variety": "Alter behavior"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_3(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"malware": {"variety": ['Unknown'], "vector": ["C2"]}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_4(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"malware": {"variety": ['Ransomware'], "vector": ["Unknown"]}}
        in_incident["value_chain"] = {"development": {"variety": "Ransomware"}}
        in_incident["attribute"] = {"integrity": {"variety": "Software installation"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_5(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"malware": {"variety": ['Ransomware'], "vector": ["Unknown"]}}
        in_incident["value_chain"] = {"cash-out": {"variety": "Cryptocurrency"}}
        in_incident["attribute"] = {"integrity": {"variety": "Software installation"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_6(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"malware": {"variety": ['Trojan'], "vector": ["Unknown"]}}
        in_incident["attribute"] = {"integrity": {"variety": "Software installation"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_7(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"social": {"variety": ['Unknown'], "vector": ["Email"]}}
        in_incident["value_chain"] = {"distribution": {"variety": "Email"}}
        in_incident["attribute"] = {"integrity": {"variety": "Alter behavior"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_8(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"social": {"variety": ['Unknown'], "vector": ["Email"]}}
        in_incident["value_chain"] = {"targeting": {"variety": "Email addresses"}}
        in_incident["attribute"] = {"integrity": {"variety": "Alter behavior"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    # Recommend only
    def test_validation_400_9(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"malware": {"variety": ['Unknown'], "vector": ["Unknown"]}}
        in_incident["attribute"] = {"integrity": {"variety": "Software installation"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_10(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"malware": {"variety": ['Trojan'], "vector": ["Unknown"]}}
        in_incident["value_chain"] = {"development": {"variety": ["Unknown"]}}
        in_incident["attribute"] = {"integrity": {"variety": "Software installation"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_11(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"social": {"variety": ['Pretexting'], "vector": ["Unknown"]}}
        in_incident["value_chain"] = {"targeting": {"variety": "Email addresses"}}
        in_incident["attribute"] = {"integrity": {"variety": "Alter behavior"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_12(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"hacking": {"variety": ['Use of stolen creds'], "vector": ["Unknown"]}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_13(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"hacking": {"variety": ['Exploit vuln'], "vector": ["Unknown"]}}
        in_incident["value_chain"] = {"targeting": {"variety": "Vulnerabilities"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_14(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"hacking": {"variety": ['Exploit vuln'], "vector": ["Unknown"]}}
        in_incident["value_chain"] = {"development": {"variety": "Exploit"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_15(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"malware": {"variety": ['Downloader'], "vector": ["Unknown"]}}
        in_incident["value_chain"] = {"development": {"variety": ["Unknown"]}}
        in_incident["attribute"] = {"integrity": {"variety": "Software installation"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_16(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"hacking": {"variety": ['Exploit misconfig'], "vector": ["Unknown"]}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_17(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"malware": {"variety": ['Exploit misconfig'], "vector": ["Unknown"]}}
        in_incident["value_chain"] = {"development": {"variety": ["Unknown"]}}
        in_incident["attribute"] = {"integrity": {"variety": "Software installation"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_18(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"malware": {"variety": ['Unknown'], "vector": ["Web application"]}}
        in_incident["value_chain"] = {"development": {"variety": ["Unknown"]}}
        in_incident["attribute"] = {"integrity": {"variety": "Software installation"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error
    def test_validation_400_19(self):
        in_incident = deepcopy(base_incident)
        in_incident["action"] = {"social": {"variety": ['Unknown'], "vector": ["Web application"]}}
        in_incident["attribute"] = {"integrity": {"variety": "Alter behavior"}}
        with self.assertRaises(ValidationError):
            for error in checkValidity.main(in_incident):
                raise error

    def test_validation_429_1(self):
        in_incident = deepcopy(base_incident)

# if True: #





if __name__ == '__main__':
    ## Test Validations
    logging.info("Review the following errors to ensure there are none unexpected. (In the future maybe we can catch all these with unit tests.")

    # Test Cases
    logging.info("Beginning test cases")
    unittest.main()