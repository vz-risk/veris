import json as sj
import argparse
import logging
from glob import glob
import os
from fnmatch import fnmatch
import configparser
from tqdm import tqdm
#import imp
from importlib import util
import pprint
# from distutils.version import LooseVersion
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    spec = util.spec_from_file_location("veris_logger", script_dir + "/veris_logger.py")
    veris_logger = util.module_from_spec(spec)
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
    #country_codes = sj.loads(open(countryfile).read())
    with open(countryfile, 'r') as filehandle:
        country_codes = sj.load(filehandle)
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

    last_version = "1.3.5"
    version = "1.3.6"
 
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
                #incident = sj.loads(open(in_fname).read())
                with open(in_fname, 'r') as filehandle:
                    incident = sj.load(filehandle)
            except sj.JSONDecodeError:
                logging.warning(
                    "ERROR: %s did not parse properly. Skipping" % in_fname)
                continue

            if 'assets' not in incident.get('asset', {}):
                raise KeyError("Asset missing from assets in incident {0}.".format(fname))


            # if the record is already version 1.3.6, skip it. This can happen if there are mixed records
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

            # Per https://github.com/vz-risk/veris/issues/271
            # infer actor.*.motive.Secondary if malware.variety.DoS
            if 'DoS' in incident['action'].get('malware', {}).get('variety', []):
                actors = incident['actor'].keys()
                if 'external' in actors:
                    actors = "external"
                elif 'partner' in actors:
                    actors = "partner"
                elif 'internal' in actors:
                    actors = "internal"
                else:
                    actors = "unknown"
                if actors != "unknown":
                    motive = incident['actor'][actors].get('motive', [])
                    if 'Secondary' not in motive:
                        if ('Unknown' in motive) and (len(motive) == 1): # if the only motive is 'Unknown', remove it to replace with Secondary
                            motive.remove('Unknown')
                        motive.append('Secondary')
                        incident['actor'][actors]['motive'] = motive
                        notes = incident['actor'][actors].get('notes', '')
                        notes = notes + "\n" + "VERIS 1.3.6: actor.{0}.motive.Secondary added because action.malware.variety.DoS exists.".format(actors)
                        incident['actor'][actors]['notes'] = notes.strip()

            ### Hierarchical Field
            # `action.malware.variety.Backdoor or C2` is a parent of `action.malware.variety.Backdoor` and `action.malware.variety.C2`
            # per vz-risk/VERIS issue # 383
            if 'malware' in incident.get('action', {}):
                if ('C2' in incident['action']['malware'].get('variety', []) or \
                'Backdoor' in incident['action']['malware'].get('variety', [])) and \
                'Backdoor or C2' not in incident['action']['malware'].get('variety', []):
                    incident['action']['malware']['variety'].append('Backdoor or C2')
            # `action.hacking.variety.Backdoor or C2` becomes `action.hacking.variety.Backdoor
            if 'Backdoor or C2' in incident.get('action', {}).get('hacking', {}).get('vector', []):
                incident['action']['hacking']['vector'].remove('Backdoor or C2')
                incident['action']['hacking']['vector'].append('Backdoor')
            if 'Use of backdoor or C2' in incident.get('action', {}).get('hacking', {}).get('variety', []):
                incident['action']['hacking']['variety'].remove('Use of backdoor or C2' )
                if len(incident['action']['hacking']['variety']) == 0:
                    incident['action']['hacking']['variety'] = ["Unknown"]
                    notes = incident['action']['hacking'].get('notes', "")
                    incident['action']['hacking']['notes'] = (notes + "\n" + "VERIS 1.3.6: Moved 'Use of backdoor or C2' to 'backdoor' in hacking.vectors causing hacking.variety to be empty.  So adding hacking.variety.Unknown for schema compliance.").strip()
                if 'Backdoor' not in incident['action']['hacking'].get('vector', []):
                    incident['action']['hacking']['vector'].append('Backdoor')

            # Fix HTTP Response Splitting capitalization to be more consistent
            # per vz-risk/VERIS issue # 386
            if 'HTTP Response Splitting' in incident.get('action', {}).get('hacking', {}).get('variety', []):
                incident['action']['hacking']['variety'].remove('HTTP Response Splitting')
                incident['action']['hacking']['variety'].append('HTTP response splitting')

            # Fix 'Website' inconsistencies
            # per vz-risk/VERIS issue # 401
            if 'Website' in incident.get('action', {}).get('social', {}).get('vector', []):
                incident['action']['social']['vector'].remove('Website')
                incident['action']['social']['vector'].append('Web application')

            # plus.analysis_status.Needs review -> plus.analysis_status.Ready for review
            # per vz-risk/VERIS issue # 405
            if 'Needs review' == incident.get('plus', {}).get('analysis_status', ""):
                incident['plus']['analysis_status'] = 'Ready for review'

            ### Validate that secondary.victim.amount is > 0 if victim.secondary.victim_id is not empty
            ### VERIS issue #407
            secondary_victims = incident.get('victim', {}).get('secondary', {}).get('victim_id', [])
            secondary_victim_amount = incident.get('victim', {}).get('secondary', {}).get('amount', 0)
            if secondary_victim_amount < 0: # I can't believe someone would make this negative, but just in case....
                secondary_victim_amount == 0
                incident['victim']['secondary']['amount'] == 0
            if len(secondary_victims) > secondary_victim_amount:
                incident['victim']['secondary']['amount'] = len(secondary_victims)

            ### Check value_chain enumerations that are likely based on actions taken
            ### VERIS issue #400
            add_any_value_chain = False
            if 'Phishing' in incident['action'].get('social', {}).get('variety', []):
                add_value_chain = False
                if 'value_chain' not in incident:
                    incident['value_chain'] = {'targeting': {'variety': ['Email addresses']}}
                    add_value_chain = True
                elif 'targeting' not in incident['value_chain']:
                    incident['value_chain']['targeting'] = {'variety': ['Email addresses']}
                    add_value_chain = True
                elif 'variety' not in incident['value_chain']['targeting']:
                    incident['value_chain']['targeting']['variety'] = ['Email addresses']
                    add_value_chain = True
                elif 'Email addresses' not in incident['value_chain']['targeting']['variety']:
                    incident['value_chain']['targeting']['variety'].append("Email addresses")
                    add_value_chain = True
                if add_value_chain:
                    add_any_value_chain = True
                    notes = incident['value_chain']['targeting'].get('notes', "")
                    incident['value_chain']['targeting']['notes'] = (notes + "\n" + "VERIS 1.3.6: value_chain.targeting.variety.Email addresses added because action.social.vector.Email exists.").strip()
                add_value_chain = False
                if 'value_chain' not in incident:
                    incident['value_chain'] = {'development': {'variety': ['Email']}}
                    add_value_chain = True
                elif 'development' not in incident['value_chain']:
                    incident['value_chain']['development'] = {'variety': ['Email']}
                    add_value_chain = True
                elif 'variety' not in incident['value_chain']['development']:
                    incident['value_chain']['development']['variety'] = ['Email']
                    add_value_chain = True
                elif 'Email' not in incident['value_chain']['development']['variety']:
                    incident['value_chain']['development']['variety'].append("Email")
                    add_value_chain = True
                if add_value_chain:
                    add_any_value_chain = True
                    notes = incident['value_chain']['development'].get('notes', "")
                    incident['value_chain']['development']['notes'] = (notes + "\n" + "VERIS 1.3.6: value_chain.development.variety.Email added because action.social.vector.Email exists.").strip()
            if 'C2' in incident['action'].get('malware', {}).get('vector', []):
                add_value_chain = False
                if 'value_chain' not in incident:
                    incident['value_chain'] = {'non-distribution services': {'variety': ['C2']}}
                    add_value_chain = True
                elif 'non-distribution services' not in incident['value_chain']:
                    incident['value_chain']['non-distribution services'] = {'variety': ['C2']}
                    add_value_chain = True
                elif 'variety' not in incident['value_chain']['non-distribution services']:
                    incident['value_chain']['non-distribution services']['variety'] = ['C2']
                    add_value_chain = True
                elif 'C2' not in incident['value_chain']['non-distribution services']['variety']:
                    incident['value_chain']['non-distribution services']['variety'].append("C2")
                    add_value_chain = True
                if add_value_chain:
                    add_any_value_chain = True
                    notes = incident['value_chain']['non-distribution services'].get('notes', "")
                    incident['value_chain']['non-distribution services']['notes'] = (notes + "\n" + "VERIS 1.3.6: value_chain.non-distribution services.variety.C2 added because action.malware.vector.C2 exists.").strip()
            if 'Ransomware' in incident['action'].get('malware', {}).get('variety', []):
                add_value_chain = False
                if 'value_chain' not in incident:
                    incident['value_chain'] = {'cash-out': {'variety': ['Cryptocurrency']}}
                    add_value_chain = True
                elif 'cash-out' not in incident['value_chain']:
                    incident['value_chain']['cash-out'] = {'variety': ['Cryptocurrency']}
                    add_value_chain = True
                elif 'variety' not in incident['value_chain']['cash-out']:
                    incident['value_chain']['cash-out']['variety'] = ['Cryptocurrency']
                    add_value_chain = True
                elif 'Cryptocurrency' not in incident['value_chain']['cash-out']['variety']:
                    incident['value_chain']['cash-out']['variety'].append("Cryptocurrency")
                    add_value_chain = True
                if add_value_chain:
                    add_any_value_chain = True
                    notes = incident['value_chain']['cash-out'].get('notes', "")
                    incident['value_chain']['cash-out']['notes'] = (notes + "\n" + "VERIS 1.3.6: value_chain.development.variety.Cryptocurrency added because action.malware.variety.Ransomware exists.").strip()
### This is a recommend only rule.
#            if 'Trojan' in incident['action'].get('malware', {}).get('variety', []):
#               add_value_chain = False
#                if 'value_chain' not in incident:
#                    incident['value_chain'] = {'development': {'variety': ['Trojan']}}
#                    add_value_chain = True
#                elif 'development' not in incident['value_chain']:
#                    incident['value_chain']['development'] = {'variety': ['Trojan']}
#                    add_value_chain = True
#                elif 'variety' not in incident['value_chain']['development']:
#                    incident['value_chain']['development']['variety'] = ['Trojan']
#                    add_value_chain = True
#                elif 'Trojan' not in incident['value_chain']['development']['variety']:
#                    incident['value_chain']['development']['variety'].append("Trojan")
#                    add_value_chain = True
#                if add_value_chain:
#                    notes = incident['value_chain']['development'].get('notes', "")
#                    incident['value_chain']['development']['notes'] = (notes + "\n" + "VERIS 1.3.6: value_chain.development.variety.Trojan added because action.malware.variety.Trojan exists.").strip()
            if 'Email' in incident['action'].get('social', {}).get('vector', []):
                add_value_chain = False
                if 'value_chain' not in incident:
                    incident['value_chain'] = {'distribution': {'variety': ['Email']}}
                    add_value_chain = True
                elif 'distribution' not in incident['value_chain']:
                    incident['value_chain']['distribution'] = {'variety': ['Email']}
                    add_value_chain = True
                elif 'variety' not in incident['value_chain']['distribution']:
                    incident['value_chain']['distribution']['variety'] = ['Email']
                    add_value_chain = True
                elif 'Email' not in incident['value_chain']['distribution']['variety']:
                    incident['value_chain']['distribution']['variety'].append("Email")
                    add_value_chain = True
                if add_value_chain:
                    add_any_value_chain = True
                    notes = incident['value_chain']['distribution'].get('notes', "")
                    incident['value_chain']['distribution']['notes'] = (notes + "\n" + "VERIS 1.3.6: value_chain.distribution.variety.Email added because action.social.vector.Email exists.").strip()
            if add_any_value_chain and incident.get('value_chain', {}).get('NA', False):
                if 'value_chain' not in incident:
                    incident['value_chain'] = {'NA': False}
                else:
                    incident['value_chain']['NA'] = False

            ### crosswalk hacking and malware actions
            ### VERIS issue #315
            if 'Footprinting' in incident.get('action', {}).get('hacking', {}).get('variety', []):
                incident['action']['hacking']['variety'].remove('Footprinting')
                incident['action']['hacking']['variety'].append('Profile host')
            if 'SQL injection' in incident.get('action', {}).get('malware', {}).get('variety', []):
                incident['action']['malware']['variety'].remove('SQL injection')
                malware_empty = True # because 'hacking.variety' may now be empty
                for field in ['variety']: # ["variety", "vector", "result"]: 
                    field_value = incident['action']['malware'].get(field, [])
                    if len(field_value) > 0 and field_value != ["Unknown"]:
                        malware_empty = False
                if 'hacking' not in incident['action']:
                    incident['action']['hacking'] = {'variety': ['SQLi'], "vector": ["Unknown"]}
                elif 'variety' not in incident['action']['hacking']:
                    incident['action']['hacking']['variety'] = ['SQLi']
                    if 'vector' not in incident['action']['hacking']:
                        incident['action']['hacking']['vector'] = ['Unknown']
                elif 'SQLi' not in incident['action']['hacking']['variety']:
                    incident['action']['hacking']['variety'].append("SQLi")
                if malware_empty:
                    _ = incident['action'].pop('malware') 
                    notes = incident['action']['hacking'].get('notes', "")
                    incident['action']['hacking']['notes'] = (notes + "\n" + "VERIS 1.3.6: Removed 'malware' section while moving malware.variety.SQL injection to hacking.variety.SQLi").strip()


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
        #config.readfp(open(args["conf"]))
        with open(args['conf'], 'r') as filehandle:
            config.readfp(filehandle)
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

