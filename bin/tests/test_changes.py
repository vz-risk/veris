#!/usr/bin/env python
"""
 AUTHOR: Gabriel Bassett
 DATE: 121104
 DEPENDENCIES: <a list of modules requiring installation>

 DESCRIPTION:
 A script to apply updates to veris json files and show the chances made per file.

 NOTES:
 <No Notes>

 ISSUES:
 <No Issues>

 TODO:
 <No TODO>

"""
# PRE-USER SETUP
import logging
import os
#import imp
from importlib import util
import pprint
import uuid
import tempfile
import jq
from jsonschema import ValidationError, Draft4Validator
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    spec = util.spec_from_file_location("veris_logger", script_dir + "/../veris_logger.py")
    veris_logger = util.module_from_spec(spec)
    spec.loader.exec_module(veris_logger)
    #veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise


########### NOT USER EDITABLE ABOVE THIS POINT #################


# USER VARIABLES
LOGLEVEL = "warning"
LOG = None

MAX_EXAMPLES = 20
# MAX_EXAMPLES = 30000

########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import json
import glob
import random
from jsondiff import diff
from packaging import version


## SETUP
__author__ = "Gabriel Bassett"

# Parse Arguments (should correspond to user variables)
parser = argparse.ArgumentParser(description='This script generates the VERIS_Standard_Excel.xlsx file from the veris schema.')
parser.add_argument('-d', '--debug',
                    help='Print lots of debugging statements',
                    action="store_const", dest="loglevel", const=logging.DEBUG,
                    default=LOGLEVEL
                   )
parser.add_argument('-v', '--verbose',
                    help='Be verbose',
                    action="store_const", dest="loglevel", const=logging.INFO
                   )
parser.add_argument('--log', help='Location of log file', default=LOG)
parser.add_argument("-c", "--convert", help="The script to convert the json from one veris version to another.")
parser.add_argument('-t', '--test_examples', help=  'A directory of veris json files to convert to examples. ' +
                                                    '(VCDB is a good option for this, but note the VCDB schema is not the same as verisc.) ' +
                                                    'If more than num_examples (currently {0}), {0} will be randomly chosen.'.format(MAX_EXAMPLES), type=str, default=None)
parser.add_argument('-n', '--num_examples', help='The number of examples to include.  Defaults to {0}. 0 indicates all.'.format(MAX_EXAMPLES), type=int, default=MAX_EXAMPLES)
args = parser.parse_args()
args = {k:v for k,v in vars(args).items() if v is not None}

filename=None
level=None
## Set up Logging
if args.get('log', None) is not None:
    filename=args['log']
    level=args['loglevel']
else:
    level=args['loglevel']


veris = os.path.expanduser("~/Documents/Development/vzrisk/veris/")
cfg = {
    'log_level': level,
    'log_file': filename,
    'version': '1.3.6',
    'convert': 'convert_1.3.5_to_1.3.6.py',
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
    'test': 'BLUE',
    'vcdb': False,
    'year': 2022
}
cfg.update(args)
#logging.info(cfg)

## GLOBAL EXECUTION

## FUNCTION DEFINITION
# import rules.py
spec = util.spec_from_file_location("rules", veris.rstrip("/") + "/bin/rules.py")
rules = util.module_from_spec(spec)
spec.loader.exec_module(rules)
Rules = rules.Rules(cfg)

# import convert_1.3.5_to_1.3.6.py
spec = util.spec_from_file_location("convert", veris.rstrip("/") + "/bin/" + cfg['convert'])
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


def diff_lists(in_incident, out_incident, diff_json):
    query2 = '''[
        . as $in |
        (paths(scalars), paths((. )?)) |
        join(".") as $key |
        $key + "=" + ($in | getpath($key | split(".") | map((. | tonumber)? // .)) | tostring)
    ] | sort | .[]'''

    d_diff = {}
    jq_compiled = jq.compile(query2)
    d_in = {}
    for s in jq_compiled.input(in_incident):
        l = s.split("=")
        if len(l[1]) > 0 and l[1][0] == "[":
          l[1] = json.loads(l[1])
          d_in[l[0]] =  l[1]
    d_out = {}
    for s in jq_compiled.input(out_incident):
        l = s.split("=")
        if len(l[1]) > 0 and l[1][0] == "[":
          l[1] = json.loads(l[1])
          d_out[l[0]] =  l[1]
    for key in set(d_out.keys()).union(d_in.keys()):
        if key == "asset.assets":
            if "assets" in diff_json.get("asset", {}): # I'm just not dealing with this here.
                print("key asset.assets was listed as a diff, but lists of objects are hard so you'll need to check.")
        elif key == "attribute.confidentiality.data":
            if "data" in diff_json.get("attribute", {}).get("confidentiality", {}):
                print("key attribute.confidentiality.data was listed as a diff, but lists of objects are hard so you'll need to check.")
        elif key == "plus.event_chain":
            if "event_chain" in diff_json.get("plus", {}):
                print("key plus.event_chain was listed as a diff, but lists of objects are hard so you'll need to check.")
        elif key == "impact.loss":
            if "loss" in diff_json.get("impact", {}):
                print("key impact.loss was listed as a diff, but lists of objects are hard so you'll need to check.")
        else:
            try:
                added_diff = set(d_out.get(key, [])).difference(d_in.get(key, []))
            except:
                print(key)
                print(d_in)
                print(d_out)
                raise
            if len(added_diff) > 0:
                yield "value added to {0}: {1}".format(key, ", ".join(added_diff))
            removed_diff = set(d_in.get(key, [])).difference(d_out.get(key, []))
            if len(removed_diff) > 0:
                yield "value removed from {0}: {1}".format(key, ", ".join(removed_diff))



## MAIN LOOP EXECUTION
def main():
    veris_logger.updateLogger(cfg)
    logging.info('Beginning main loop.')

    # Build examples from Test VERIS records.
    if args['test_examples'] is not None:
        try:
            if not os.path.isdir(args['test_examples']): raise ValueError("Directory does not exist.")
            testfiles = glob.glob(args['test_examples'].rstrip("/") + "/*.json")
            if len(testfiles) <= 0: raise ValueError("No test files found in directory.")
            if args['num_examples'] > 0 and len(testfiles) > args['num_examples']:
                testfiles = random.sample(testfiles, args['num_examples'])
            #logging.debug(testfiles)
            # read in and flatten files
            for filename in testfiles:
                with open(filename, 'r') as filehandle:
                    j = json.load(filehandle)

                if version.parse(j['schema_version']) < version.parse(cfg['version']):
                    j_out = apply_convert(j, convert, cfg=cfg)
                else:
                    j_out = Rules.addRules(j)

                j_diff = diff(j, j_out)
                
                output = []
                output.append("Filename: {0}\n".format(filename))
                output.append("Diff: {0}\n".format(repr(j_diff)))
                for s in diff_lists(j, j_out, j_diff):
                    output.append(s)
                for e in validator.iter_errors(j_out):
                    output.append("Schema validation error: {0}".format(e.message))
                for e in checkValidity.main(j_out):
                    output.append("Business logic validation error: {0}".format(e.message))
                print("\n".join(output))


        except:
            #logging.info("No test files found.")
            raise
    logging.info('Ending main loop.')

if __name__ == "__main__":
    main()
