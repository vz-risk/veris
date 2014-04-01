#TODO should check if the config file exists before trying to use it.

import simplejson
import nose
import os
from jsonschema import validate, ValidationError
import argparse
import ConfigParser
import logging
from glob import glob


def buildSchema(schema, enum):
    # All of the action enumerations
    for each in ['hacking', 'malware', 'social', 'error', 'misuse', 'physical']:
        schema['properties']['action']['properties'][each]['properties']['variety']['items']['enum'] = \
        enum['action'][each]['variety']
        schema['properties']['action']['properties'][each]['properties']['vector']['items']['enum'] = \
        enum['action'][each]['vector']
    schema['properties']['action']['properties']['environmental']['properties']['variety']['items']['enum'] = \
    enum['action']['environmental']['variety']
    schema['properties']['action']['properties']['social']['properties']['target']['items']['enum'] = \
    enum['action']['social']['target']

    # actor enumerations
    for each in ['external', 'internal', 'partner']:
        schema['properties']['actor']['properties'][each]['properties']['motive']['items']['enum'] = enum['actor'][
            'motive']
    schema['properties']['actor']['properties']['external']['properties']['variety']['items']['enum'] = \
    enum['actor']['external']['variety']
    schema['properties']['actor']['properties']['internal']['properties']['variety']['items']['enum'] = \
    enum['actor']['internal']['variety']
    schema['properties']['actor']['properties']['external']['properties']['country']['items']['enum'] = enum['country']
    schema['properties']['actor']['properties']['partner']['properties']['country']['items']['enum'] = enum['country']

    # asset properties
    schema['properties']['asset']['properties']['assets']['items']['properties']['variety']['pattern'] = '|'.join(
        enum['asset']['variety'])
    schema['properties']['asset']['properties']['governance']['items']['enum'] = \
        enum['asset']['governance']

    # attribute properties
    schema['properties']['attribute']['properties']['availability']['properties']['variety']['items']['enum'] = \
    enum['attribute']['availability']['variety']
    schema['properties']['attribute']['properties']['availability']['properties']['duration']['properties']['unit'][
        'pattern'] = '|'.join(enum['timeline']['unit'])
    schema['properties']['attribute']['properties']['confidentiality']['properties']['data']['items']['properties'][
        'variety']['pattern'] = '|'.join(enum['attribute']['confidentiality']['data']['variety'])
    schema['properties']['attribute']['properties']['confidentiality']['properties']['data_disclosure'][
        'pattern'] = '|'.join(enum['attribute']['confidentiality']['data_disclosure'])
    schema['properties']['attribute']['properties']['confidentiality']['properties']['state']['items']['enum'] = \
    enum['attribute']['confidentiality']['state']
    schema['properties']['attribute']['properties']['integrity']['properties']['variety']['items']['enum'] = \
    enum['attribute']['integrity']['variety']

    # impact
    schema['properties']['impact']['properties']['iso_currency_code']['patter'] = '|'.join(enum['iso_currency_code'])
    schema['properties']['impact']['properties']['loss']['items']['properties']['variety']['pattern'] = '|'.join(
        enum['impact']['loss']['variety'])
    schema['properties']['impact']['properties']['loss']['items']['properties']['rating']['pattern'] = '|'.join(
        enum['impact']['loss']['rating'])
    schema['properties']['impact']['properties']['overall_rating']['patter'] = '|'.join(
        enum['impact']['overall_rating'])

    # timeline
    for each in ['compromise', 'containment', 'discovery', 'exfiltration']:
        schema['properties']['timeline']['properties'][each]['properties']['unit']['pattern'] = '|'.join(
            enum['timeline']['unit'])

    # victim
    schema['properties']['victim']['properties']['country']['pattern'] = '|'.join(enum['country'])
    schema['properties']['victim']['properties']['employee_count']['pattern'] = '|'.join(
        enum['victim']['employee_count'])
    schema['properties']['victim']['properties']['revenue']['properties']['iso_currency_code']['pattern'] = '|'.join(
        enum['iso_currency_code'])

    # Randoms
    for each in ['confidence', 'cost_corrective_action', 'discovery_method', 'security_incident', 'targeted']:
        schema['properties'][each]['pattern'] = '|'.join(enum[each])

    return schema # end of buildSchema()

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

def checkSQLMisappropriation(inDict):
  if 'SQLi' in inDict.get('action',{}).get('hacking',{}).get('variety',[]):
    if 'Misappropriation' not in inDict.get('attribute',{}).get('integrity',{}).get('variety',[]):
      raise ValidationError("action.hacking.SQLi present but Misappropriation not in attribute.integrity.variety")
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


if __name__ == '__main__':
    # TODO: implement config file options for all of these
    parser = argparse.ArgumentParser(description="Checks a set of json files to see if they are valid VERIS incidents")
    parser.add_argument("-s", "--schema", help="schema file to validate with", default="../verisc.json")
    parser.add_argument("-e", "--enum", help="enumeration file to validate with", default="../verisc-enum.json")
    parser.add_argument("-l", "--logging", choices=["critical", "warning", "info"],
                        help="Minimum logging level to display", default="warning")
    parser.add_argument("-p", "--path", nargs='+', help="list of paths to search for incidents")
    args = parser.parse_args()
    logging_remap = {'warning': logging.WARNING, 'critical': logging.CRITICAL, 'info': logging.INFO}
    logging.basicConfig(level=logging_remap[args.logging])
    logging.info("Now starting checkValidity.")

    # Do we want to fix this? Should command line OVERRIDE config file
    # or just add to the list of places to look?
    config = ConfigParser.ConfigParser()
    config.read('checkValidity.cfg')
    data_paths = []
    if args.path:
        data_paths = args.path
    else:  # only use config option if nothing is specified on the command line
        try:
            path_to_parse = config.get('VERIS', 'datapath')
            data_paths = path_to_parse.strip().split('\n')
        except ConfigParser.Error:
            print "No path found in config file, continuing..."
            data_paths = ['.']
            pass

    try:
        sk = simplejson.loads(open(args.schema).read())
    except IOError:
        logging.critical("ERROR: schema file not found. Cannot continue.")
        exit(1)
    except simplejson.scanner.JSONDecodeError:
        logging.critical("ERROR: schema file is not parsing properly. Cannot continue.")
        exit(1)

    try:
        en = simplejson.loads(open(args.enum).read())
    except IOError:
        logging.critical("ERROR: enumeration file is not found. Cannot continue.")
        exit(1)
    except simplejson.scanner.JSONDecodeError:
        logging.critical("ERROR: enumeration file is not parsing properly. Cannot continue.")
        exit(1)

    # Now we can build the schema which will be used to validate our incidents
    schema = buildSchema(sk, en)
    logging.info("schema assembled successfully.")

    data_paths = [x + '/*.json' for x in data_paths]
    for eachDir in data_paths:
        for eachFile in glob(eachDir):
          try:
              incident = simplejson.loads(open(eachFile).read())
          except simplejson.scanner.JSONDecodeError:
              logging.warning("ERROR: %s did not parse properly. Skipping" % eachFile)
              continue

          try:
              validate(incident, schema)
              checkMalwareIntegrity(incident)
              checkSocialIntegrity(incident)
              checkSQLMisappropriation(incident)
              checkSecurityIncident(incident)
              checkLossTheftAvailability(incident)
          except ValidationError as e:
              offendingPath = '.'.join(str(x) for x in e.path)
              logging.warning("ERROR in %s. %s %s" % (eachFile, offendingPath, e.message))

    logging.info("checkValidity complete")
