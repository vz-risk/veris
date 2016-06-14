# TODO should check if the config file exists before trying to use it.

import simplejson
import nose
import os
from jsonschema import validate, ValidationError, Draft4Validator
import argparse
import ConfigParser
import logging
from glob import glob

#defaultSchema = "../verisc.json"
#defaultEnum = "../verisc-enum.json"
defaultMerged = "../verisc-merged.json"


def checkMalwareIntegrity(inDict):
    if 'malware' in inDict['action']:
        if 'Software installation' not in inDict.get('attribute',{}).get('integrity',{}).get('variety',[]):
          raise ValidationError("Malware present, but no Software installation in attribute.integrity.variety")
    return True


def checkSocialIntegrity(inDict):
  if 'social' in inDict['action']:
    if 'Alter behavior' not in inDict.get('attribute',{}).get('integrity',{}).get('variety',[]):
      raise ValidationError("acton.social present, but Alter behavior not in attribute.integrity.variety")
  return True


def checkSQLiRepurpose(inDict):
  if 'SQLi' in inDict.get('action',{}).get('hacking',{}).get('variety',[]):
    if 'Repurpose' not in inDict.get('attribute',{}).get('integrity',{}).get('variety',[]):
      raise ValidationError("action.hacking.SQLi present but Repurpose not in attribute.integrity.variety")
  return True


def checkSecurityIncident(inDict):
  if inDict['security_incident'] == "Confirmed":
    if 'attribute' not in inDict:
      raise ValidationError("security_incident Confirmed but attribute section not present")
  return True


def checkLossTheftAvailability(inDict):
  expectLoss = False
  if 'Theft' in inDict.get('action',{}).get('physical',{}).get('variety',[]):
    expectLoss = True
  if 'Loss' in inDict.get('action',{}).get('error',{}).get('variety',[]):
    expectLoss = True
  if expectLoss:
    if 'Loss' not in inDict.get('attribute',{}).get('availability',{}).get('variety',[]):
      raise ValidationError("action.physical.theft or action.error.loss present but attribute.availability.loss not present")
  return True

def checkPlusAttributeConsistency(inDict):
  if 'confidentiality' in inDict.get('plus', {}).get('attribute', {}):
    if 'confidentiality' not in inDict.get('attribute', {}):
      raise ValidationError("plus.attribute.confidentiality present but confidentiality is not an affected attribute.")

def main(incident):
  checkMalwareIntegrity(incident)
  checkSocialIntegrity(incident)
  checkSQLiRepurpose(incident)
  checkSecurityIncident(incident)
  checkLossTheftAvailability(incident)
  checkPlusAttributeConsistency(incident)


if __name__ == '__main__':
    # TODO: implement config file options for all of these
    parser = argparse.ArgumentParser(description="Checks a set of json files to see if they are valid VERIS incidents")
    parser.add_argument("-m", "--merge", help="fully merged json file. Overrides --schema, --enum, and --plus")
    #parser.add_argument("-s", "--schema", help="schema file to validate with")
    #parser.add_argument("-e", "--enum", help="enumeration file to validate with")
    parser.add_argument("-l", "--logging", choices=["critical", "warning", "info", "debug"],
                        help="Minimum logging level to display", default="warning")
    parser.add_argument("-p", "--path", nargs='+', help="list of paths to search for incidents")
    parser.add_argument("-u", "--plus", help="optional schema for plus section")
    args = parser.parse_args()
    logging_remap = {'warning': logging.WARNING, 'critical': logging.CRITICAL, 'info': logging.INFO, 'debug': logging.DEBUG}
    logging.basicConfig(level=logging_remap[args.logging])
    logging.info("Now starting checkValidity.")

    config = ConfigParser.ConfigParser()
    config.read('_checkValidity.cfg')

    if args.merge:
        try:
            schema = simplejson.loads(open(args.merge).read())
        except IOError:
            logging.critical("ERROR: merge file not found. Cannot continue.")
            exit(1)
        except simplejson.scanner.JSONDecodeError:
            logging.critical("ERROR: merge file is not parsing properly. Cannot continue.")
            exit(1)
    # removed schema joining.  If you need a merged schema, use mergeSchema.py to generate one. - gdb 061416
    else:
      logging.critical("ERROR: merge file not found.  Cannot continue.")

    # Create validator
    validator = Draft4Validator(schema)

    data_paths = []
    if args.path:
        data_paths = args.path
    else:  # only use config option if nothing is specified on the command line
        try:
            path_to_parse = config.get('VERIS', 'datapath')
            data_paths = path_to_parse.strip().split('\n')
        except ConfigParser.Error:
            logging.warning("No path specified in config file. Using default")
            data_paths = ['.']
            pass
    logging.info("schema assembled successfully.")
    logging.debug(simplejson.dumps(schema,indent=2,sort_keys=True))

    data_paths = [x + '/*.json' for x in data_paths]
    incident_counter = 0
    for eachDir in data_paths:
        for eachFile in glob(eachDir):
          logging.debug("Now validating %s" % eachFile)
          try:
              incident = simplejson.loads(open(eachFile).read())
          except simplejson.scanner.JSONDecodeError:
              logging.warning("ERROR: %s did not parse properly. Skipping" % eachFile)
              continue


          try:
              #validate(incident, schema)
              validator.validate(incident)
              main(incident)
          except ValidationError as e:
              offendingPath = '.'.join(str(x) for x in e.path)
              logging.warning("ERROR in %s. %s %s" % (eachFile, offendingPath, e.message))

          incident_counter += 1
          if incident_counter % 100 == 0:
              logging.info("%s incident validated" % incident_counter)

    logging.info("checkValidity complete")
