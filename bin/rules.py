#!/usr/bin/env python
"""
 AUTHOR: Gabriel Bassett
 DATE: 06-09-16
 DEPENDENCIES: <a list of modules requiring installation>
 

 DESCRIPTION:
 Meant to be imported.  Takes json records and adds rules for correlated enumerations.
 that may have been left out of the original source file.

 NOTES:
 <No Notes>

 ISSUES:
 <No Issues>

 TODO:
 <No TODO>

"""
# PRE-USER SETUP
import logging

########### NOT USER EDITABLE ABOVE THIS POINT #################


# USER VARIABLES
LOGLEVEL = logging.DEBUG
LOG = None

########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import ConfigParser
import os
import json


## SETUP
__author__ = "Gabriel Bassett"
# Default Configuration Settings
cfg = {
    'log_level': 'warning',
    'log_file': None,
    'schemafile': "../vcdb/veris.json",
    'enumfile': "../vcdb/veris-enum.json",
    'vcdb':False,
    'version':"1.3",
    'countryfile':'all.json',
    'output': None,
    'quiet': False,
    'repositories': ""
}
#logger = multiprocessing.get_logger()
logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG,
                 50: logging.CRITICAL, 40: logging.ERROR, 30: logging.WARNING, 20: logging.INFO, 10: logging.DEBUG, 0: logging.CRITICAL}
FORMAT = '%(asctime)19s - %(processName)s {0} - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT.format(""), datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger()

## FUNCTION DEFINITION
def addRules(incident):
    iid = incident["incident_id"]
    inRow = incident["plus"]["row_number"]
    # Takes in an incident and applies rules for internal consistency and consistency with previous incidents


    # Malware always has an integrity attribute
    if 'malware' in incident['action']:
        if 'attribute' not in incident:
            logger.info("%s: Added attribute.integrity since malware was involved.",iid)
            incident['attribute'] = {}
        if 'integrity' not in incident['attribute']:
            logger.info("%s: Added integrity since it has a malware action.",iid)
            incident['attribute']['integrity'] = {}
        if 'variety' not in incident['attribute']['integrity']:
            logger.info("%s: Added integrity.variety array since it didn't have one.",iid)
            incident['attribute']['integrity']['variety'] = []
        if 'Software installation' not in incident['attribute']['integrity']['variety']:
            logger.info("%s: Added software installation to attribute.integrity.variety since malware was involved.",iid)
            incident['attribute']['integrity']['variety'].append('Software installation')

    # Social engineering alters human behavior
    if 'social' in incident['action']:
        if 'attribute' not in incident:
            logger.info("%s: Added attribute.integrity since social engineering was involved.",iid)
            incident['attribute'] = {}
            incident['attribute']['integrity'] = {}
        if 'integrity' not in incident['attribute']:
            logger.info("%s: Added attribute.integrity since social engineering was involved.",iid)
            incident['attribute']['integrity'] = {}
        if 'variety' not in incident['attribute']['integrity']:
            logger.info("%s: Added attribute.integrity.variety array since it wasn't there.",iid)
            incident['attribute']['integrity']['variety'] = []
        if 'Alter behavior' not in incident['attribute']['integrity']['variety']:
            logger.info("%s: Added alter behavior to attribute.integrity.variety since social engineering was involved.",iid)
            incident['attribute']['integrity']['variety'].append('Alter behavior')

    # The target of social engineering is one of the affected assets
    if 'social' in incident['action']:
        if 'target' not in incident['action']['social']:
            logger.info("%s: Added action.social.target since it wasn't there.",iid)
            incident['action']['social']['target'] = ['Unknown']
        if 'asset' not in incident:
            logger.info("%s: Added asset object since it wasn't there.",iid)
            incident['asset'] = {}
        if 'assets' not in incident['asset']:
            logger.info("%s: Added asset.assets list since it wasn't there.",iid)
            incident['asset']['assets'] = []
        asset_list = list()
        for each in incident['asset']['assets']:
            asset_list.append(each['variety'])
        for each in incident['action']['social']['target']:
            if each == "Unknown":
                if 'P - Unknown' not in asset_list:
                    logger.info("%s: Adding P - Unknown to asset list since there was social engineering.",iid)
                    incident['asset']['assets'].append({'variety':'P - Unknown'})
                    continue
            if 'P - '+each not in asset_list:
                if 'P - '+each != 'P - Unknown':
                    logger.info("%s: Adding P - %s to asset list since there was social engineering.",each,iid)
                    incident['asset']['assets'].append({'variety':'P - '+each})

    # If SQLi was involved then there needs to be misappropriation too
    if 'hacking' in incident['action']:
        if 'SQLi' in incident['action']['hacking']['variety']:
            if 'integrity' not in incident['attribute']:
                logger.info("%s: Adding attribute.integrity since SQLi was involved.",iid)
                incident['attribute']['integrity'] = {'variety': [] }
            if 'variety' not in incident['attribute']['integrity']:
                logger.info("%s: Adding attribute.integrity.variety array since it was omitted.",iid)
                incident['attribute']['integrity']['variety'] = []
            if 'Repurpose' not in incident['attribute']['integrity']['variety']:
                logger.info("%s: Adding repurpose since SQLi was there.",iid)
                incident['attribute']['integrity']['variety'].append('Repurpose')

    # If there is a theft or loss then there is an availability loss
    if 'physical' in incident['action']:
        if 'Theft' in incident['action']['physical']['variety']:
            if 'availability' not in incident['attribute']:
                logger.info("%s: Added attribute.availability since there was theft.",iid)
                incident['attribute']['availability'] = {'variety': ['Loss']}
            if 'Loss' not in incident['attribute']['availability']['variety']:
                logger.info("%s: Added Loss to attribute.availability.variety in respone %s since there was theft.",iid)
                incident['attribute']['availability']['variety'].append('Loss')
    if 'error' in incident['action']:
        if 'Loss' in incident['action']['error']['variety']:
            if 'availability' not in incident['attribute']:
                logger.info("%s: Added attribute.availability since there was theft.",iid)
                incident['attribute']['availability'] = {'variety': ['Loss']}
            if 'Loss' not in incident['attribute']['availability']['variety']:
                logger.info("%s: Added Loss to attribute.availability.variety in respone %s since there was theft.",iid)
                incident['attribute']['availability']['variety'].append('Loss')

    # Commented out as discussion is these should only be applied to SG short form-entered incidents
    '''
    # ATM/Gas/POS Skimmer shim rules.  From Marc/Jay 2/13/15.  Added by gbassett
    try:
        if 'Skimmer' in incident['action']['physical']['variety']:
            logger.info('Adding attribute.confidentiality.data.variety=Payment, '
                         'attribute.integrity.variety = Hardware tampering and '
                         'action.misuse.variety.Unapproved hardware')
            # ensure attribute, integrity, and variety exist and set them to hardware tampering
            if 'attribute' not in incident:
                incident['attribute'] = {'integrity':{'variety':['Hardware tampering']}}
            elif 'integrity' not in incident['attribute']:
                incident['attribute']['integrity'] = {'variety': ['Hardware tampering']}
            else:
                if 'Hardware tampering' not in incident['attribute']['integrity']['variety']:
                    incident['attribute']['integrity']['variety'].append('Hardware tampering')
            # ensure cofidentiality, data, and variety are in the incident and add 'payment' to the list
            if 'confidentiality' not in incident['attribute']:
                incident['attribute']['confidentiality'] = {'data': [{'variety': 'Payment'}]}
            elif 'data' not in incident['attribute']['confidentiality']:
                incident['attribute']['confidentiality']['data'] = [{'variety': 'Payment'}]
            else:
                if 'Payment'.lower().strip() not in [x['variety'].lower().strip() for x in incident['attribute']['confidentiality']['data']]:
                    incident['attribute']['confidentiality']['data'].append({'variety': 'Payment'})
            # ensure action, misuse, and variety are in the incident and add 'Unapproved hardware' to the list
            if 'action' not in incident:
                incident['action'] = {'misuse':{'variety':['Unapproved hardware']}}
            elif 'misuse' not in incident['action']:
                incident['action']['misuse'] = {'variety':['Unapproved hardware']}
            else:
                if 'Unapproved hardware' not in incident['action']['misuse']['variety']:
                    incident['action']['misuse']['variety'].append('Unapproved hardware')
    except KeyError:
        logger.info('act.physical.variety not set so Skimmer (ATM/gas station/PoS skimmer shim) rule ignored.')


    # Handheld Skimmer rules.  From Marc/Jay 2/13/15.  Added by gbassett
    try:
        if 'Possession abuse' in incident['action']['misuse']['variety']:
            logger.info('Adding attribute.confidentiality.data.variety=Payment, '
                         'asset.assets.variety = M - Payment card, and '
                         'action.misuse.variety.Unapproved hardware')
            # ensure asset, assets, and variety are in the dictionary and set it to M - Payment card as it is a string
            if 'asset' not in incident:
                incident['asset'] = {'assets': [{'variety': 'M - Payment card'}]}
            elif 'assets' not in incident['asset']:
                incident['asset']['assets'] = [{'variety': 'M - Payment card'}]
            else:
                if 'M - Payment card'.lower().strip() not in [x['variety'].lower().strip() for x in incident['asset']['assets']]:
                    incident['asset']['assets'].append({'variety': 'M - Payment card'})
            # ensure confidentiality, data, and variety are in the incident and add 'payment' to the list
            if 'attribute' not in incident:
                incident['attribute'] = {'confidentiality': {'data': [{'variety': 'Payment'}]}}
            elif 'confidentiality' not in incident['attribute']:
                incident['attribute']['confidentiality'] = {'data': [{'variety': 'Payment'}]}
            elif 'data' not in incident['attribute']['confidentiality']:
                incident['attribute']['confidentiality']['data'] = [{'variety': 'Payment'}]
            else:
                if 'Payment'.lower().strip() not in [x['variety'].lower().strip() for x in incident['attribute']['confidentiality']['data']]:
                    incident['attribute']['confidentiality']['data'].append({'variety': 'Payment'})
            # ensure action, misuse, and variety are in the incident and add 'Unapproved hardware' to the list
            if 'action' not in incident:
                incident['action'] = {'misuse':{'variety':['Unapproved hardware']}}
            elif 'misuse' not in incident['action']:
                incident['action']['misuse'] = {'variety':['Unapproved hardware']}
            else:
                if 'Unapproved hardware' not in incident['action']['misuse']['variety']:
                    incident['action']['misuse']['variety'].append('Unapproved hardware')
    except KeyError:
        logger.info('act.misuse.variety not set so Possession abuse (handheld skimmer) rule ignored.')
    '''

    # if the secondary victim has no additional information then add a note
    # about that.
    if 'secondary' in incident['victim'] and len(incident['victim'].get('secondary', {})) == 0:
      incident['victim']['secondary']['notes'] = "No additional information."
      logger.info("Secondary victim, but no additional info so adding victim.secondary.notes to document it.")

    # If the hacking vector was "web application", add S - Web Application to "asset.assets"
    if 'hacking' in incident['action'].keys() and "Web application" in incident['action']['hacking']['vector']:
        if 'asset' not in incident.keys():
            logger.info("Added asset object to response %s since it wasn't there.",iid)
            incident['asset'] = {}
        if 'assets' not in incident['asset'].keys():
            logger.info("Added asset.assets list to response %s since it wasn't there.",iid)
            incident['asset']['assets'] = []
        if "S - Web application" not in [d.get("variety", "") for d in incident['asset']['assets']]:
            logger.info("Added asset.assets.variety.S - Web application to action.hacking.vector.Web application incident for response {0}".format(iid))

    return incident


def makeValid(incident):
    iid = incident["incident_id"]
    inRow = incident["plus"]["row_number"]

    # Unknown victims have NAICS code of "000", not just one zero
    if incident['victim']['industry'].lower().strip("0") in ['0','unknown', ""]:
        incident['victim']['industry'] = "000"
        logger.info("replacing unknown victim.industry with '000' in {0}".format(iid))

    # KDT the script sometimes produces incidents with an asset array that has
    # no entries. I'm too lazy to figure out where that happens so I'll just
    # check for it here and fix it.
    if len(incident['asset']['assets']) < 1:
        incident['asset']['assets'].append({'variety':'Unknown'})
        logger.info("No asset varieties listed in {0} so adding asset.assets.variety.Unknown".format(iid))

    # make sure variety and vector are in actions and of correct length
    if 'action' not in incident:
        incident['action'] = { "Unknown" : {} }
        logger.info("No action so adding action.Unknown to {0}".format(iid))
    for action in ['hacking', 'malware', 'social', 'environmental', 'physical', 'misuse', 'error']:
        if action in incident['action'].keys():
            if 'variety' not in incident['action'][action].keys():
                incident['action'][action]['variety'] = []
            if len(incident['action'][action]['variety']) == 0:
                logger.info("Adding {0} variety to response {1} because it wasn't in there.".format(action, iid))
                incident['action'][action]['variety'].append("Unknown")
            if action != 'environmental' and 'vector' not in incident['action'][action].keys():
                incident['action'][action]['vector'] = []
            if  action != 'environmental' and len(incident['action'][action]['vector']) == 0:
                logger.info("Adding {0} vector to response {1} because it wasn't in there.".format(action, iid))
                incident['action'][action]['vector'].append("Unknown") 

    # if confidentiality then there should be something in the data array
    if 'confidentiality' in incident['attribute']:
        if 'data' not in incident['attribute']['confidentiality']:
            incident['attribute']['confidentiality']['data'] = []
        if len(incident['attribute']['confidentiality']['data']) == 0:
            logger.info("Adding attribute.confidentiality.data.variety:Unknown to {0} because attribute.confidentiality exists without data variety.".format(iid))
            incident['attribute']['confidentiality']['data'].append({'variety':'Unknown'})

    # if confidentiality was not affected then it shouldn't be in the plus
    # section either. Usually just has credit_monitoring unknown anyway.
    if 'confidentiality' not in incident['attribute'] and \
      incident['plus'].get('attribute', {}).keys() == ['confidentiality']:
        logger.info("attribute.confidentiality not in record so removing attribute from plus for record {0}.".format(iid))
        incident['plus'].pop('attribute')

    return incident


## MAIN LOOP EXECUTION
def main(cfg):
    if __name__ != "__main__":
        raise RuntimeError("Main should not be imported and run.  Instead run ''makeValid()' and 'addRules()'")

    logging.info('Beginning main loop.')
    formatter = logging.Formatter(FORMAT.format("- " + "/".join(cfg["input"].split("/")[-2:])))
    logger = logging.getLogger()
    ch = logging.StreamHandler()
    ch.setLevel(logging_remap[cfg["log_level"]])
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    if "log_file" in cfg and cfg["log_file"] is not None:
        fh = logging.FileHandler(cfg["log_file"])
        fh.setLevel(logging_remap[cfg["log_level"]])
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # get all files in directory and sub-directories
    if os.path.isfile(cfg['input']):
        filenames = [cfg['input']]
    elif os.path.isdir(cfg['input']):
        # http://stackoverflow.com/questions/14798220/how-can-i-search-sub-folders-using-glob-glob-module-in-python
        filenames = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(cfg['input'])
            for f in files if f.endswith(".json")]
    else:
        raise OSError("File or directory {0} does not exist.".format(cfg['input']))

    # open each json file
    if 'output' in cfg and cfg['output'] is not None:
        overwrite = False
    else:
        overwrite = True
    for filename in filenames:
        with open(filename, 'rw') as filehandle:
            try:
                incident = json.load(filehandle)
            except:
                logger.warning("Unable to load {0}.".format(filename))
                continue
            # add 'unknowns' as appropriate
            incident = makeValid(incident)
            # add rules
            incident = addRules(incident)
            # save it back out
            if overwrite:
                json.dump(incident, filehandle)
            else:
                with open(cfg['output'].rstrip("/") + "/" + filename.split("/")[-1], 'w') as outfilehandle:
                    json.dump(incident, outfilehandle, indent=2, sort_keys=True)


    logging.info('Ending main loop.')

if __name__ == "__main__":

    ## Gabe
    ## The general Apprach to config parsing (Probably not the best way)
    ## 1. create a dictionary called 'cfg' of fallback values (up at the top of the file)
    ## 2. parse the arguments (args) and turn into a dictionary if the value is not None
    ## 3. Use the config from the command line parser to read the config file and update the 'cfg' dictionary
    ## 4. Update the cfg dictionary with the arguements (args) from the command line

    parser = argparse.ArgumentParser(description="This script takes a directory of VERIS json, fixes missing values and adds logical rules. " +
                                                 "to each json file.")
    parser.add_argument("-i", "--input", required=True, help="The json file or directory")
    parser.add_argument("-o", "--output", help="directory where json files will be written")
    #parser.add_argument("--veris", required=False, help="The location of the veris_scripts repository.")
    #parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    #parser.add_argument('--log_file', help='Location of log file')
    #parser.add_argument("--dbir-private", required=False, help="The location of the dbirR repository.")
    #parser.add_argument("-s","--schemafile", help="The JSON schema file")
    #parser.add_argument("-e","--enumfile", help="The JSON file with VERIS enumerations")
    #parser.add_argument("--vcdb",help="Convert the data for use in VCDB",action="store_true")
    #parser.add_argument("--version", help="The version of veris in use")
    parser.add_argument('--conf', help='The location of the config file', default="./_checkValidity.cfg")
    #parser.add_argument('--year', help='The DBIR year to assign tot he records.')
    #parser.add_argument('--countryfile', help='The json file holdering the country mapping.')
    #parser.add_argument('--source', help="Source_id to use for the incidents. Partner pseudonym.")
    #parser.add_argument("-f", "--force_analyst", help="Override default analyst with --analyst.", action='store_true')
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}

    # Parse the config file
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(args["conf"]))
        cfg_key = {
            'GENERAL': ['input', 'output'] #, 'dbirR', 'veris_scripts'],
#            'LOGGING': ['level', 'log_file'],
 #           'VERIS': ['version', 'schemafile', 'enumfile', 'vcdb', 'year', 'countryfile']
        }
        for section in cfg_key.keys():
            if config.has_section(section):
                for value in cfg_key[section]:
                    if value.lower() in config.options(section):
                        cfg[value] = config.get(section, value)
#        if "year" in cfg:
#            cfg["year"] = int(cfg["year"])
#        else:
#            cfg["year"] = int(datetime.now().year)
#        cfg["vcdb"] = {True:True, False:False, "false":False, "true":True}[cfg["vcdb"].lower()]
        logger.debug("config import succeeded.")
    except Exception as e:
        logger.warning("config import failed with error {0}.".format(e))
        #raise e
        pass

    cfg.update(args)


    logger.setLevel(logging_remap[cfg["log_level"]])
    #logger.basicConfig(level=logging_remap[cfg["log_level"]],
    #      format='%(asctime)19s %(levelname)8s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    if cfg["log_file"] is not None:
        logger.filename = cfg["log_file"]

    logger.debug(args)
    logger.debug(cfg)

    main(cfg)
