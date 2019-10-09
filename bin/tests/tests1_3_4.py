#!/usr/bin/python

import unittest
import importlib
import json
import shutil
import os

veris = "/Users/v685573/Documents/Development/vzrisk/veris/"
cfg = {
    "log_level": "debug",
    "log_file": "./unittest.log",
    'provide_context': True,
    'input': "./",
    'output': "./",
    'force_analyst': False,
    'check': False,
    'update': True,
    'analyst': "unittest",
    'veris': veris,
    'version': "1.3.4",
    'countryfile': veris.rstrip("/") + "/bin/all.json",
#    'report': report,
#    'year': year,
    'test': 'BLUE'
}

# import rules.py
spec = importlib.util.spec_from_file_location("rules", veris.rstrip("/") + "/bin/rules.py")
rules = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rules)
Rules = rules.Rules(cfg)

# import convert_1.3.3_to_1.3.4.py
spec = importlib.util.spec_from_file_location("convert", veris.rstrip("/") + "/bin/convert_1.3.3_to_1.3.4.py")
convert = importlib.util.module_from_spec(spec)
spec.loader.exec_module(convert)

with open(veris.rstrip("/") + "/bin/tests/veris-1_3_4-test1.json", 'r') as filehandle:
    incident0 = json.load(filehandle)

#convert_filename = cfg['input'][1] + ".out"
#shutil.copyfile(cfg['input'][1], convert_filename)
convert.main(dict(cfg, **{'input': veris.rstrip("/") + "/bin/tests/test_json_2/", 'output':veris.rstrip("/") + "/bin/tests/"}))
with open(veris.rstrip("/") + "/bin/tests/veris-1_3_4-test2.json", 'r') as filehandle:
    incident1 = json.load(filehandle)
os.remove(veris.rstrip("/") + "/bin/tests/veris-1_3_4-test2.json")


class TestRules(unittest.TestCase):

    # vz-risk/veirs issue # 212
    def test213_1(self):
        incident_in = incident0
        incident_in['action']['hacking'] = {'variety': ['Insecure deserialization'], 'vector': ['Unknown']}
        incident_out = Rules.addRules(incident_in)
        self.assertIn('Exploit vuln', incident_out['action']['hacking']['variety'])

    # vz-risk/veirs issue # 212
    def test225_1(self):
        incident_in = incident0
        incident_in['action']['hacking'] = {'variety': ['User breakout'], 'vector': ['Unknown']}
        incident_out = Rules.addRules(incident_in)
        self.assertIn('Exploit vuln', incident_out['action']['hacking']['variety'])
    
    # vz-risk/veris issue # 263
    def  test263_1(self):
        incident_in = incident0
        incident_in['asset']['assets'].append({'variety': "U - Laptop"})
        incident_out = Rules.addRules(incident_in)
        self.assertIn('U - Desktop or laptop', [item.get("variety", "") for item in incident_out['asset']['assets']])
    def  test263_2(self):
        incident_in = incident0
        incident_in['asset']['assets'].append({'variety': "U - Desktop"})
        incident_out = Rules.addRules(incident_in)
        self.assertIn('U - Desktop or laptop', [item.get("variety", "") for item in incident_out['asset']['assets']])

    # vz-risk/veris issue # 232
    def test232_1(self):
        incident_in = incident0
        incident_in['action']['malware'] = {'variety': ['Email attachment'], 'vector': ['Unknown']}
        incident_out = Rules.addRules(incident_in)
        self.assertIn('Email', incident_out['action']['malware']['variety'])
    def test232_2(self):
        incident_in = incident0
        incident_in['action']['malware'] = {'variety': ['Email link'], 'vector': ['Unknown']}
        incident_out = Rules.addRules(incident_in)
        self.assertIn('Email', incident_out['action']['malware']['variety'])
    def test232_3(self):
        incident_in = incident0
        incident_in['action']['malware'] = {'variety': ['Email other'], 'vector': ['Unknown']}
        incident_out = Rules.addRules(incident_in)
        self.assertIn('Email', incident_out['action']['malware']['variety'])
    def test232_4(self):
        incident_in = incident0
        incident_in['action']['malware'] = {'variety': ['Email unknown'], 'vector': ['Unknown']}
        incident_out = Rules.addRules(incident_in)
        self.assertIn('Email', incident_out['action']['malware']['variety'])

    # vz-risk/veris issue #215
    def test215_1(self):
        incident_in = incident0
        incident_in['action']['malware'] = {'variety': ['Trojan', 'Backdoor'], 'vector': ['Unknown']}
        incident_out = Rules.addRules(incident_in)
        self.assertIn('RAT', incident_out['action']['malware']['variety'])
    def test215_2(self):
        incident_in = incident0
        incident_in['action']['malware'] = {'variety': ['RAT'], 'vector': ['Unknown']}
        incident_out = Rules.addRules(incident_in)
        self.assertIn('Trojan', incident_out['action']['malware']['variety'])
        self.assertIn('Backdoor', incident_out['action']['malware']['variety'])

    # vz-risk/veris issue #150
    def test150_1(self):
        incident_in = incident0
        incident_in['action']['social'] = {'target': ['End-user'], 'variety': ['Unknown'], 'vector': ['Unknown']}
        incident_out = Rules.addRules(incident_in)
        self.assertIn('End-user or employee', incident_out['action']['social']['target'])
    def test150_2(self):
        incident_in = incident0
        incident_in['action']['social'] = {'target': ['Other employee'], 'variety': ['Unknown'], 'vector': ['Unknown']}
        incident_out = Rules.addRules(incident_in)
        self.assertIn('End-user or employee', incident_out['action']['social']['target'])


class Testconvert(unittest.TestCase):
    # vz-risk/veris issue #263
    def test263_1(self):
        self.assertIn('U - Desktop or laptop', [item.get("variety", "") for item in incident1['asset']['assets']])

    # vz-risk/veris issue #232
    def test232_1(self):
        self.assertIn('Email', incident1['action']['malware']['variety'])

    # vz-risk/veris issue #260
    def test360_1(self):
        self.assertEqual('Yes', incident1['plus']['attribute']['confidentiality']['credit_monitoring'])
    def test360_2(self):
        self.assertEqual(1.5, incident1['plus']['attribute']['confidentiality']['credit_monitoring_years'])

    # vz-risk/veris issue #259
    def test259_1(self):
        self.assertEqual('Other', incident1['plus']['attribute']['confidentiality']['partner_data'])
    def test259_2(self):
        self.assertNotIn("partner_number", incident1['plus']['attribute']['confidentiality'])

    # vz-risk/veris issue #225
    def test259_2(self):
        self.assertIn("Unknown", incident1['asset']['cloud'])

    # vz-risk/veris issue #150
    def test259_2(self):
        self.assertIn("End-user or employee", incident1['action']['social']['target'])

if __name__ == '__main__':
    unittest.main()