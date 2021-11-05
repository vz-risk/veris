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
def checkDataTotal(inDict):
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


### Validate victim region field
### VERIS issue #180
def checkRegion(inDict):
    regions = {
        "002": ["011", "014", "017", "018", "015", "000"], # Africa
        "010": ["000"], # Antarctica
        "019": ["021", "005", "013", "029", "419", "000"], # America
        "419": ["005", "013", "029"], # Latin America and Caribbean 
        "142": ["030", "034", "035", "143", "145", "000"], # Asia
        "150": ["039", "151", "154", "830", "155", "000"], # Europe
        "009": ["053", "054", "057", "061", "000"], # Oceania
        "000": ["000"] # Unknown
    }
    non_used_regions = {
        "001": "000", # world
        "020": "002", # sub-saharan africa
        "003": "019" # americas"
    }

    for region in inDict.get('victim', {}).get('region', []):
        if type(region) != str or len(region) != 6:
            yield ValidationError("Victim.region {0} is not a six character string.".format(region))
        else:
            super_region = region[:3]
            sub_region = region[3:]
            if super_region in non_used_regions.keys():
                yield ValidationError("Region {2} is incorrect. Replace first half of victim.region ('{0}') with '{1}'.".format(super_region, non_used_regions[super_region], region))
#            elif sub_region in non_used_regions.keys():
#                yield ValidationError("Region {1} is incorrect. Replace second half of victim.region ('{0}') with '000' unless you know the correct region.".format(sub_region, region))
            elif sub_region not in regions.get(super_region, []):
                error_text = "victim.region second half, ('{0}') does not match first half '{1}'".format(sub_region, super_region)
                if super_region in regions:
                    error_text += "  Please replace the second half with one of {0}.".format(", ".join(regions[super_region]))
                else:
                    error_text += "  Since {0} is not a super region, please check the whole region.".format(super_region)
                yield ValidationError(error_text)


### Validate that secondary.victim.amount is > 0 if victim.secondary.victim_id is not empty
### VERIS issue #407
def checkSecondaryVictimAmount(inDict):
    secondary_victims = inDict.get('victim', {}).get('secondary', {}).get('victim_id', [])
    secondary_victim_amount = inDict.get('victim', {}).get('secondary', {}).get('amount', 0)
    if len(secondary_victims) > secondary_victim_amount:
        yield ValidationError("victim.secondary.victim_id lists {0} victims, however victim.secondary.amount is less or missing. Check that the amount is correct.  The amount should be the number of known victims (even if unknown victims may exist.)".format(len(secondary_victims)))


### Check value_chain enumerations that are likely based on actions taken
### VERIS issue #400
def checkValueChain(inDict):
    any_value_chain_recommendation = False
    ### Check enrichments from rules.py
    if 'Phishing' in inDict['action'].get('social', {}).get('variety', []):
        if "Email" not in inDict.get('value_chain', {}).get('development', {}).get('variety', []):
            yield ValidationError("Because incident includes 'action.social.variety.Phishing', 'value_chain.deveopment.variety.Email' should also. Please update.")
        if "Email addresses" not in inDict.get('value_chain', {}).get('targeting', {}).get('variety', []):
            yield ValidationError("Because incident includes 'action.social.variety.Phishing', 'value_chain.targeting.variety.Email addresses' should also. Please update.")
    if 'C2' in inDict['action'].get('malware', {}).get('vector', []) and "C2" not in inDict.get('value_chain', {}).get('non-distribution services', {}).get('variety', []):
        yield ValidationError("Because there is action.malware.variety.C2, value_chain.non-distribution services.variety.C2 should also.  Please update.")
    if 'Ransomware' in inDict['action'].get('malware', {}).get('variety', []):
        if "Cryptocurrency" not in inDict.get('value_chain', {}).get('cash-out', {}).get('variety', []):
            yield ValidationError("Because there is action.malware.variety.Ransomware, value_chain.cash-out.variety.Cryptocurrency should also.  Please update.")
        # note: this is a recommendation, not enrichment
        if "Ransomware" not in inDict.get('value_chain', {}).get('development', {}).get('variety', []):
            yield ValidationError("Because there is action.malware.variety.Ransomware, consider adding value_chain.distribution.variety.Ransomware.")
            any_value_chain_recommendation = True
### This is recommend only
#    if 'Trojan' in inDict['action'].get('malware', {}).get('variety', []) and "Trojan" not in inDict.get('value_chain', {}).get('development', {}).get('variety', []):
#        yield ValidationError("Because there is action.malware.variety.Trojan, value_chain.development.variety.Trojan should also.  Please update.")
    if 'Email' in inDict['action'].get('social', {}).get('vector', []):
        if "Email" not in inDict.get('value_chain', {}).get('distribution', {}).get('variety', []):
            yield ValidationError("Because there is action.social.variety.Email, value_chain.distribution.variety.Email should also.  Please update.")
        # note: this is a recommendation, not enrichment
        if "Email addresses" not in inDict.get('value_chain', {}).get('targeting', {}).get('variety', []):
            yield ValidationError("Because there is action.social.variety.Email addresses, consider adding value_chain.targeting.variety.Email.")
            any_value_chain_recommendation = True

    ### Recommended Only
    if ('malware' in inDict['action'].keys()) & (len(inDict.get('value_chain', {}).get('development', {}).get('variety', [])) == 0):
        yield ValidationError("Because there is a malware action, consider adding a value_chain development variety, even if it is 'Unknown'.")
        any_value_chain_recommendation = True
    if 'Trojan' in inDict['action'].get('malware', {}).get('variety', []) and "Trojan" not in inDict.get('value_chain', {}).get('development', {}).get('variety', []):
        yield ValidationError("Because there is action.malware.variety.Trojan, consider adding value_chain.development.variety.Trojan.")
        any_value_chain_recommendation = True
    if 'Pretexting' in inDict['action'].get('social', {}).get('variety', []) and "Persona" not in inDict.get('value_chain', {}).get('development', {}).get('variety', []):
        yield ValidationError("Because there is action.social.variety.Pretexting, consider adding value_chain.development.variety.Persona.")
        any_value_chain_recommendation = True
    if 'Use of stolen creds' in inDict['action'].get('hacking', {}).get('variety', []) and "Lost or stolen credentials" not in inDict.get('value_chain', {}).get('targeting', {}).get('variety', []):
        yield ValidationError("Because there is action.hacking.variety.Use of stolen creds, consider adding value_chain.targeting.variety.Lost or stolen credentials, but only if the creds are the beginning of the attack and not stolen mid attack.")
        any_value_chain_recommendation = True
    if 'Exploit vuln' in inDict['action'].get('hacking', {}).get('variety', []):
        if "Vulnerabilities" not in inDict.get('value_chain', {}).get('targeting', {}).get('variety', []):
            yield ValidationError("Because there is action.hacking.variety.Exploit vuln, consider adding value_chain.targeting.variety.Vulnerabilities.")
            any_value_chain_recommendation = True
        if "Exploit" not in inDict.get('value_chain', {}).get('development', {}).get('variety', []):
            yield ValidationError("Because there is action.hacking.variety.Exploit vuln, consider adding value_chain.development.variety.Exploit.")
            any_value_chain_recommendation = True
    if 'Downloader' in inDict['action'].get('malware', {}).get('variety', []) and "Loader" not in inDict.get('value_chain', {}).get('distribution', {}).get('variety', []):
        yield ValidationError("Because there is action.malware.variety.Downloader, consider adding value_chain.distribution.variety.Loader.")
        any_value_chain_recommendation = True
    if 'Exploit misconfig' in inDict['action'].get('hacking', {}).get('variety', []) and "Misconfigurations" not in inDict.get('value_chain', {}).get('targeting', {}).get('variety', []):
        yield ValidationError("Because there is action.hacking.variety.Exploit misconfig, consider adding value_chain.targeting.variety.Misconfigurations.")
        any_value_chain_recommendation = True
    if 'Exploit misconfig' in inDict['action'].get('malware', {}).get('variety', []) and "Misconfigurations" not in inDict.get('value_chain', {}).get('targeting', {}).get('variety', []):
        yield ValidationError("Because there is action.malware.variety.Exploit misconfig, consider adding value_chain.targeting.variety.Misconfigurations.")
        any_value_chain_recommendation = True
    if 'Web application' in inDict['action'].get('malware', {}).get('vector', []) and "Website" not in inDict.get('value_chain', {}).get('development', {}).get('variety', []):
        yield ValidationError("Because there is action.malware.vector.Web application, consider adding value_chain.development.variety.Website.")
        any_value_chain_recommendation = True
    if 'Web application' in inDict['action'].get('social', {}).get('vector', []) and "Website" not in inDict.get('value_chain', {}).get('development', {}).get('variety', []):
        yield ValidationError("Because there is action.social.vector.Web application, consider adding value_chain.development.variety.Website.")
        any_value_chain_recommendation = True
    if any_value_chain_recommendation:
        yield ValidationError("Some value_chain changes are recommendations only.  This could be for one of three reasons: The actor could have gotten it free.  The actor could have obtained it during the incident (e.g. creds).  Website describes building a full website, not just uploading a file or such.  Please take these into account when updating the incident.")



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
  for e in checkDataTotal(incident):
    yield e
# Added with 1.3.6    
  for e in checkRegion(incident):
    yield e
  for e in checkSecondaryVictimAmount(incident):
    yield e
  for e in checkValueChain(incident):
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
