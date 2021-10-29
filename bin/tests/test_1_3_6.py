#!/usr/bin/python

# https://www.mattcrampton.com/blog/a_list_of_all_python_assert_methods/

import unittest
from importlib import util
import json
import shutil
import os
from jsonschema import ValidationError, Draft4Validator
import re
import logging
import tempfile
from copy import deepcopy
import uuid

veris = "/Users/v685573/Documents/Development/vzrisk/veris/"
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
    'version': "1.3.6",
    'countryfile': veris.rstrip("/") + "/bin/all.json",
#    'report': report,
#    'year': year,
    'test': 'BLUE'
}

# import rules.py
spec = util.spec_from_file_location("rules", veris.rstrip("/") + "/bin/rules.py")
rules = util.module_from_spec(spec)
spec.loader.exec_module(rules)
Rules = rules.Rules(cfg)

# import convert_1.3.5_to_1.3.6.py
spec = util.spec_from_file_location("convert", veris.rstrip("/") + "/bin/convert_1.3.5_to_1.3.6.py")
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
filename = "/Users/v685573/Documents/Development/vzrisk/veris/bin/tests/veris-1_3_6-test1.json"
with open(filename, 'r') as filehandle:
  base_incident = json.load(filehandle)


class TestRules(unittest.TestCase):

#    # vz-risk/veris issue # 263
#    def  test263_1(self):
#        incident_in = incident0
#        incident_in['asset']['assets'].append({'variety': "U - Laptop"})
#        incident_out = Rules.addRules(incident_in)
#        self.assertIn('U - Desktop or laptop', [item.get("variety", "") for item in incident_out['asset']['assets']])
#    def  test263_2(self):
#        incident_in = incident0
#        incident_in['asset']['assets'].append({'variety': "U - Desktop"})
#        incident_out = Rules.addRules(incident_in)
#        self.assertIn('U - Desktop or laptop', [item.get("variety", "") for item in incident_out['asset']['assets']])

    def test271_1(self):
        in_incident = deepcopy(base_incident)
        in_incident["schema_version"] = "1.3.5"
        in_incident["action"] = {"malware": {"variety": ["DoS"]}}
        in_incident["actor"] = {"internal": {"variety": ["Unknown"]}}
        out_incident = apply_convert(in_incident, convert)
        motives = list(set(
            out_incident['actor'].get('external', {}).get('motive', []) +
            out_incident['actor'].get('internal', {}).get('motive', []) +
            out_incident['actor'].get('partner', {}).get('motive', [])
        ))
        #pprint(out_incident)
        self.assertIn('Secondary', motives)

    def test383_1(self):
        in_incident = deepcopy(base_incident)
        in_incident["schema_version"] = "1.3.5"
        in_incident["action"] = {"malware": {"variety": ["C2"]}}
        out_incident = apply_convert(in_incident, convert)
        self.assertIn('Backdoor or C2', out_incident['action']['malware']['variety'])
    def test383_2(self):
        in_incident = deepcopy(base_incident)
        in_incident["schema_version"] = "1.3.5"
        in_incident["action"] = {"malware": {"variety": ["Backdoor"]}}
        out_incident = apply_convert(in_incident, convert)
        self.assertIn('Backdoor or C2', out_incident['action']['malware']['variety'])
    def test383_3(self):
        in_incident = deepcopy(base_incident)
        in_incident["schema_version"] = "1.3.5"
        in_incident["action"] = {"hacking": {"variety": ['Use of backdoor or C2' ], "vector": ["Unknown"]}}
        out_incident = apply_convert(in_incident, convert)
        self.assertNotIn('Use of backdoor or C2' , out_incident['action']['hacking']['variety'])
    def test383_4(self):
        in_incident = deepcopy(base_incident)
        in_incident["schema_version"] = "1.3.5"
        in_incident["action"] = {"hacking": {"variety": ['Use of backdoor or C2' ], "vector": ["Unknown"]}}
        out_incident = apply_convert(in_incident, convert)
        self.assertIn('Backdoor', out_incident['action']['hacking']['vector'])



class TestConvert(unittest.TestCase):
#    # vz-risk/veris issue #263
#    def test263_1(self):
#        self.assertIn('U - Desktop or laptop', [item.get("variety", "") for item in incident1['asset']['assets']])
    pass





if __name__ == '__main__':
    ## Test Validations
    logging.info("Review the following errors to ensure there are none unexpected. (In the future maybe we can catch all these with unit tests.")
#    for error in validator.iter_errors(incident2):
#        logging.warning(error.message)
#    for error in checkValidity.main(incident2):
#        logging.warning(error.message)
#    for error in validator.iter_errors(incident3):
#        logging.warning(error.message)
#    for error in checkValidity.main(incident3):
#        logging.warning(error.message)

    # Test Cases
    logging.info("Beginning test cases")
    unittest.main()