import json as sj
import argparse
import logging
from glob import glob
import os
from fnmatch import fnmatch
import configparser
from tqdm import tqdm
#import imp
import importlib
import pprint
# from distutils.version import LooseVersion
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    spec = importlib.util.spec_from_file_location("veris_logger", script_dir + "/veris_logger.py")
    veris_logger = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(veris_logger)
    # veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise

cfg = {
    'log_level': 'warning',
    'log_file': None,
    'countryfile':'./all.json'
}

def getCountryCode(countryfile):
    country_codes = sj.loads(open(countryfile).read())
    country_code_remap = {'Unknown': '000000'}
    for eachCountry in country_codes:
        try:
            country_code_remap[eachCountry['alpha-2']] = \
                eachCountry['region-code']
        except:
            country_code_remap[eachCountry['alpha-2']] = "000"
        try:
            country_code_remap[eachCountry['alpha-2']] += \
                eachCountry['sub-region-code']
        except:
            country_code_remap[eachCountry['alpha-2']] += "000"
    return country_code_remap


def getField(current, txt):
    tsplit = txt.split('.', 1)
    if tsplit[0] in current:
        result = current[tsplit[0]]
        if len(tsplit) > 1:
            result = getField(result, tsplit[1])
    else:
        result = None
    return result


def grepText(incident, searchFor):
    txtFields = ['summary', "notes", "victim.notes", "actor.external.notes",
                 "actor.internal.notes", "actor.partner.notes",
                 "actor.unknown.notes", "action.malware.notes",
                 "action.hacking.notes", "action.social.notes",
                 "action.misuse.notes", "action.physical.notes",
                 "action.error.notes", "action.environmental.notes",
                 "asset.notes", "attribute.confidentiality.notes",
                 "attribute.integrity.notes", "attribute.availability.notes",
                 "impact.notes", "plus.analyst_notes", "plus.pci.notes"]
    foundAny = False
    for txtField in txtFields:
        curText = getField(incident, txtField)
        if isinstance(curText, str): # replaced basestr with str per 2to3. - GDB 181109
          if searchFor.lower() in curText:
              foundAny = True
              break
        # could be extended to look for fields in lists
    return foundAny


def main(cfg):
    veris_logger.updateLogger(cfg)

    last_version = "1.3.4"
    version = "1.3.5"
 
    if cfg.get('log_level', '').lower() == "debug":
        pprint.pprint(cfg) # DEBUG

    logging.info("Converting files from {0} to {1}.".format(cfg["input"], cfg["output"]))
    for root, dirnames, filenames in tqdm(os.walk(cfg['input'])):
      logging.info("starting parsing of directory {0}.".format(root))
      # filenames = filter(lambda fname: fnmatch(fname, "*.json"), filenames)
      filenames = [fname for fname in filenames if fnmatch(fname, "*.json")] # per 2to3. - GDB 181109
      if filenames:
        dir_ = os.path.join(cfg['output'], root[len(cfg['input']):].lstrip("/")) # if we don't strip the input, we get duplicate directories 
        logging.info("Output directory is {0}.".format(dir_))
        if not os.path.isdir(dir_):
            os.makedirs(dir_)
        for fname in filenames:
            in_fname = os.path.join(root,fname)
            out_fname = os.path.join(dir_, fname)

            logging.info("Now processing %s" % in_fname)
            try:
                incident = sj.loads(open(in_fname).read())
            except sj.JSONDecodeError:
                logging.warning(
                    "ERROR: %s did not parse properly. Skipping" % in_fname)
                continue

            if 'assets' not in incident.get('asset', {}):
                raise KeyError("Asset missing from assets in incident {0}.".format(fname))


            # if the record is already version 1.3.5, skip it. This can happen if there are mixed records
            if incident.get('schema_version', last_version) != last_version:
                if incident.get('schema_version', '') != version:
                    logging.warning("Incident {0} is version {1} instead of {2} and can therefore not be updated.".format(fname, incident.get('schema_version', 'NONE'), last_version))
                continue

            # Update the schema version
            incident['schema_version'] = version

            # EXAMPLE UPDATE
#             # Replace asset S - SCADA with S - ICS
#             # Issue 104, Commit f8b7387
#             # if "S - SCADA" in incident.get("asset", {}).get("assets", []):
#                 # incident["asset"]["assets"] = [e.replace("S - SCADA", "S - ICS") for e in incident["asset"]["assets"]]  
#             incident["asset"]["assets"] = [dict(e, **{u"variety": u"S - ICS"}) if e.get(u"variety", "") ==  u"S - SCADA" else e for e in incident["asset"]["assets"]] 

            ## Replace 'Ram' with 'RAM'
            ## Issue 337
            if "variety" in incident["action"].get("malware", {}):
                incident["action"]["malware"]["variety"] = [u"RAM scraper" if e ==  u"Ram scraper" else e for e in incident["action"]["malware"]["variety"]] 

            ## Add Web Application to vectors in all actions
            ## Issue 331
            ## Below two lines removed as the update to social.vector.Web application did not get added.
            #if "vector" in incident["action"].get("social", {}):
            #    incident["action"]["social"]["vector"] = [u"Web application" if e ==  u"Website" else e for e in incident["action"]["social"]["vector"]] 
            if "vector" in incident["action"].get("malware", {}):
                incident["action"]["malware"]["vector"] = [u"Web application - drive-by" if e ==  u"Web drive-by" else e for e in incident["action"]["malware"]["vector"]] 
                incident["action"]["malware"]["vector"] = [u"Web application - download" if e ==  u"Web download" else e for e in incident["action"]["malware"]["vector"]] 
                if 'Web application - drive-by' in incident["action"]["malware"]["vector"] or "web application - download" in incident["action"]["malware"]["vector"]:
                    incident["action"]["malware"]["vector"].append("Web application")


            ### asset.assets.P - End-user defined as 'End-user or regular employee' is being split into asset.assets.P - End-user and asset.assets.P - Other employee
            # per vz-risk/VERIS issue #306
            incident['asset']['assets']= [enum if enum.get(u"variety", "") != "P - End-user" else dict(enum, **{u"variety": u"P - End-user or employee"}) for enum in incident['asset']['assets']]

            ## Summary now required
            ## per vz-risk/VERIS issue #305
            if "summary" not in incident:
                incident["summary"] = ""

            ## Monitoring service shoudl never be external in discovery_method.  Moving to partner.
            ## per vz-risk/VERIS issue #304
            if type(incident['discovery_method']) == dict: # because "Unknown" and "Other" may be strings
                if "Monitoring service" in incident['discovery_method'].get("external", {}).get("variety", []):
                    # Add Monitoring service to partner 
                    if 'partner' not in incident['discovery_method']:
                        incident['discovery_method']['partner'] = {'variety': ["Monitoring service"]}
                    elif 'variety' not in incident['discovery_method']['partner']:
                        incident['discovery_method']['partner']["variety"] = ["Monitoring service"]
                    elif "Monitoring service" not in incident['discovery_method']['partner']["variety"]:
                        incident['discovery_method']['partner']["variety"].append("Monitoring service")
                        if "Unknown" in incident['discovery_method']['partner']["variety"]:
                            incident['discovery_method']['partner']["variety"].remove("Unknown")
                    # Remove monitorign service from external, and then (probably) remove external
                    incident['discovery_method']['external']['variety'].remove("Monitoring service")
                    if len(incident['discovery_method']['external']['variety']) == 0:
                        _ = incident['discovery_method'].pop('external')


            ## "infiltrate" shoudl nto exist in 'misuse.result'
            ## per vz-risk/VERIS issue #281
            if 'misuse' in incident['action']:
                if 'Infiltrate' in incident['action']['misuse'].get('result', []):
                    incident['action']['misuse']['result'].remove("Infiltrate")
                    if len(incident['action']['misuse']['result']) == 0:
                        _ = incident['action']['misuse'].pop('result')


            ## update of physical vector. Added last year, but trnsitions were not applied.
            ## per issue Vvz-risk/VERIS issue #198
            if "vector" in incident["action"].get("physical", {}):
                incident["action"]["physical"]["vector"] = [u"Victim work area" if e ==  u"Visitor privileges" else e for e in incident["action"]["physical"]["vector"]] 
                incident["action"]["physical"]["vector"] = [u"Public facility" if e ==  u"Uncontrolled location" else e for e in incident["action"]["physical"]["vector"]]

            ## Change "Validated" to "Reviewed" in plus.analysis_status for consistency with workflow
            ## Per vz-risk/VERIS issue # 303
            if incident["plus"].get("analysis_status", "") == "Validated":
                incident["plus"]["analysis_status"] = "Reviewed"


            ## Chang "Not Applicable" to NA in all but PCI
            ## Per  vz-risk/VERIS #301
            if "asset_os" in incident["plus"]:
                incident["plus"]["asset_os"] = [u"NA" if e ==  u"Not applicable" else e for e in incident["plus"]["asset_os"]] 
            if "attack_difficulty_initial" in incident["plus"]:
                if incident["plus"]["attack_difficulty_initial"] == "Not applicable":
                    incident["plus"]["attack_difficulty_initial"] = "NA"
            if "attack_difficulty_legacy" in incident["plus"]:
                if incident["plus"]["attack_difficulty_legacy"] == "Not applicable":
                    incident["plus"]["attack_difficulty_legacy"] = "NA"
            if "attack_difficulty_subsequent" in incident["plus"]:
                if incident["plus"]["attack_difficulty_subsequent"] == "Not applicable":
                    incident["plus"]["attack_difficulty_subsequent"] = "NA"

            ## "government" is required in victim
            ## per vz-risk/VERIS #347
            if "government" not in incident['victim']:
                if incident['victim']['industry'][:2] != "92":
                    incident['victim']['government'] = ["NA"]
                else:
                    incident['victim']['government'] = ["Unknown"]

            ## "cloud" is now required in "asset"
            if "asset" in incident:
                if "cloud" not in incident['asset']:
                    incident['asset']['cloud'] = ["Unknown"]

            # Now to save the incident
            logging.info("Writing new file to %s" % out_fname)
            with open(out_fname, 'w') as outfile:
                sj.dump(incident, outfile, indent=2, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    descriptionText = "Converts VERIS 1.3.3 incidents to v1.3.4"
    helpText = "output directory to write new files. Default is to overwrite."
    parser = argparse.ArgumentParser(description=descriptionText)
    parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument("-i", "--input", required=True,
                        help="top level folder to search for incidents")
    parser.add_argument("-o", "--output",
                        help=helpText)
    # parser.add_argument('--countryfile', help='The json file holdering the country mapping.')
    parser.add_argument('--conf', help='The location of the config file', default="../user/data_flow.cfg")
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).items() if v is not None}

    # logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG} # defined above. - gdb 080716

    # Parse the config file
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
        veris_logger.updateLogger(cfg)
        logging.debug("config import succeeded.")
    except Exception as e:
        logging.warning("config import failed with error {0}.".format(e))
        #raise e
        pass
    # place any unique config file parsing here
    if "input" in cfg:
        cfg["input"] = [l.strip() for l in cfg["input"].split(" ,")]  # spit to list

    cfg.update(args)

    if "output" not in cfg:
        cfg["output"] = cfg["input"]

    veris_logger.updateLogger(cfg)

    # country_region = getCountryCode(cfg['countryfile'])

    # assert args.path != args.output, "Source and destination must differ"

    main(cfg)

