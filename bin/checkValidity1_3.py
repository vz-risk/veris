# TODO should check if the config file exists before trying to use it.

import simplejson
import nose
import os
from jsonschema import validate, ValidationError
import argparse
import ConfigParser
import logging
from glob import glob

defaultSchema = "../verisc.json"
defaultEnum = "../verisc-enum.json"


def buildSchema(schema, enum, plus):
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
    schema['properties']['asset']['properties']['assets']['items']['properties']['variety']['enum'] = \
        enum['asset']['variety']
    schema['properties']['asset']['properties']['governance']['items']['enum'] = \
        enum['asset']['governance']

    # attribute properties
    schema['properties']['attribute']['properties']['availability']['properties']['variety']['items']['enum'] = \
        enum['attribute']['availability']['variety']
    schema['properties']['attribute']['properties']['availability']['properties']['duration']['properties']['unit'][
        'enum'] = enum['timeline']['unit']
    schema['properties']['attribute']['properties']['confidentiality']['properties']['data']['items']['properties'][
        'variety']['enum'] = enum['attribute']['confidentiality']['data']['variety']
    schema['properties']['attribute']['properties']['confidentiality']['properties']['data_disclosure'][
        'enum'] = enum['attribute']['confidentiality']['data_disclosure']
    schema['properties']['attribute']['properties']['confidentiality']['properties']['state']['items']['enum'] = \
        enum['attribute']['confidentiality']['state']
    schema['properties']['attribute']['properties']['integrity']['properties']['variety']['items']['enum'] = \
        enum['attribute']['integrity']['variety']

    # impact
    schema['properties']['impact']['properties']['iso_currency_code']['enum'] = enum['iso_currency_code']
    schema['properties']['impact']['properties']['loss']['items']['properties']['variety']['enum'] = \
        enum['impact']['loss']['variety']
    schema['properties']['impact']['properties']['loss']['items']['properties']['rating']['enum'] = \
        enum['impact']['loss']['rating']
    schema['properties']['impact']['properties']['overall_rating']['enum'] = \
        enum['impact']['overall_rating']

    # timeline
    for each in ['compromise', 'containment', 'discovery', 'exfiltration']:
        schema['properties']['timeline']['properties'][each]['properties']['unit']['enum'] = \
            enum['timeline']['unit']

    # victim
    schema['properties']['victim']['properties']['country']['items']['enum'] = enum['country']
    schema['properties']['victim']['properties']['employee_count']['enum'] = \
        enum['victim']['employee_count']
    schema['properties']['victim']['properties']['revenue']['properties']['iso_currency_code']['enum'] = \
        enum['iso_currency_code']

    # Randoms
    for each in ['confidence', 'cost_corrective_action', 'discovery_method', 'security_incident', 'targeted']:
        schema['properties'][each]['enum'] = enum[each]

    # Plus section
    schema['properties']['plus'] = plus

    return schema  # end of buildSchema()


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


if __name__ == '__main__':
    # TODO: implement config file options for all of these
    parser = argparse.ArgumentParser(description="Checks a set of json files to see if they are valid VERIS incidents")
    parser.add_argument("-m", "--merge", help="fully merged json file. Overrides --schema, --enum, and --plus")
    parser.add_argument("-s", "--schema", help="schema file to validate with")
    parser.add_argument("-e", "--enum", help="enumeration file to validate with")
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
    else:
        if args.schema:
          schema_file = args.schema
        else:
          try:
            schema_file = config.get('VERIS','schemafile')
          except ConfigParser.Error:
            logging.warning("No schemafile specified in config file. Using default")
            schema_file = defaultSchema

        if args.enum:
          enum_file = args.enum
        else:
          try:
            enum_file = config.get('VERIS','enumfile')
          except ConfigParser.Error:
            logging.warning("No enumfile specified in config file. Using default")
            enum_file = defaultEnum

        if args.plus:
          plus_file = args.plus
        else:
          try:
            plus_file = config.get('VERIS','plusfile')
          except ConfigParser.Error:
            logging.warning("No plus file specified in config file. Using empty")
            plus_file = "empty"

        try:
            sk = simplejson.loads(open(schema_file).read())
        except IOError:
            logging.critical("ERROR: schema file not found. Cannot continue.")
            exit(1)
        except simplejson.scanner.JSONDecodeError:
            logging.critical("ERROR: schema file is not parsing properly. Cannot continue.")
            exit(1)

        try:
            en = simplejson.loads(open(enum_file).read())
        except IOError:
            logging.critical("ERROR: enumeration file is not found. Cannot continue.")
            exit(1)
        except simplejson.scanner.JSONDecodeError:
            logging.critical("ERROR: enumeration file is not parsing properly. Cannot continue.")
            exit(1)

        if plus_file == "empty":
          pl = {}
        else:
          try:
            pl = simplejson.loads(open(plus_file).read())
          except IOError:
            logging.critical("ERROR: plus file is not found. Unable to validate plus section.")
            pl = {}
          except simplejson.scanner.JSONDecodeError:
            logging.critical("ERROR: plus file is not parsing properly. Unable to validate plus section.")
            pl = {}

        # Now we can build the schema which will be used to validate our incidents
        schema = buildSchema(sk, en, pl)

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
              validate(incident, schema)
              checkMalwareIntegrity(incident)
              checkSocialIntegrity(incident)
              checkSQLiRepurpose(incident)
              checkSecurityIncident(incident)
              checkLossTheftAvailability(incident)
              checkPlusAttributeConsistency(incident)
          except ValidationError as e:
              offendingPath = '.'.join(str(x) for x in e.path)
              logging.warning("ERROR in %s. %s %s" % (eachFile, offendingPath, e.message))

          incident_counter += 1
          if incident_counter % 100 == 0:
              logging.info("%s incident validated" % incident_counter)

    logging.info("checkValidity complete")
