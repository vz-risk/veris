# TODO should check if the config file exists before trying to use it.

import simplejson
# import nose # removing as I don't think it's used. - GDB 18-11-05
import os
from jsonschema import validate, ValidationError, Draft4Validator
import argparse
import configparser
import logging
# import glob
import fnmatch
from datetime import date
import importlib
import zipfile # to decompress
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    spec = importlib.util.spec_from_file_location("veris_logger", script_dir + "/veris_logger.py")
    veris_logger = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(veris_logger)
    # veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise


#logging.basicConfig(level=logging.INFO, format=FORMAT.format(""), datefmt='%m/%d/%Y %H:%M:%S')

#defaultSchema = "../verisc.json"
#defaultEnum = "../verisc-enum.json"
defaultMerged = "../verisc-merged.json"


def checkMalwareIntegrity(inDict):
    if 'malware' in inDict.get("action", {}):
        if 'Software installation' not in inDict.get('attribute',{}).get('integrity',{}).get('variety',[]):
          yield ValidationError("Malware present, but no Software installation in attribute.integrity.variety")


def checkSocialIntegrity(inDict):
  if 'social' in inDict.get("action", {}):
    if 'Alter behavior' not in inDict.get('attribute',{}).get('integrity',{}).get('variety',[]):
      yield ValidationError("acton.social present, but Alter behavior not in attribute.integrity.variety")


def checkSQLiRepurpose(inDict):
  if 'SQLi' in inDict.get('action',{}).get('hacking',{}).get('variety',[]):
    if 'Repurpose' not in inDict.get('attribute',{}).get('integrity',{}).get('variety',[]):
      yield ValidationError("action.hacking.SQLi present but Repurpose not in attribute.integrity.variety")


def checkSecurityIncident(inDict):
  if 'security_incident' not in inDict:
    yield ValidationError("security_incident not in incident.")
  else:
    if inDict['security_incident'] == "Confirmed" and 'attribute' not in inDict:
      yield ValidationError("security_incident Confirmed but attribute section not present")


def checkLossTheftAvailability(inDict):
  expectLoss = False
  if 'Theft' in inDict.get('action',{}).get('physical',{}).get('variety',[]):
    expectLoss = True
  if 'Loss' in inDict.get('action',{}).get('error',{}).get('variety',[]):
    expectLoss = True
  if expectLoss:
    if 'Loss' not in inDict.get('attribute',{}).get('availability',{}).get('variety',[]):
      yield ValidationError("action.physical.theft or action.error.loss present but attribute.availability.loss not present")

def checkPlusAttributeConsistency(inDict):
  if 'confidentiality' in inDict.get('plus', {}).get('attribute', {}):
    if 'confidentiality' not in inDict.get('attribute', {}):
      yield ValidationError("plus.attribute.confidentiality present but confidentiality is not an affected attribute.")

def checkYear(inDict):
    if inDict.get('plus', {}).get('dbir_year', None):
        dbir_year = inDict['plus']['dbir_year']
        nyear = inDict.get('plus', {}).get('timeline', {}).get('notification', {}).get('year', None)
        nmonth = inDict.get('plus', {}).get('timeline', {}).get('notification', {}).get('month', None)
        nday = inDict.get('plus', {}).get('timeline', {}).get('notification', {}).get('day', None)
        iyear = inDict.get('timeline', {}).get('incident', {}).get('year', None)
        imonth = inDict.get('timeline', {}).get('incident', {}).get('month', None)
        iday = inDict.get('timeline', {}).get('incident', {}).get('day', None)
        discovered = inDict.get('timeline', {}).get('discovered', {}).get('unit', "(no discovery unit)")
        if nyear is not None:
            source = "notification"
            tyear = nyear
            tmonth = nmonth
        else:
            tyear = iyear
            tmonth = imonth
            source = "incident"
        if tyear >= dbir_year:
            yield ValidationError("DBIR year of {0} from {5} runs from Nov 1, {1} to Oct 31, {2}. Incident year {3} and month {4} is too late to be in this DBIR year.".format(
                dbir_year, dbir_year - 2, dbir_year - 1, tyear, tmonth, source))
        if tyear == dbir_year - 1:
            if tmonth is not None and tmonth > 10:
                yield ValidationError("DBIR year of {0} from {5} runs from Nov 1, {1} to Oct 31, {2}. Incident year {3} and month {4} is too late to be in this DBIR year.".format(
                    dbir_year, dbir_year - 2, dbir_year - 1, tyear, tmonth, source))
        elif tyear == dbir_year - 2:
            if tmonth is not None and tmonth < 11:
                if discovered in ["Months", "Years"]:
                    yield ValidationError("DBIR year of {0} from {5} runs from Nov 1, {1} to Oct 31, {2}. Incident year {3}, month {4}, and discovery unit {6} is before this range.".format(
                        dbir_year, dbir_year - 2, dbir_year - 1, tyear, tmonth, source, discovered))
        else:
            if discovered != "Years":
                yield ValidationError("DBIR year of {0} from {4} runs from Nov 1, {1} to Oct 31, {2}. Incident year {3} and discovery unit {5} is before this range.".format(
                    dbir_year, dbir_year - 2, dbir_year - 1, tyear, source, discovered)) 
        # check if incident or notification dates are in future
        if nyear is not None:
            try:
                ndate = date(*[x if x else 1 for x in [nyear, nmonth, nday]]) 
            except ValueError as e:
                yield ValidationError("Problem with notification date: {0}".format(e)) 
            if ndate > date.today():
                yield ValidationError("Notification date {0} is greater than today's date {1}.".format(ndate, date.today()))
        try:
            idate = date(*[x if x else 1 for x in [iyear, imonth, iday]])
        except ValueError as e:
            yield ValidationError("Problem with incident date: {0}".format(e))
        if idate > date.today():
            yield ValidationError("Incident date {0} is greater than today's date {1}.".format(idate, date.today()))
        if nyear is not None and idate > ndate:
            yield ValidationError("Notification date {0} appears to be earlier than incident date {1}. This may be due to incomplete dates.".format(ndate, idate))


### sanity check impact.overall_amount to ensure it's at least the sum of losses
## VERIS issue #142
def checkImpactTotal(inDict):
    if 'loss' in inDict.get('impact', {}):
        sum_of_amounts = sum([k.get('amount', 0) for k in inDict['impact']['loss']])
        if sum_of_amounts > inDict['impact'].get('overall_amount', 0):
            yield ValidationError("The amounts in impact.loss sum to {0}, but impact.overall_amount is {1}.  ".format(sum_of_amounts, inDict['impact'].get('overall_amount', "Not Present")) +
                                  "impact.overall_amount should at least be as much as the sum of individual losses.")


### sanity check attribute.confidentiality.data_total to ensure it's at least the max of data lost
## VERIS issue #143
def checkImpactTotal(inDict):
    if 'data' in inDict['attribute'].get('confidentiality', {}):
        max_of_amounts = max([k.get('amount', 0) for k in inDict['attribute']['confidentiality']['data']])
        if max_of_amounts > inDict['attribute']['confidentiality'].get('data_total', 0):
            yield ValidationError("The maximum amount of attribute.confidentiality.data.amount is {0}, but attribute.confidentiality.data_total is {1}.  ".format(max_of_amounts, inDict['attribute']['confidentiality'].get('data_total', "Not Present")) +
                                  "attribute.confidentiality.data_total should at least be as much as the max of individual data amounts.")

### sanity check. if 'misuse', 'actor' should include 'external'
### VERIS issue #229
def checkMisuseActor(inDict):
    if 'misuse' in inDict['action'] and 'internal' not in inDict['actor'] and 'partner' not in inDict['actor']:
        yield ValidationError("Misuse in action, but no internal or partner actor defined.  Per VERIS issue #229, there should always be an internal or partner actor if there is a misuse action.")


def main(incident):
  for e in checkMalwareIntegrity(incident):
    yield e
  for e in checkSocialIntegrity(incident):
    yield e
  for e in checkSQLiRepurpose(incident):
    yield e
  for e in checkSecurityIncident(incident):
    yield e
  for e in checkLossTheftAvailability(incident):
    yield e
  for e in checkPlusAttributeConsistency(incident):
    yield e
  for e in checkYear(incident):
    yield e
  for e in checkImpactTotal(incident):
    yield e
  for e in checkMisuseActor(incident):
    yield e

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
    args = {k:v for k,v in vars(args).items() if v is not None}



    # Parse the config file
    cfg = {}
    try:
        config = configparser.ConfigParser()
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
        veris_logger.updateLogger(cfg)
        logging.debug("config import succeeded.")
    except Exception as e:
        logging.warning("config import failed.")
        #raise e
        pass

    cfg.update(args)
    dateFmt = '%m/%d/%Y %H:%M:%S'
    veris_logger.updateLogger(cfg, None, dateFmt)

    logging.debug(args)
    logging.debug(cfg)

    if cfg.get("mergedfile", ""):
        if type(cfg['mergedfile']) == dict:
            schema = cfg['mergedfile']
        else:
            try:
                schema = simplejson.loads(open(cfg["mergedfile"]).read())
            except IOError:
                logging.critical("ERROR: mergedfile not found. Cannot continue.")
                raise
                # exit(1)
            except simplejson.scanner.JSONDecodeError:
                logging.critical("ERROR: mergedfile is not parsing properly. Cannot continue.")
                raise
                # exit(1)
    # removed schema joining.  If you need a merged schema, use mergeSchema.py to generate one. - gdb 061416
    else:
      IOError("ERROR: mergedfile not found.  Cannot continue.")
      # exit(1)

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
        if os.path.isfile(src) and src.endswith(".json"):
            logging.debug("Now validating {0}.".format(src))
            # errors in json
            try:
                incident = simplejson.load(open(src))
                if type(incident) == list:
                    logging.warning("ERROR: %s is a list (presumably of VERIS json).  If so, it must be zipped to be processed. Skipping" % inFile)
                    continue
            except simplejson.scanner.JSONDecodeError:
                logging.warning("ERROR: %s did not parse properly. Skipping" % src)
                continue
            # replacing vakudate() with iterating errors - 171206 - GDB
            for e in validator.iter_errors(incident):
                offendingPath = '.'.join(str(x) for x in e.path)
                logging.warning("ERROR in %s. %s %s" % (src, offendingPath, e.message))  
            # capture errors from main
            # try:
            #     # validator.validate(incident) # replacing with iterating errors - 171206 GDB  
            #     main(incident) 
            # except ValidationError as e:
            #     offendingPath = '.'.join(str(x) for x in e.path)
            #     logging.warning("ERROR in %s. %s %s" % (src, offendingPath, e.message))  
            for e in main(incident):
                offendingPath = '.'.join(str(x) for x in e.path)
                logging.warning("ERROR in %s. %s %s" % (src, offendingPath, e.message))  

            incident_counter += 1
            if incident_counter % 100 == 0:
                logging.info("%s incident validated" % incident_counter)
        elif os.path.isfile(src) and src.endswith(".zip"):
            with zipfile.ZipFile(src, mode='r', compression=zipfile.ZIP_DEFLATED) as zf:
                for jfile in zf.namelist():
                    with zf.open(jfile) as filehandle:
                        try:
                            incidents = simplejson.load(filehandle)
                        except simplejson.scanner.JSONDecodeError:
                            logging.warning("ERROR: %s in %s did not parse properly. Skipping" % (jfile, src))
                            continue
                        for incident in incidents:
                            for e in validator.iter_errors(incident):
                                offendingPath = '.'.join(str(x) for x in e.path)
                                logging.warning("ERROR in incident %s in file %s in zipfile %s. %s %s" % (incident.get("plus", {}).get("master_id", "Unknown plus.master_id"), jfile, src, offendingPath, e.message))    
                            for e in main(incident):
                                offendingPath = '.'.join(str(x) for x in e.path)
                                logging.warning("ERROR in incident %s in file %s in zipfile %s. %s %s" % (incident.get("plus", {}).get("master_id", "Unknown plus.master_id"), jfile, src, offendingPath, e.message))  

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
                        if type(incident) == list:
                            logging.warning("ERROR: %s is a list (presumably of VERIS json).  If so, it must be zipped to be processed.  Skipping." % inFile)
                            continue
                    except simplejson.scanner.JSONDecodeError:
                        logging.warning("ERROR: %s did not parse properly. Skipping" % inFile)
                        continue
                    for e in validator.iter_errors(incident):
                        offendingPath = '.'.join(str(x) for x in e.path)
                        logging.warning("ERROR in %s. %s %s" % (inFile, offendingPath, e.message)) 
                    for e in main(incident):
                        offendingPath = '.'.join(str(x) for x in e.path)
                        logging.warning("ERROR in %s. %s %s" % (inFile, offendingPath, e.message))  

                    incident_counter += 1
                    if incident_counter % 100 == 0:
                        logging.info("%s incident validated" % incident_counter)
                for filename in fnmatch.filter(filenames, '*.zip'):
                    inFile = os.path.join(root, filename)
                    with zipfile.ZipFile(inFile, mode='r', compression=zipfile.ZIP_DEFLATED) as zf:
                        for jfile in zf.namelist():
                            with zf.open(jfile) as filehandle:
                                try:
                                    incidents = simplejson.load(filehandle)
                                except simplejson.scanner.JSONDecodeError:
                                    logging.warning("ERROR: %s in %s did not parse properly. Skipping" % (jfile, inFile))
                                for incident in incidents:
                                    for e in validator.iter_errors(incident):
                                        offendingPath = '.'.join(str(x) for x in e.path)
                                        logging.warning("ERROR in incident %s in file %s in zipfile %s. %s %s" % (incident.get("plus", {}).get("master_id", "Unknown plus.master_id"), jfile, inFile, offendingPath, e.message))    
                                    for e in main(incident):
                                        offendingPath = '.'.join(str(x) for x in e.path)
                                        logging.warning("ERROR in incident %s in file %s in zipfile %s. %s %s" % (incident.get("plus", {}).get("master_id", "Unknown plus.master_id"), jfile, inFile, offendingPath, e.message)) 

                                    incident_counter += 1
                                    if incident_counter % 100 == 0:
                                        logging.info("%s incident validated" % incident_counter) 
        else:
            logging.warning("%s did not match a known veris format.  Skipping." % src)


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
