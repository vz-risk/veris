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
import imp
import os
import sys
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    logging.debug("Script dir: {0}.".format(script_dir))
    print("Script dir: {0}.".format(script_dir))
    raise
#import veris_logger

########### NOT USER EDITABLE ABOVE THIS POINT #################


# USER VARIABLES
#LOGLEVEL = logging.DEBUG
#LOG = None

########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import ConfigParser
import os
import json
from datetime import datetime, date
from distutils.version import LooseVersion
from tqdm import tqdm
from pprint import pprint, pformat


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
    'repositories': "",
    'force_analyst': False,
    'year': date.today().year
}
#logger = multiprocessing.get_logger()
#logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG,
#                 50: logging.CRITICAL, 40: logging.ERROR, 30: logging.WARNING, 20: logging.INFO, 10: logging.DEBUG, 0: logging.CRITICAL}
#FORMAT = '%(asctime)19s - %(processName)s {0} - %(levelname)s - %(message)s'
#logging.basicConfig(level=logging.INFO, format=FORMAT.format(""), datefmt='%m/%d/%Y %H:%M:%S')
#logger = logging.getLogger()

## FUNCTION DEFINITION

### Functionality redundant with check in schema - gdb 061516
#def checkIndustry(label, industry):
#    if not industry.isdigit() and not industry in [ "31-33", "44-45", "48-49" ]:
#        logger.warning("%s: %s is not numbers: \"%s\"", iid, label, industry)
#        # retString.append("must be numbers or one of 31-33, 44-45, 48-49")

### Functionality redundant with checkValidity.py - gdb 061516
#def compareFromTo(label, fromArray, toArray):
#    if isinstance(fromArray, basestring):
#        if fromArray not in toArray:
#            logger.warning("%s: %s has invalid enumeration: \"%s\"", iid, label, fromArray)
#    else:
#        if len(fromArray) == 0:
#            logger.warning("%s: %s has no values in enumeration", iid, label)
#        for item in fromArray:
#            if item not in toArray:
#                logger.warning("%s: %s has invalid enumeration: \"%s\"", iid, label, iter_logger.updateLogger(cfg)m

class Rules():
    cfg = None
    country_region = None
    ctry_to_alpha2 = None

    def __init__(self, cfg):
        veris_logger.updateLogger(cfg)
        logging.debug("Initializing Rules object.")

        self.country_region, self.ctry_to_alpha2 = self.getCountryCode(cfg["countryfile"])
        #countryData = json.loads(open(cfg["countryfile"]).read())  # unused in current parsing.  Should replace self.self.getCountryCode() for consistency. gdb 1/10
        #countryList = [e['alpha-2'] for e in countryData]  # unused in current parsing.  Should replace self.self.getCountryCode() for consistency. gdb 1/10

        self.cfg = cfg


    # Function to parse the country file (all.json) to the two dictionaries used.
    def getCountryCode(self, country_file):
        ctry_to_alpha2 = {}
        if type(country_file) == list:
            country_codes = country_file
        else:
            country_codes = json.loads(open(country_file).read())
        country_code_remap = {'Unknown': '000000', 'Other': '000000'}
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
            try:
                ctry_to_alpha2[eachCountry['name'].upper()] = eachCountry['alpha-2'].upper()
            except:
                pass
        return country_code_remap, ctry_to_alpha2


    #def compareCountryFromTo(label, fromArray, toArray):
    def compareCountryFromTo(self, label, fromArray, iid):
        #if isinstance(fromArray, basestring):
        #    if fromArray not in toArray:
        #        logger.warning("%s: %s has invalid enumeration[1]: \"%s\"", iid, label, fromArray)
        #else:
        if len(fromArray) == 0:
            logging.warning("%s: %s has no values in enumeration", iid, label)
        for idx, item in enumerate(fromArray):
    #        if item not in toArray:
            if item.upper() == "USA":
                logging.warning("%s: %s was set to 'USA', converting to 'US'", iid, label)
                fromArray[idx] = "US"
            elif item.upper() == "UK":
                logging.warning("%s: %s was set to 'UK', converting to 'GB'", iid, label)
                fromArray[idx] = "GB"
    #        else:
    #            fromArray[idx] = "Unknown"
    #            logger.warning("%s: %s has invalid enumeration[2]: \"%s\", converting to 'Unknown'", iid, label, item)
        if type(fromArray) == "str":
            fromArray = [ fromArray ]
        return(fromArray)


    def addRules(self, incident, cfg=None):
        if cfg == None:
            cfg = self.cfg

        if "master_id" in incident.get("plus", {}):
            iid = incident['plus']['master_id']
        else:
            iid = incident["incident_id"]
        logging.info("Beginning addRules for incident {0}.".format(iid))
        #inRow = incident["plus"]["row_number"]  # not used and conflicts with versions lower than 1.3. Could test for version > 1.3 and then include... - gdb 7/11/16
        # Takes in an incident and applies rules for internal consistency and consistency with previous incidents

        # The schema should have an import year
        #checkEnum(outjson, jenums, country_region, cfg)
        if incident.get('plus', {}).get('dbir_year', None) is None and cfg['vcdb'] != True:
            logging.warning("{0}: missing plus.dbir_year, auto-filled {1}".format(iid, int(cfg["year"])))
            incident['plus']['dbir_year'] = int(cfg["year"])
        if ('source_id' not in incident or cfg["force_analyst"]) and 'source' in cfg:
            incident['source_id'] = cfg['source']


        # Malware always has an integrity attribute
        if 'malware' in incident['action']:
            if 'attribute' not in incident:
                logging.info("%s: Added attribute since malware was involved implying 'attribute.integrity' should exist.",iid)
                incident['attribute'] = {}
            if 'integrity' not in incident['attribute']:
                logging.info("%s: Added attribute.integrity since it has a malware action.",iid)
                incident['attribute']['integrity'] = {}
            if 'variety' not in incident['attribute']['integrity']:
                logging.info("%s: Added integrity.variety array since it didn't have one.",iid)
                incident['attribute']['integrity']['variety'] = []
            if 'Software installation' not in incident['attribute']['integrity']['variety']:
                logging.info("%s: Added software installation to attribute.integrity.variety since malware was involved.",iid)
                incident['attribute']['integrity']['variety'].append('Software installation')


        # 'state' has 'stored', 'stored encrypted', and 'stored unencrypted'. That is an internal hierarchy. that should be documented and handled. 
        # Per vz-risk/veris #195
        if 'confidentiality' in incident['attribute']:
            if ('Stored encrypted' in incident['attribute']['confidentiality'].get('variety', []) or \
                'Stored unencrypted' in incident['attribute']['confidentiality'].get('variety', [])) and \
               'Stored' not in incident['attribute']['confidentiality'].get('variety', []):
                incident['attribute']['confidentiality']['variety'].append('Stored')


        ### Hierarchical Field
        # action.malware.variety.Click fraud and cryptocurrency mining is a parent of action.malware.variety.Click fraud and action.malware.variety.Cryptocurrency mining
        # per vz-risk/VERIS issue #203
        if 'malware' in incident['action']:
            if ('Click fraud' in incident['action']['malware'].get('variety', []) or \
                'Cryptocurrency mining' in incident['action']['malware'].get('variety', [])) and \
               'Click fraud and cryptocurrency mining' not in incident['action']['malware'].get('variety', []):
                incident['action']['malware']['variety'].append('Click fraud and cryptocurrency mining')


        ### Hierarchical Field
        ### Add hacking.exploit vuln and malware.exploit vuln hierarchy
        ## Issue VERIS # 192
        exploit_varieties = ["Abuse of functionality", 
                   "Buffer overflow", "Cache poisoning", 
                   "Cryptanalysis", "CSRF", 
                   "Forced browsing", "Format string attack", 
                   "Fuzz testing", "HTTP request smuggling", 
                   "HTTP request splitting", "HTTP response smuggling", 
                   "HTTP Response Splitting", "Integer overflows", 
                   "LDAP injection", "Mail command injection", 
                   "MitM", "Null byte injection", 
                   "OS commanding", 
                   "Other", 
                   "Path traversal", "Reverse engineering", 
                   "RFI", "Routing detour", 
                   "Session fixation", "Session prediction", 
                   "Session replay", "Soap array abuse", 
                   "Special element injection", "SQLi", 
                   "SSI injection",
                   "URL redirector abuse",  
                   "Virtual machine escape", 
                   "XML attribute blowup", "XML entity expansion", 
                   "XML external entities", "XML injection", 
                   "XPath injection", "XQuery injection", 
                   "XSS"]
        if 'variety' in incident['action'].get('hacking', {}):
            if "Exploit vuln" not in incident['hacking']['variety'] and len(set(incident['hacking']['variety']).intersect(hak_exploit_varieties)) > 0:
                incident['hacking']['variety'].append('Exploit vuln') 
        mal_exploit_varieties = ["Remote injection", "Web drive-by"]
        if 'variety' in incident['action'].get('malware', {}):
            if "Exploit vuln" not in incident['malware']['variety'] and len(set(incident['malware']['variety']).intersect(mal_exploit_varieties)) > 0:
                incident['malware']['variety'].append('Exploit vuln') 


        # Social engineering alters human behavior
        if 'social' in incident['action']:
            if 'attribute' not in incident:
                logging.info("%s: Added attribute.integrity since social engineering was involved.",iid)
                incident['attribute'] = {}
                incident['attribute']['integrity'] = {}
            if 'integrity' not in incident['attribute']:
                logging.info("%s: Added attribute.integrity since social engineering was involved.",iid)
                incident['attribute']['integrity'] = {}
            if 'variety' not in incident['attribute']['integrity']:
                logging.info("%s: Added attribute.integrity.variety array since it wasn't there.",iid)
                incident['attribute']['integrity']['variety'] = []
            if 'Alter behavior' not in incident['attribute']['integrity']['variety']:
                logging.info("%s: Added alter behavior to attribute.integrity.variety since social engineering was involved.",iid)
                incident['attribute']['integrity']['variety'].append('Alter behavior')



        # The target of social engineering is one of the affected assets
        if 'social' in incident['action']:
            if 'target' not in incident['action']['social']:
                logging.info("%s: Added action.social.target since it wasn't there.",iid)
                incident['action']['social']['target'] = ['Unknown']
            if 'asset' not in incident:
                logging.info("%s: Added asset object since it wasn't there.",iid)
                incident['asset'] = {}
            if 'assets' not in incident['asset']:
                logging.info("%s: Added asset.assets list since it wasn't there.",iid)
                incident['asset']['assets'] = []
            asset_list = list()
            for each in incident['asset']['assets']:
                asset_list.append(each['variety'])
            for each in incident['action']['social']['target']:
                if LooseVersion(incident['schema_version']) > LooseVersion("1.3"):
                    logging.debug("Version {0} greater than 1.3.".format(incident['schema_version']))
                    if 'P - '+each not in asset_list:
                        logging.info("{1}: Adding P - {0} to asset list since there was social engineering.".format(each,iid))
                        incident['asset']['assets'].append({'variety':'P - '+each})
                else:
                    if each == "Unknown":
                        if 'P - Other' not in asset_list:
                            logging.info("%s: Adding P - Other to asset list since there was social engineering.",iid)
                            incident['asset']['assets'].append({'variety':'P - Other'})
                            continue
                    if 'P - '+each not in asset_list:
                        if 'P - '+each not in  ['P - Other', 'P - Unknown']:
                            logging.info("{1}: Adding P - {0} to asset list since there was social engineering.".format(each,iid))
                            incident['asset']['assets'].append({'variety':'P - '+each})


        # If SQLi was involved then there needs to be misappropriation too
        if 'hacking' in incident['action']:
            if 'SQLi' in incident['action']['hacking']['variety']:
                if 'integrity' not in incident['attribute']:
                    logging.info("%s: Adding attribute.integrity since SQLi was involved.",iid)
                    incident['attribute']['integrity'] = {'variety': [] }
                if 'variety' not in incident['attribute']['integrity']:
                    logging.info("%s: Adding attribute.integrity.variety array since it was omitted.",iid)
                    incident['attribute']['integrity']['variety'] = []
                if 'Repurpose' not in incident['attribute']['integrity']['variety']:
                    logging.info("%s: Adding repurpose since SQLi was there.",iid)
                    incident['attribute']['integrity']['variety'].append('Repurpose')


        # If there is a theft or loss then there is an availability loss
        if 'physical' in incident['action']:
            if 'Theft' in incident['action']['physical']['variety']:
                if 'availability' not in incident['attribute']:
                    logging.info("%s: Added attribute.availability since there was theft.",iid)
                    incident['attribute']['availability'] = {'variety': ['Loss']}
                if 'Loss' not in incident['attribute']['availability']['variety']:
                    logging.info("%s: Added Loss to attribute.availability.variety in respone %s since there was theft.",iid)
                    incident['attribute']['availability']['variety'].append('Loss')
        if 'error' in incident['action']:
            if 'Loss' in incident['action']['error']['variety']:
                if 'availability' not in incident['attribute']:
                    logging.info("%s: Added attribute.availability since there was theft.",iid)
                    incident['attribute']['availability'] = {'variety': ['Loss']}
                if 'Loss' not in incident['attribute']['availability']['variety']:
                    logging.info("%s: Added Loss to attribute.availability.variety in respone %s since there was theft.",iid)
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
          logging.info("Secondary victim, but no additional info so adding victim.secondary.notes to document it.")

        # If the hacking vector was "web application", add S - Web Application to "asset.assets"
        if 'hacking' in incident['action'].keys() and "Web application" in incident['action']['hacking']['vector']:
            if 'asset' not in incident.keys():
                logging.info("Added asset object to response %s since it wasn't there.",iid)
                incident['asset'] = {}
            if 'assets' not in incident['asset'].keys():
                logging.info("Added asset.assets list to response %s since it wasn't there.",iid)
                incident['asset']['assets'] = []
            if "S - Web application" not in [d.get("variety", "") for d in incident['asset']['assets']]:
                logging.info("Added asset.assets.variety.S - Web application to action.hacking.vector.Web application incident for response {0}".format(iid))


        # If a country exists, make sure the region exists in the regions list - GDB 180724
        # from issue https://github.com/vz-risk/veris/issues/194
        # for victim
        for eachCountry in incident['victim'].get('country', []):
            incident['victim']['region'] = incident['victim'].get('region', []) + [self.country_region[eachCountry]]
        if 'region' in incident['victim'].keys():
            incident['victim']['region'] = list(set(incident['victim']['region'])) # remove duplicates
            # if a region exists but no country, country will be filled in 'unknown'
            # the 'unknown' country value will cause '000000' to be filled into the region
            # we want to remove the '000000' if another region exists
            if len(incident['victim']['region']) > 1 and '000000' in incident['victim']['region']:
                incident['victim']['region'].remove('000000') 
        # for actor.external
        if 'external' in incident['actor']:
            for eachCountry in incident['actor']['external'].get('country', []):
                incident['actor']['external']['region'] = incident['actor']['external'].get('region', []) + [self.country_region[eachCountry]]
            if 'region' in incident['victim'].keys():
                incident['actor']['external']['region'] = list(set(incident['actor']['external']['region'])) # remove duplicates
                # if a region exists but no country, country will be filled in 'unknown'
                # the 'unknown' country value will cause '000000' to be filled into the region
                # we want to remove the '000000' if another region exists
                if len(incident['actor']['external']['region']) > 1 and '000000' in incident['actor']['external']['region']:
                    incident['actor']['external']['region'].remove('000000') 
        # for actor.partner
        if 'partner' in incident['actor']:
            for eachCountry in incident['actor']['partner'].get('country', []):
                incident['actor']['partner']['region'] = incident['actor']['external'].get('partner', []) + [self.country_region[eachCountry]]
            if 'region' in ['actor']['partner'].keys():
                incident['actor']['partner']['region'] = list(set(incident['actor']['partner']['region'])) # remove duplicates
                # if a region exists but no country, country will be filled in 'unknown'
                # the 'unknown' country value will cause '000000' to be filled into the region
                # we want to remove the '000000' if another region exists
                if len(incident['actor']['partner']['region']) > 1 and '000000' in incident['actor']['partner']['region']:
                    incident['actor']['partner']['region'].remove('000000') 

        return incident


    def makeValid(self, incident, cfg=None):
        if cfg == None:
            cfg = self.cfg

        iid = incident["incident_id"]
        logging.info("Beginning makeValid for incident_id {0}, master_id {1}.".format(iid, incident.get('plus', {}).get('master_id', "NO MASTER ID")))
        #inRow = incident["plus"]["row_number"]   # not used and conflicts with versions lower than 1.3. Could test for version > 1.3 and then include... - gdb 7/11/16

        #with open(cfg['schemafile'], "r") as filehandle:
        #    schema = json.load(filehandle)

        ### Rules from import std_excel
        # Removed comparisons to schema as those happen in checkValidity.py -gdb 061516
    #def checkEnum(incident, schema, country_region, cfg=cfg):
        ## INCIDENT ##
        if 'security_incident' not in incident:
            logging.warning("%s: security_incident not found (required)", iid)
        #else:
        #    compareFromTo('security_incident', incident['security_incident'], schema['security_incident'])
        if 'master_id' not in incident['plus']:
            if 'incident_id' in incident:
                master_id = incident['incident_id']
            else:
                master_id = "notblank"
            logging.info("%s: auto-filling plus.master_id to %s", iid, master_id)
            incident['plus']['master_id'] = master_id

        ## VICTIM ##
        if 'victim' not in incident:
            logging.info("%s: auto-filled Unknown for victim section", iid)
            incident['victim'] = { 'employee_count' : 'Unknown', 'industry':"000", 'country': [ "Unknown" ], 'notes':'auto-filled Unknown' }
        victim = incident['victim']
        if 'employee_count' not in victim:
            logging.info("%s: auto-filled Unknown for victim.employee_count", iid)
            victim['employee_count'] = "Unknown"
        #compareFromTo('victim.employee_count', victim['employee_count'], schema['victim']['employee_count'])
        if 'industry' not in victim:
            logging.info("%s: auto-filled Unknown for victim.industry", iid)
            victim['industry'] = "000"
        #checkIndustry('victim.industry', victim['industry'])  # redundant with schema check. -gdb 061516

        if 'country' not in victim:
            logging.info("%s: auto-filled Unknown for victim.country", iid)
            victim['country'] = [ "Unknown" ]

        # Unknown victims have NAICS code of "000", not just one zero
        if incident['victim']['industry'].lower().strip("0") in ['0','unknown', ""]:
            incident['victim']['industry'] = "000"
            logging.info("replacing unknown victim.industry with '000' in {0}".format(iid))

        # CC
        victim['country'] = self.compareCountryFromTo('victim.country', victim['country'], iid) #, schema['victim']['country'])

        ## ACTOR ##
        if 'actor' not in incident:
            logging.info("%s: auto-filled Unknown for entire actor section", iid)
            incident['actor'] = { 'unknown' : { 'notes':'auto-filled Unknown' } }
        if 'external' in incident['actor']:
            actor = incident['actor']['external']
            if 'motive' not in actor:
                logging.info("%s: auto-filled Unknown for actor.external.motive", iid)
                actor['motive'] = [ "Unknown" ]
            if len(actor['motive']) == 0:
                logging.info("%s: auto-filled Unknown for empty array in actor.external.motive", iid)
                actor['motive'] = [ "Unknown" ]
            #compareFromTo('actor.external.motive', actor['motive'], schema['actor']['external']['motive'])
            if 'variety' not in actor:
                logging.info("%s: auto-filled Unknown for actor.external.variety", iid)
                actor['variety'] = [ "Unknown" ]
            if len(actor['variety']) == 0:
                logging.info("%s: auto-filled Unknown for empty array in actor.external.variety", iid)
                actor['variety'] = [ "Unknown" ]
            #compareFromTo('actor.external.variety', actor['variety'], schema['actor']['external']['variety'])

            if 'country' in actor:
                if len(actor['country']) == 0:
                    logging.info("%s: auto-filled Unknown for empty array in actor.external.country", iid)
                    actor['country'] = [ "Unknown" ]
                #else:
                    # only add region if it doesn't exist at all in the incident.
                    # if 'external_region' not in incident['plus']:
                    #     logger.info("%s: auto-filled plus.external_region from the actor.external.country", iid)
                    #     incident['plus']['external_region'] = [ country_region[c] for c in actor['country'] ]
                    # elif len(incident['plus']['external_region']) < len(actor['country']):
                    #     logger.info("%s: auto-filled plus.external_region from the actor.external.country (len region < actor.country", iid)
                    #     incident['plus']['external_region'] = [ country_region[c] for c in actor['country'] ]
            else:
                logging.info("%s: auto-filled Unknown for actor.external.country", iid)
                actor['country'] = [ "Unknown" ]

            #if 'plus' not in incident:  # check already exists below. -gdb 061516
            #    incident['plus'] = {}
            ## CC
            actor['country'] = self.compareCountryFromTo('actor.external.country', actor['country'], iid) #, schema['actor']['external']['country'])

            incident['actor']['external'] = actor

        if 'internal' in incident['actor']:
            actor = incident['actor']['internal']
            if 'motive' not in actor:
                logging.info("%s: auto-filled Unknown for actor.internal.motive", iid)
                actor['motive'] = [ "Unknown" ]
            if len(actor['motive']) == 0:
                logging.info("%s: auto-filled Unknown for empty array in actor.internal.motive", iid)
                actor['motive'] = [ "Unknown" ]
            #compareFromTo('actor.internal.motive', actor['motive'], schema['actor']['internal']['motive'])
            if 'variety' not in actor:
                logging.info("%s: auto-filled Unknown for actor.internal.variety", iid)
                actor['variety'] = [ "Unknown" ]
            if len(actor['variety']) == 0:
                logging.info("%s: auto-filled Unknown for empty array in actor.internal.variety", iid)
                actor['variety'] = [ "Unknown" ]
            #compareFromTo('actor.internal.variety', actor['variety'], schema['actor']['internal']['variety'])
            if "job_change" in actor and type(actor['job_change']) in (str, unicode):
                logging.info("{0}: changing job_change from a string to an array to fit the schema.".format(iid))
                actor['job_change'] = actor['job_change'].split(",")
            incident['actor']['internal'] = actor
        if 'partner' in incident['actor']:
            actor = incident['actor']['partner']
            if 'motive' not in actor:
                logging.info("%s: auto-filled Unknown for actor.partner.motive", iid)
                actor['motive'] = [ "Unknown" ]
            if len(actor['motive']) == 0:
                logging.info("%s: auto-filled Unknown for empty array in actor.partner.motive", iid)
                actor['motive'] = [ "Unknown" ]
            #compareFromTo('actor.partner.motive', actor['motive'], schema['actor']['partner']['motive'])
            if 'country' not in actor:
                logging.info("%s: auto-filled Unknown for actor.partner.country", iid)
                actor['country'] = [ "Unknown" ]
            if len(actor['country']) == 0:
                logging.info("%s: auto-filled Unknown for empty array in actor.partner.country", iid)
                actor['country'] = [ "Unknown" ]
            # compareFromTo('actor.partner.variety', actor['variety'], schema['actor']['partner']['country'])


            # CC
            actor['country'] = self.compareCountryFromTo('actor.partner.country', actor['country'], iid) #, schema['actor']['partner']['country'])


            if 'industry' not in actor:
                logging.info("%s: auto-filled Unknown for actor.partner.industry", iid)
                actor['industry'] = "000"
            #checkIndustry('actor.partner.industry', actor['industry'])
            incident['actor']['partner'] = actor

        ## ACTION ##
        if 'action' not in incident:
            logging.info("%s: auto-filled Unknown for entire action section", iid)
            incident['action'] = { "unknown" : { "notes" : "auto-filled Unknown" } }

        for action in ['malware', 'hacking', 'social', 'misuse', 'physical', 'error']:
            if action in incident['action']:
                for method in ['variety', 'vector']:
                    if method not in incident['action'][action]:
                        logging.info("%s: auto-filled Unknown for action.%s.%s", iid, action, method)
                        incident['action'][action][method] = [ 'Unknown' ]
                    if len(incident['action'][action][method]) == 0:
                        logging.info("%s: auto-filled Unknown for empty array in action.%s.%s", iid, action, method)
                        incident['action'][action][method] = [ 'Unknown' ]
                    #astring = 'action.' + action + '.' + method
                    #compareFromTo(astring, incident['action'][action][method], schema['action'][action][method])
                if action == "physical":
                    method = "vector"
                    if method not in incident['action'][action]:
                        logging.info("%s: auto-filled Unknown for action.%s.%s", iid, action, method)
                        incident['action'][action][method] = [ 'Unknown' ]
                    if len(incident['action'][action][method]) == 0:
                        logging.info("%s: auto-filled Unknown for empty array in action.%s.%s", iid, action, method)
                        incident['action'][action][method] = [ 'Unknown' ]
                    #astring = 'action.' + action + '.' + method
                    #compareFromTo(astring, incident['action'][action][method], schema['action'][action][method])
                if action == "social":
                    method = "target"
                    if method not in incident['action'][action]:
                        logging.info("%s: auto-filled Unknown for action.%s.%s", iid, action, method)
                        incident['action'][action][method] = [ 'Unknown' ]
                    if len(incident['action'][action][method]) == 0:
                        logging.info("%s: auto-filled Unknown for empty array in action.%s.%s", iid, action, method)
                        incident['action'][action][method] = [ 'Unknown' ]
                    #astring = 'action.' + action + '.' + method
                    #compareFromTo(astring, incident['action'][action][method], schema['action'][action][method])
        action = 'environmental'
        if action in incident['action']:
            method = "variety"
            if method not in incident['action'][action]:
                logging.info("%s: auto-filled Unknown for action.%s.%s", iid, action, method)
                incident['action'][action][method] = [ 'Unknown' ]
            if len(incident['action'][action][method]) == 0:
                logging.info("%s: auto-filled Unknown for empty array in action.%s.%s", iid, action, method)
                incident['action'][action][method] = [ 'Unknown' ]
            #astring = 'action.' + action + '.' + method
            #compareFromTo(astring, incident['action'][action][method], schema['action'][action][method])

        ## ASSET ##
        if 'asset' not in incident:
            logging.info("%s: auto-filled Unknown for entire asset section", iid)
            incident['asset'] = { "assets" : [ { "variety" : "Unknown" } ] }
        if 'assets' not in incident['asset']:
            logging.info("%s: auto-filled Unknown for asset.asseets section", iid)
            incident['asset']['assets'] = [ { "variety" : "Unknown" } ]
        for index, asset in enumerate(incident['asset']['assets']):
            if 'variety' not in asset:
                logging.info("%s: auto-filled Unknown for asset.asseets.variety ", iid)
                asset['variety'] = "Unknown"
            #compareFromTo('asset.assets.' + str(index) + '.variety', asset['variety'], schema['asset']['assets']['variety'])
        #for method in ["cloud", "accessibility", "ownership", "management", "hosting"]:
            #if method in incident:
                #compareFromTo('asset.'+method, incident['asset'][method], schema['asset'][method])

        ## ATTRIBUTE ##
        if 'attribute' not in incident:
            logging.info("%s: no attribute section is found (not required)", iid)
        else:
            if 'confidentiality' in incident['attribute']:
                if 'data' not in incident['attribute']['confidentiality']:
                    logging.info("%s: auto-filled Unknown for attribute.confidentiality.data.variety ", iid)
                    incident['attribute']['confidentiality']['data'] = [ { 'variety' : 'Unknown' } ]
                if len(incident['attribute']['confidentiality']['data']) == 0:
                    logging.info("%s: auto-filled Unknown for empty attribute.confidentiality.data.variety ", iid)
                    incident['attribute']['confidentiality']['data'] = [ { 'variety' : 'Unknown' } ]
                #for index, datatype in enumerate(incident['attribute']['confidentiality']['data']):
                    #astring = 'attribute.confidentiality.data.' + str(index) + '.variety'
                    #compareFromTo(astring, datatype['variety'], schema['attribute']['confidentiality']['data']['variety'])
                if 'data_disclosure' not in incident['attribute']['confidentiality']:
                    logging.warning("%s: data_disclosure not present (required if confidentiality present)", iid)
                    incident['attribute']['confidentiality']['data_disclosure'] = "Unknown"
                #else:
                    #astring = 'attribute.confidentiality.data_disclosure'
                    #compareFromTo(astring, incident['attribute']['confidentiality']['data_disclosure'], schema['attribute']['confidentiality']['data_disclosure'])
                #if 'state' in incident['attribute']['confidentiality']:
                    #astring = 'attribute.confidentiality.state'
                    #compareFromTo(astring, incident['attribute']['confidentiality']['state'], schema['attribute']['confidentiality']['state'])
            for attribute in ['integrity', 'availability']:
                if attribute in incident['attribute']:
                    if 'variety' not in incident['attribute'][attribute]:
                        logging.info("%s: auto-filled Unknown for attribute.%s.variety", iid, attribute)
                        incident['attribute'][attribute]['variety'] = [ 'Unknown' ]
                    if len(incident['attribute'][attribute]['variety']) == 0:
                        logging.info("%s: auto-filled Unknown for empty attribute.%s.variety", iid, attribute)
                        incident['attribute'][attribute]['variety'] = [ 'Unknown' ]
                    #astring = 'attribute.' + attribute + '.variety'
                    #compareFromTo(astring, incident['attribute'][attribute]['variety'], schema['attribute'][attribute]['variety'])
                    # only for availability
                    if 'duration' in incident['attribute'][attribute]:
                        if 'unit' not in incident['attribute'][attribute]['duration']:
                            logging.info("%s: auto-filled Unknown for attribute.%s.duration.unit", iid, attribute)
                            incident['attribute'][attribute]['duration']['unit'] = "unit"
                        #astring = 'attribute.' + attribute + '.duration.unit'
                        #compareFromTo(astring, incident['attribute'][attribute]['duration']['unit'], schema['timeline']['unit'])

        ## TIMELINE ##
        if 'timeline' not in incident: 
            logging.info("{0}: timeline section missing, auto-fillng in {1}".format(iid, int(cfg["year"])-1))
            incident['timeline'] = { 'incident' : { 'year' : int(cfg["year"])-1 } }
        if 'incident' not in incident['timeline']:
            logging.info("{0}: timeline.incident section missing, auto-fillng in {1}".format(iid, int(cfg["year"])-1))
            incident['timeline']['incident'] = { 'year' : int(cfg["year"])-1 }
            # assume that the schema validator will verify number
        #for timeline in ['compromise', 'exfiltration', 'discovery', 'containment']:
            #astring = 'timeline.' + timeline + '.unit'
            #if timeline in incident['timeline']:
                #if 'unit' in incident['timeline'][timeline]:
                    #compareFromTo(astring, incident['timeline'][timeline]['unit'], schema['timeline']['unit'])

        ## DISCOVERY METHOD ##
        if 'discovery_method' not in incident:
            logging.info("%s: auto-filled Unknown for discovery_method", iid)
            incident['discovery_method'] = "Unknown"
        #compareFromTo('discovery_method', incident['discovery_method'], schema['discovery_method'])
        #if incident.has_key('cost_corrective_action'):
            #compareFromTo('cost_corrective_action', incident['cost_corrective_action'], schema['cost_corrective_action'])
        #if incident.has_key('targeted'):
            #compareFromTo('targeted', incident['targeted'], schema['targeted'])
        #if incident.has_key('impact'):
            #if incident.has_key('overall_rating'):
                #compareFromTo('impact.overall_rating', incident['impact']['overall_rating'], schema['impact']['overall_rating'])
            #if incident.has_key('iso_currency_code'):
                #compareFromTo('impact.iso_currency_code', incident['impact']['iso_currency_code'], schema['iso_currency_code'])
            #if incident['impact'].has_key('loss'):
                #for index, loss in enumerate(incident['impact']['loss']):
                    #if loss.has_key('variety'):
                        #astring = 'impact.loss.' + str(index) + '.variety'
                        #compareFromTo(astring, loss['variety'], schema['impact']['loss']['variety'])
                    #if loss.has_key('rating'):
                        #astring = 'impact.loss.' + str(index) + '.rating'  # added g to the end of '.ratin' - GDB
                        #compareFromTo(astring, loss['rating'], schema['impact']['loss']['rating'])

        if 'plus' not in incident:
            incident['plus'] = {}
        #for method in ['attack_difficulty_legacy', 'attack_difficulty_initial', 'attack_difficulty_subsequent']:
            #if incident['plus'].has_key(method):
                #astring = 'plus.' + method
                #compareFromTo(astring, incident['plus'][method], schema['plus']['attack_difficulty'])
        #for method in ['analysis_status', 'public_disclosure', 'security_maturity']:
            #if incident['plus'].has_key(method):
                #astring = 'plus.' + method
                #compareFromTo(astring, incident['plus'][method], schema['plus'][method])


        ### Rules from import SG

        # KDT the script sometimes produces incidents with an asset array that has
        # no entries. I'm too lazy to figure out where that happens so I'll just
        # check for it here and fix it.
        if len(incident['asset']['assets']) < 1:
            incident['asset']['assets'].append({'variety':'Unknown'})
            logging.info("No asset varieties listed in {0} so adding asset.assets.variety.Unknown".format(iid))

        # make sure variety and vector are in actions and of correct length
        if 'action' not in incident:
            incident['action'] = { "Unknown" : {} }
            logging.info("No action so adding action.Unknown to {0}".format(iid))
        for action in ['hacking', 'malware', 'social', 'environmental', 'physical', 'misuse', 'error']:
            if action in incident['action'].keys():
                if 'variety' not in incident['action'][action].keys():
                    incident['action'][action]['variety'] = []
                if len(incident['action'][action]['variety']) == 0:
                    logging.info("Adding {0} variety to response {1} because it wasn't in there.".format(action, iid))
                    incident['action'][action]['variety'].append("Unknown")
                if action != 'environmental' and 'vector' not in incident['action'][action].keys():
                    incident['action'][action]['vector'] = []
                if  action != 'environmental' and len(incident['action'][action]['vector']) == 0:
                    logging.info("Adding {0} vector to response {1} because it wasn't in there.".format(action, iid))
                    incident['action'][action]['vector'].append("Unknown") 

        # if confidentiality then there should be something in the data array
        if 'confidentiality' in incident.get('attribute', {}):
            if 'data' not in incident['attribute']['confidentiality']:
                incident['attribute']['confidentiality']['data'] = []
            if len(incident['attribute']['confidentiality']['data']) == 0:
                logging.info("Adding attribute.confidentiality.data.variety:Unknown to {0} because attribute.confidentiality exists without data variety.".format(iid))
                incident['attribute']['confidentiality']['data'].append({'variety':'Unknown'})

        # if confidentiality was not affected then it shouldn't be in the plus
        # section either. Usually just has credit_monitoring unknown anyway.
        if 'confidentiality' not in incident.get('attribute', {}) and \
          incident['plus'].get('attribute', {}).keys() == ['confidentiality']:
            logging.info("attribute.confidentiality not in record so removing attribute from plus for record {0}.".format(iid))
            incident['plus'].pop('attribute')


     
        mydate = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        if 'created' not in incident['plus']:
            logging.info("%s: auto-filling now() for plus.created", iid)
            incident['plus']['created'] = mydate
        if 'modified' not in incident['plus']:
            logging.info("%s: auto-filling now() for plus.modified", iid)
            incident['plus']['modified'] = mydate

        return incident



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
    parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    #parser.add_argument("--dbir-private", required=False, help="The location of the dbirR repository.")
    #parser.add_argument("-s","--schemafile", help="The JSON schema file")
    #parser.add_argument("-e","--enumfile", help="The JSON file with VERIS enumerations")
    #parser.add_argument("--vcdb",help="Convert the data for use in VCDB",action="store_true")
    #parser.add_argument("--version", help="The version of veris in use")
    parser.add_argument('--conf', help='The location of the config file', default="./_checkValidity.cfg")
    parser.add_argument('--year', help='The DBIR year to assign tot he records.')
    #parser.add_argument('--countryfile', help='The json file holdering the country mapping.')
    parser.add_argument('--source', help="Source_id to use for the incidents. Partner pseudonym.")
    #parser.add_argument("-f", "--force_analyst", help="Override default analyst with --analyst.", action='store_true')
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}

    # Parse the config file
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(args["conf"]))
        cfg_key = {
            'GENERAL': ['input', 'output'], #'report', 'analysis', 'year', 'force_analyst', 'version', 'database', 'check'],
            'LOGGING': ['log_level', 'log_file'] #,
            # 'REPO': ['veris', 'dbir_private'],
            # 'VERIS': ['mergedfile', 'enumfile', 'schemafile', 'labelsfile', 'countryfile']
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
        logging.debug("config import succeeded.")
    except Exception as e:
        logging.warning("config import failed with error {0}.".format(e))
        #raise e
        pass

    cfg.update(args)
    veris_logger.updateLogger(cfg)

    logging.debug(args)

    logging.debug(cfg)

#    main(cfg)
# def main(cfg):
#    if __name__ != "__main__":
#        raise RuntimeError("Main should not be imported and run.  Instead run ''makeValid()' and 'addRules()'")

    logging.info('Beginning main loop.')
    formatter = ("- " + "/".join(cfg["input"].split("/")[-2:]))
    # Updating the format of the logging
    veris_logger.updateLogger(cfg, formatter)
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

    rules = Rules(cfg)

    # open each json file
    if 'output' in cfg and cfg['output'] is not None:
        overwrite = False
    else:
        overwrite = True
    for filename in tqdm(filenames):
        with open(filename, 'r+') as filehandle:
            try:
                incident = json.load(filehandle)
            except:
                logging.warning("Unable to load {0}.".format(filename))
                continue
            logging.debug("Before parsing:\n" + pformat(incident))
            # add 'unknowns' as appropriate
            incident = rules.makeValid(incident, cfg)
            # add rules
            incident = rules.addRules(incident, cfg)
            logging.debug("After parsing:\n" + pformat(incident))
            # save it back out
            if overwrite:
                filehandle.seek(0)
                json.dump(incident, filehandle, sort_keys=True, indent=2, separators=(',', ': '))
                filehandle.truncate()
            else:
                with open(cfg['output'].rstrip("/") + "/" + filename.split("/")[-1], 'w') as outfilehandle:
                    json.dump(incident, outfilehandle, sort_keys=True, indent=2, separators=(',', ': '))


    logging.info('Ending main loop.')