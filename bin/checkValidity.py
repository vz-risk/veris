# TODO should check if the config file exists before trying to use it.

import simplejson
import nose
import os
from jsonschema import validate, ValidationError, Draft4Validator
import argparse
import ConfigParser
import logging
# import glob
import fnmatch

logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG,
                 50: logging.CRITICAL, 40: logging.ERROR, 30: logging.WARNING, 20: logging.INFO, 10: logging.DEBUG, 0: logging.CRITICAL}
FORMAT = '%(asctime)19s - %(processName)s {0} - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT.format(""), datefmt='%m/%d/%Y %H:%M:%S')

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
    parser.add_argument("-m","--mergedfile", help="The fully merged json schema file.")
    #parser.add_argument("-s", "--schema", help="schema file to validate with")
    #parser.add_argument("-e", "--enum", help="enumeration file to validate with")
    parser.add_argument("-l", "--log_level", choices=["error", "critical", "warning", "info", "debug"],
                        help="Minimum logging level to display", default="warning")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument("-i", "--input", nargs='+', help="list of paths to search for incidents")
    #parser.add_argument("-u", "--plus", help="optional schema for plus section")
    parser.add_argument('--conf', help='The location of the config file', default="../user/data_flow.cfg")
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}



    # Parse the config file
    cfg = {}
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(args["conf"]))
        cfg_key = {
            'GENERAL': ['report', 'input', 'output', 'analysis', 'year', 'force_analyst', 'version', 'database', 'check'],
            'LOGGING': ['log_level', 'log_file'],
            'REPO': ['veris', 'dbir_private'],
            'VERIS': ['mergedfile', 'enumfile', 'schemafile', 'labelsfile', 'countryfile']
        }
        for section in cfg_key.keys():
            if config.has_section(section):
                for value in cfg_key[section]:
                    if value.lower() in config.options(section):
                        cfg[value] = config.get(section, value)
        cfg["year"] = int(cfg["year"])
        logging.debug("config import succeeded.")
    except Exception as e:
        logging.warning("config import failed.")
        #raise e
        pass

    cfg.update(args)


    logging.getLogger().setLevel(logging_remap[cfg["log_level"]])
    logging.info("Now starting checkValidity.")

    logging.debug(args)
    logging.debug(cfg)

    if cfg.get("mergedfile", ""):
        try:
            schema = simplejson.loads(open(cfg["mergedfile"]).read())
        except IOError:
            logging.critical("ERROR: mergedfile not found. Cannot continue.")
            exit(1)
        except simplejson.scanner.JSONDecodeError:
            logging.critical("ERROR: mergedfile is not parsing properly. Cannot continue.")
            exit(1)
    # removed schema joining.  If you need a merged schema, use mergeSchema.py to generate one. - gdb 061416
    else:
      logging.critical("ERROR: mergedfile not found.  Cannot continue.")
      exit(1)

    # Create validator
    validator = Draft4Validator(schema)

    # data_paths = []
    # if args.path:
    #     data_paths = args.path
    # else:  # only use config option if nothing is specified on the command line
    #     try:
    #         path_to_parse = cfg.get('input')
    #         data_paths = path_to_parse.strip().split('\n')
    #     except ConfigParser.Error:
    #         logging.warning("No path specified in config file. Using default")
    #         data_paths = ['.']
    #         pass

    # if "input" in cfg:
    #     cfg["input"] = [l.strip() for l in cfg["input"].split(" ,")]  # spit to list
    # else:
    #     raise ValueError("No input director or file provided to validate.")

    # files_to_validate = set()
    incident_counter = 0
    for src in cfg["input"]:
        if os.path.isfile(src):
            logging.debug("Now validating {0}.".format(src))
            # files_to_validate.add(src)
            try:
                incident = simplejson.load(open(src))
                validator.validate(incident)
                main(incident) 
            except ValidationError as e:
                offendingPath = '.'.join(str(x) for x in e.path)
                logging.warning("ERROR in %s. %s %s" % (src, offendingPath, e.message))    
            except simplejson.scanner.JSONDecoderError:
                logging.warning("ERROR: %s did not parse properly. Skipping" % src)
            incident_counter += 1
            if incident_counter % 100 == 0:
                logging.info("%s incident validated" % incident_counter)
        elif os.path.isdir(src):
            logging.debug("Now validating files in {0}.".format(src))
            src = src.rstrip("/")
            # for inFile in glob.iglob(src + "/*/*.json"):
            for root, dirnames, filenames in os.walk(src):
                for filename in fnmatch.filter(filenames, '*.json'):
                    inFile = os.path.join(root, filename)
                    # files_to_validate.add(inFile)
                    try:
                        incident = simplejson.load(open(inFile))
                        validator.validate(incident)
                        main(incident) 
                    except ValidationError as e:
                        offendingPath = '.'.join(str(x) for x in e.path)
                        logging.warning("ERROR in %s. %s %s" % (inFile, offendingPath, e.message))    
                    except simplejson.scanner.JSONDecoderError:
                        logging.warning("ERROR: %s did not parse properly. Skipping" % inFile)
                    incident_counter += 1
                    if incident_counter % 100 == 0:
                        logging.info("%s incident validated" % incident_counter)


    logging.info("schema assembled successfully.")
    # logging.debug(simplejson.dumps(schema,indent=2,sort_keys=True))

    # data_paths = [x + '/*.json' for x in data_paths]
    # incident_counter = 0
    # for eachDir in data_paths:
    #     for eachFile in glob(eachDir):
    #       logging.debug("Now validating %s" % eachFile)
    #       try:
    #           incident = simplejson.loads(open(eachFile).read())
    #       except simplejson.scanner.JSONDecodeError:
    #           logging.warning("ERROR: %s did not parse properly. Skipping" % eachFile)
    #           continue


          # try:
          #     #validate(incident, schema)
          #     validator.validate(incident)
          #     main(incident)
          # except ValidationError as e:
          #     offendingPath = '.'.join(str(x) for x in e.path)
          #     logging.warning("ERROR in %s. %s %s" % (eachFile, offendingPath, e.message))

          # incident_counter += 1
          # if incident_counter % 100 == 0:
          #     logging.info("%s incident validated" % incident_counter)

    logging.info("checkValidity complete")
