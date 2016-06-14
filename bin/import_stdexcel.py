#!/usr/bin/python

import json
import csv
import sys
import argparse
import os
import uuid
import hashlib # convert incident_id to UUID
import copy
import logging
#import multiprocessing # used for multiprocessing logger
import re
from datetime import datetime
import ConfigParser

# Default Configuration Settings
cfg = {
    'log_level': 'warning',
    'log_file': None,
    'schemafile': "../vcdb/veris.json",
    'enumfile': "../vcdb/veris-enum.json",
    'vcdb':False,
    'version':"1.3",
    'countryfile':'all.json',
    'output': os.getcwd(),
    'quiet': False,
    'repositories': ""
}
#logger = multiprocessing.get_logger()
logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG,
                 50: logging.CRITICAL, 40: logging.ERROR, 30: logging.WARNING, 20: logging.INFO, 10: logging.DEBUG, 0: logging.CRITICAL}
FORMAT = '%(asctime)19s - %(processName)s {0} - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT.format(""), datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger()

def reqSchema(v, base="", mykeylist={}):
    "given schema in v, returns a list of keys and it's type"
    if 'required' in v:
        if v['required']:
            if base not in mykeylist:
                mykeylist[base] = v['type']
            # mykeylist.append(base)
    if v['type']=="object":
        for k,v2 in v['properties'].items():
            if len(base):
                callout = base + "." + k
            else:
                callout = k
            reqSchema(v2, callout, mykeylist)
    elif v['type']=="array":
        reqSchema(v['items'], base, mykeylist)
    return mykeylist

def parseSchema(v, base="", mykeylist=[]):
    "given schema in v, returns a list of concatenated keys in the schema"
    if v['type']=="object":
        for k,v2 in v['properties'].items():
            if len(base):
                callout = base + "." + k
            else:
                callout = k
            parseSchema(v2, callout, mykeylist)
    elif v['type']=="array":
        parseSchema(v['items'], base, mykeylist)
    else:
        mykeylist.append(base)
    return mykeylist

def isnum(x):
    x = re.sub('[$,]', '', x)
    try:
        x=int(float(x))
    except:
        return None
    return x

def isfloat(x):
    x = re.sub('[$,]', '', x)
    try:
        x=float(x)
    except:
        return
    return x


def addValue(src, enum, dst, val="list"):
    "adding value to dst at key if present in src"
    if src.has_key(enum):
        if len(src[enum]):
            allenum = enum.split('.')
            saved = dst
            for i in range(len(allenum)-1):
                if not saved.has_key(allenum[i]):
                    saved[allenum[i]] = {}
                saved = saved[allenum[i]]
            if val=="list":
                templist = [x.strip() for x in src[enum].split(',') if len(x)>0 ]
                saved[allenum[-1]] = [x for x in templist if len(x)>0 ]
            elif val=="string":
                saved[allenum[-1]] = unicode(src[enum],errors='ignore')
            elif val=="numeric":
                if isnum(src[enum]):
                    saved[allenum[-1]] = isnum(src[enum])
            elif val=="integer":
                if isnum(src[enum]):
                    saved[allenum[-1]] = isnum(src[enum])

def chkDefault(incident, enum, default):
    allenum = enum.split('.')
    saved = incident
    for i in range(len(allenum)-1):
        if not saved.has_key(allenum[i]):
            saved[allenum[i]] = {}
        saved = saved[allenum[i]]
    if not saved[allenum[-1]]:
        saved[allenum[-1]] = copy.deepcopy(default)

def openJSON(filename):
    parsed = {}
    rawjson = open(filename).read()
    try:
        parsed = json.loads(rawjson)
    except:
        print "Unexpected error while loading", filename, "-", sys.exc_info()[1]
        parsed = None
    return parsed


def compareFromTo(label, fromArray, toArray):
    if isinstance(fromArray, basestring):
        if fromArray not in toArray:
            logger.warning("%s: %s has invalid enumeration: \"%s\"", iid, label, fromArray)
    else:
        if len(fromArray) == 0:
            logger.warning("%s: %s has no values in enumeration", iid, label)
        for item in fromArray:
            if item not in toArray:
                logger.warning("%s: %s has invalid enumeration: \"%s\"", iid, label, item)




def compareCountryFromTo(label, fromArray, toArray):
    if isinstance(fromArray, basestring):
        if fromArray not in toArray:
            logger.warning("%s: %s has invalid enumeration[1]: \"%s\"", iid, label, fromArray)
    else:
        if len(fromArray) == 0:
            logger.warning("%s: %s has no values in enumeration", iid, label)
        for idx, item in enumerate(fromArray):
            if item not in toArray:
                if item == "USA":
                    logger.warning("%s: %s was set to 'USA', converting to 'US'", iid, label)
                    fromArray[idx] = "US"
                elif item == "UK":
                    logger.warning("%s: %s was set to 'UK', converting to 'GB'", iid, label)
                    fromArray[idx] = "GB"
                else:
                    fromArray[idx] = "Unknown"
                    logger.warning("%s: %s has invalid enumeration[2]: \"%s\", converting to 'Unknown'", iid, label, item)
    if type(fromArray) == "str":
        fromArray = [ fromArray ]
    return(fromArray)




def checkIndustry(label, industry):
    if not industry.isdigit() and not industry in [ "31-33", "44-45", "48-49" ]:
        logger.warning("%s: %s is not numbers: \"%s\"", iid, label, industry)
        # retString.append("must be numbers or one of 31-33, 44-45, 48-49")

def checkEnum(incident, schema, country_region, cfg=cfg):
    if 'security_incident' not in incident:
        logger.warning("%s: security_incident not found (required)", iid)
    else:
        compareFromTo('security_incident', incident['security_incident'], schema['security_incident'])
    if 'victim' not in incident:
        logger.info("%s: auto-filled Unknown for victim section", iid)
        incident['victim'] = { 'employee_count' : 'Unknown', 'industry':"00", 'country': [ "Unknown" ], 'notes':'auto-filled Unknown' }
    victim = incident['victim']
    if 'employee_count' not in victim:
        logger.info("%s: auto-filled Unknown for victim.employee_count", iid)
        victim['employee_count'] = "Unknown"
    compareFromTo('victim.employee_count', victim['employee_count'], schema['victim']['employee_count'])
    if 'industry' not in victim:
        logger.info("%s: auto-filled Unknown for victim.industry", iid)
        victim['industry'] = "00"
    checkIndustry('victim.industry', victim['industry'])

    if 'country' not in victim:
        logger.info("%s: auto-filled Unknown for victim.country", iid)
        victim['country'] = [ "Unknown" ]

    # CC
    victim['country'] = compareCountryFromTo('victim.country', victim['country'], schema['victim']['country'])


    if 'actor' not in incident:
        logger.info("%s: auto-filled Unknown for entire actor section", iid)
        incident['actor'] = { 'unknown' : { 'notes':'auto-filled Unknown' } }
    if 'external' in incident['actor']:
        actor = incident['actor']['external']
        if 'motive' not in actor:
            logger.info("%s: auto-filled Unknown for actor.external.motive", iid)
            actor['motive'] = [ "Unknown" ]
        if len(actor['motive']) == 0:
            logger.info("%s: auto-filled Unknown for empty array in actor.external.motive", iid)
            actor['motive'] = [ "Unknown" ]
        compareFromTo('actor.external.motive', actor['motive'], schema['actor']['external']['motive'])
        if 'variety' not in actor:
            logger.info("%s: auto-filled Unknown for actor.external.variety", iid)
            actor['variety'] = [ "Unknown" ]
        if len(actor['variety']) == 0:
            logger.info("%s: auto-filled Unknown for empty array in actor.external.variety", iid)
            actor['variety'] = [ "Unknown" ]
        compareFromTo('actor.external.variety', actor['variety'], schema['actor']['external']['variety'])

        if 'country' in actor:
            if len(actor['country']) == 0:
                logger.info("%s: auto-filled Unknown for empty array in actor.external.country", iid)
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
            logger.info("%s: auto-filled Unknown for actor.external.country", iid)
            actor['country'] = [ "Unknown" ]

        if 'plus' not in incident:
            incident['plus'] = {}


        # CC
        actor['country'] = compareCountryFromTo('actor.external.country', actor['country'], schema['actor']['external']['country'])


    if 'internal' in incident['actor']:
        actor = incident['actor']['internal']
        if 'motive' not in actor:
            logger.info("%s: auto-filled Unknown for actor.internal.motive", iid)
            actor['motive'] = [ "Unknown" ]
        if len(actor['motive']) == 0:
            logger.info("%s: auto-filled Unknown for empty array in actor.internal.motive", iid)
            actor['motive'] = [ "Unknown" ]
        compareFromTo('actor.internal.motive', actor['motive'], schema['actor']['internal']['motive'])
        if 'variety' not in actor:
            logger.info("%s: auto-filled Unknown for actor.internal.variety", iid)
            actor['variety'] = [ "Unknown" ]
        if len(actor['variety']) == 0:
            logger.info("%s: auto-filled Unknown for empty array in actor.internal.variety", iid)
            actor['variety'] = [ "Unknown" ]
        compareFromTo('actor.internal.variety', actor['variety'], schema['actor']['internal']['variety'])
    if 'partner' in incident['actor']:
        actor = incident['actor']['partner']
        if 'motive' not in actor:
            logger.info("%s: auto-filled Unknown for actor.partner.motive", iid)
            actor['motive'] = [ "Unknown" ]
        if len(actor['motive']) == 0:
            logger.info("%s: auto-filled Unknown for empty array in actor.partner.motive", iid)
            actor['motive'] = [ "Unknown" ]
        compareFromTo('actor.partner.motive', actor['motive'], schema['actor']['partner']['motive'])
        if 'country' not in actor:
            logger.info("%s: auto-filled Unknown for actor.partner.country", iid)
            actor['country'] = [ "Unknown" ]
        if len(actor['country']) == 0:
            logger.info("%s: auto-filled Unknown for empty array in actor.partner.country", iid)
            actor['country'] = [ "Unknown" ]
        # compareFromTo('actor.partner.variety', actor['variety'], schema['actor']['partner']['country'])


        # CC
        actor['country'] = compareCountryFromTo('actor.partner.country', actor['country'], schema['actor']['partner']['country'])


        if 'industry' not in actor:
            logger.info("%s: auto-filled Unknown for actor.partner.industry", iid)
            actor['industry'] = "00"
        checkIndustry('actor.partner.industry', actor['industry'])

    if 'action' not in incident:
        logger.info("%s: auto-filled Unknown for entire action section", iid)
        incident['action'] = { "unknown" : { "notes" : "auto-filled Unknown" } }

    for action in ['malware', 'hacking', 'social', 'misuse', 'physical', 'error']:
        if action in incident['action']:
            for method in ['variety', 'vector']:
                if method not in incident['action'][action]:
                    logger.info("%s: auto-filled Unknown for action.%s.%s", iid, action, method)
                    incident['action'][action][method] = [ 'Unknown' ]
                if len(incident['action'][action][method]) == 0:
                    logger.info("%s: auto-filled Unknown for empty array in action.%s.%s", iid, action, method)
                    incident['action'][action][method] = [ 'Unknown' ]
                astring = 'action.' + action + '.' + method
                compareFromTo(astring, incident['action'][action][method], schema['action'][action][method])
            if action == "physical":
                method = "vector"
                if method not in incident['action'][action]:
                    logger.info("%s: auto-filled Unknown for action.%s.%s", iid, action, method)
                    incident['action'][action][method] = [ 'Unknown' ]
                if len(incident['action'][action][method]) == 0:
                    logger.info("%s: auto-filled Unknown for empty array in action.%s.%s", iid, action, method)
                    incident['action'][action][method] = [ 'Unknown' ]
                astring = 'action.' + action + '.' + method
                compareFromTo(astring, incident['action'][action][method], schema['action'][action][method])
            if action == "social":
                method = "target"
                if method not in incident['action'][action]:
                    logger.info("%s: auto-filled Unknown for action.%s.%s", iid, action, method)
                    incident['action'][action][method] = [ 'Unknown' ]
                if len(incident['action'][action][method]) == 0:
                    logger.info("%s: auto-filled Unknown for empty array in action.%s.%s", iid, action, method)
                    incident['action'][action][method] = [ 'Unknown' ]
                astring = 'action.' + action + '.' + method
                compareFromTo(astring, incident['action'][action][method], schema['action'][action][method])
    action = 'environmental'
    if action in incident['action']:
        method = "variety"
        if method not in incident['action'][action]:
            logger.info("%s: auto-filled Unknown for action.%s.%s", iid, action, method)
            incident['action'][action][method] = [ 'Unknown' ]
        if len(incident['action'][action][method]) == 0:
            logger.info("%s: auto-filled Unknown for empty array in action.%s.%s", iid, action, method)
            incident['action'][action][method] = [ 'Unknown' ]
        astring = 'action.' + action + '.' + method
        compareFromTo(astring, incident['action'][action][method], schema['action'][action][method])

    if 'asset' not in incident:
        logger.info("%s: auto-filled Unknown for entire asset section", iid)
        incident['asset'] = { "assets" : [ { "variety" : "Unknown" } ] }
    if 'assets' not in incident['asset']:
        logger.info("%s: auto-filled Unknown for asset.asseets section", iid)
        incident['asset']['assets'] = [ { "variety" : "Unknown" } ]
    for index, asset in enumerate(incident['asset']['assets']):
        if 'variety' not in asset:
            logger.info("%s: auto-filled Unknown for asset.asseets.variety ", iid)
            asset['variety'] = "Unknown"
        compareFromTo('asset.assets.' + str(index) + '.variety', asset['variety'], schema['asset']['assets']['variety'])
    for method in ["cloud", "accessibility", "ownership", "management", "hosting"]:
        if method in incident:
            compareFromTo('asset.'+method, incident['asset'][method], schema['asset'][method])

    if 'attribute' not in incident:
        logger.info("%s: no attribute section is found (not required)", iid)
    else:
        if 'confidentiality' in incident['attribute']:
            if 'data' not in incident['attribute']['confidentiality']:
                logger.info("%s: auto-filled Unknown for attribute.confidentiality.data.variety ", iid)
                incident['attribute']['confidentiality']['data'] = [ { 'variety' : 'Unknown' } ]
            if len(incident['attribute']['confidentiality']['data']) == 0:
                logger.info("%s: auto-filled Unknown for empty attribute.confidentiality.data.variety ", iid)
                incident['attribute']['confidentiality']['data'] = [ { 'variety' : 'Unknown' } ]
            for index, datatype in enumerate(incident['attribute']['confidentiality']['data']):
                astring = 'attribute.confidentiality.data.' + str(index) + '.variety'
                compareFromTo(astring, datatype['variety'], schema['attribute']['confidentiality']['data']['variety'])
            if 'data_disclosure' not in incident['attribute']['confidentiality']:
                logger.warning("%s: data_disclosure not present (required if confidentiality present)", iid)
            else:
                astring = 'attribute.confidentiality.data_disclosure'
                compareFromTo(astring, incident['attribute']['confidentiality']['data_disclosure'], schema['attribute']['confidentiality']['data_disclosure'])
            if 'state' in incident['attribute']['confidentiality']:
                astring = 'attribute.confidentiality.state'
                compareFromTo(astring, incident['attribute']['confidentiality']['state'], schema['attribute']['confidentiality']['state'])
        for attribute in ['integrity', 'availability']:
            if attribute in incident['attribute']:
                if 'variety' not in incident['attribute'][attribute]:
                    logger.info("%s: auto-filled Unknown for attribute.%s.variety", iid, attribute)
                    incident['attribute'][attribute]['variety'] = [ 'Unknown' ]
                if len(incident['attribute'][attribute]['variety']) == 0:
                    logger.info("%s: auto-filled Unknown for empty attribute.%s.variety", iid, attribute)
                    incident['attribute'][attribute]['variety'] = [ 'Unknown' ]
                astring = 'attribute.' + attribute + '.variety'
                compareFromTo(astring, incident['attribute'][attribute]['variety'], schema['attribute'][attribute]['variety'])
                # only for availability
                if 'duration' in incident['attribute'][attribute]:
                    if 'unit' not in incident['attribute'][attribute]['duration']:
                        logger.info("%s: auto-filled Unknown for attribute.%s.duration.unit", iid, attribute)
                        incident['attribute'][attribute]['duration']['unit'] = "unit"
                    astring = 'attribute.' + attribute + '.duration.unit'
                    compareFromTo(astring, incident['attribute'][attribute]['duration']['unit'], schema['timeline']['unit'])

    if 'timeline' not in incident: 
        logger.info("{0}: timeline section missing, auto-fillng in {1}".format(iid, cfg["year"]-1))
        incident['timeline'] = { 'incident' : { 'year' : cfg["year"]-1 } }
    if 'incident' not in incident['timeline']:
        logger.info("{0}: timeline.incident section missing, auto-fillng in {1}".format(iid, cfg["year"]-1))
        incident['timeline']['incident'] = { 'year' : cfg["year"]-1 }
        # assume that the schema validator will verify number
    for timeline in ['compromise', 'exfiltration', 'discovery', 'containment']:
        astring = 'timeline.' + timeline + '.unit'
        if timeline in incident['timeline']:
            if 'unit' in incident['timeline'][timeline]:
                compareFromTo(astring, incident['timeline'][timeline]['unit'], schema['timeline']['unit'])

    if 'discovery_method' not in incident:
        logger.info("%s: auto-filled Unknown for discovery_method", iid)
        incident['discovery_method'] = "Unknown"
    compareFromTo('discovery_method', incident['discovery_method'], schema['discovery_method'])
    if incident.has_key('cost_corrective_action'):
        compareFromTo('cost_corrective_action', incident['cost_corrective_action'], schema['cost_corrective_action'])
    if incident.has_key('targeted'):
        compareFromTo('targeted', incident['targeted'], schema['targeted'])
    if incident.has_key('impact'):
        if incident.has_key('overall_rating'):
            compareFromTo('impact.overall_rating', incident['impact']['overall_rating'], schema['impact']['overall_rating'])
        if incident.has_key('iso_currency_code'):
            compareFromTo('impact.iso_currency_code', incident['impact']['iso_currency_code'], schema['iso_currency_code'])
        if incident['impact'].has_key('loss'):
            for index, loss in enumerate(incident['impact']['loss']):
                if loss.has_key('variety'):
                    astring = 'impact.loss.' + str(index) + '.variety'
                    compareFromTo(astring, loss['variety'], schema['impact']['loss']['variety'])
                if loss.has_key('rating'):
                    astring = 'impact.loss.' + str(index) + '.rating'  # added g to the end of '.ratin' - GDB
                    compareFromTo(astring, loss['rating'], schema['impact']['loss']['rating'])
    if 'plus' not in incident:
        incident['plus'] = {}
    for method in ['attack_difficulty_legacy', 'attack_difficulty_initial', 'attack_difficulty_subsequent']:
        if incident['plus'].has_key(method):
            astring = 'plus.' + method
            compareFromTo(astring, incident['plus'][method], schema['plus']['attack_difficulty'])
    for method in ['analysis_status', 'public_disclosure', 'security_maturity']:
        if incident['plus'].has_key(method):
            astring = 'plus.' + method
            compareFromTo(astring, incident['plus'][method], schema['plus'][method])
    if 'dbir_year' not in incident['plus'] and cfg['vcdb'] != True:
        logger.warning("{0}: missing plus.dbir_year, auto-filled {1}".format(iid, cfg["year"]))
        incident['plus']['dbir_year'] = cfg["year"]
    if ('source_id' not in incident or cfg["force_analyst"]) and 'source' in cfg:
        incident['source_id'] = cfg['source']
    mydate = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    if 'created' not in incident['plus']:
        logger.info("%s: auto-filling now() for plus.created", iid)
        incident['plus']['created'] = mydate
    if 'modified' not in incident['plus']:
        logger.info("%s: auto-filling now() for plus.modified", iid)
        incident['plus']['modified'] = mydate
    if 'master_id' not in incident['plus']:
        if 'incident_id' in incident:
            master_id = incident['incident_id']
        else:
            master_id = "notblank"
        logger.info("%s: auto-filling plus.master_id to %s", iid, master_id)
        incident['plus']['master_id'] = master_id
    return incident

def parseComplex(field, inline, labels):
    regex = re.compile(r',+') # parse on one or more consequtive commas
    units = [x.strip() for x in regex.split(inline)]
    retval = []
    for i in units:
        entry = [x.strip() for x in i.split(':')]
        out = {}
        for index, s in enumerate(entry):
            if index > len(labels):
                logger.warning("%s: failed to parse complex field %s, more entries seperated by colons than labels, skipping", iid, field)
                return
            elif len(s):
                out[labels[index]] = s
        if len(out) > 0:
            retval.append(copy.deepcopy(out))
    return retval

def cleanValue(incident, enum):
    v = re.sub("^[,]+", "", incident[enum])
    v = re.sub("[,]+$", "", v)
    v = re.sub("[,]+", ",", v)
    return(v)

def convertCSV(incident, cfg=cfg):
    out = {}
    out['schema_version'] = cfg["version"]
    if incident.has_key("incident_id"):
        if len(incident['incident_id']):
#            out['incident_id'] = incident['incident_id']
            # Changing incident_id to UUID to prevent de-anonymiziation of incidents
            m = hashlib.md5(incident["incident_id"])
            out["incident_id"] = str(uuid.UUID(bytes=m.digest())).upper()
        else:
            out['incident_id'] = str(uuid.uuid4()).upper()
    else:
        out['incident_id'] = str(uuid.uuid4()).upper()
    tmp = {}
    for enum in incident: tmp[enum] = cleanValue(incident, enum)
    incident = tmp
    for enum in ['source_id', 'reference', 'security_incident', 'confidence', 'summary', 'related_incidents', 'notes']:
        addValue(incident, enum, out, "string")
    # victim
    for enum in ['victim_id', 'industry', 'employee_count', 'state',
            'revenue.iso_currency_code', 'secondary.notes', 'notes']:
        addValue(incident, 'victim.'+enum, out, "string")
    addValue(incident, 'victim.revenue.amount', out, "integer")
    addValue(incident, 'victim.secondary.amount', out, "numeric")
    addValue(incident, 'victim.secondary.victim_id', out, "list")
    addValue(incident, 'victim.locations_affected', out, "numeric")
    addValue(incident, 'victim.country', out, "list")

    # actor
    for enum in ['motive', 'variety', 'country']:
        addValue(incident, 'actor.external.'+enum, out, 'list')
    addValue(incident, 'actor.external.notes', out, 'string')
    for enum in ['motive', 'variety']:
        addValue(incident, 'actor.internal.'+enum, out, 'list')
    addValue(incident, 'actor.internal.notes', out, 'string')
    for enum in ['motive', 'country']:
        addValue(incident, 'actor.partner.'+enum, out, 'list')
    addValue(incident, 'actor.partner.industry', out, 'string')
    addValue(incident, 'actor.partner.notes', out, 'string')

    # action
    action = "malware."
    for enum in ['variety', 'vector']:
        addValue(incident, 'action.' + action + enum, out, 'list')
    for enum in ['cve', 'name', 'notes']:
        addValue(incident, 'action.' + action + enum, out, 'string')
    action = "hacking."
    for enum in ['variety', 'vector']:
        addValue(incident, 'action.' + action + enum, out, 'list')
    for enum in ['cve', 'notes']:
        addValue(incident, 'action.' + action + enum, out, 'string')
    action = "social."
    for enum in ['variety', 'vector', 'target']:
        addValue(incident, 'action.' + action + enum, out, 'list')
    for enum in ['notes']:
        addValue(incident, 'action.' + action + enum, out, 'string')
    action = "misuse."
    for enum in ['variety', 'vector']:
        addValue(incident, 'action.' + action + enum, out, 'list')
    for enum in ['notes']:
        addValue(incident, 'action.' + action + enum, out, 'string')
    action = "physical."
    for enum in ['variety', 'vector', 'vector']:
        addValue(incident, 'action.' + action + enum, out, 'list')
    for enum in ['notes']:
        addValue(incident, 'action.' + action + enum, out, 'string')
    action = "error."
    for enum in ['variety', 'vector']:
        addValue(incident, 'action.' + action + enum, out, 'list')
    for enum in ['notes']:
        addValue(incident, 'action.' + action + enum, out, 'string')
    action = "environmental."
    for enum in ['variety']:
        addValue(incident, 'action.' + action + enum, out, 'list')
    for enum in ['notes']:
        addValue(incident, 'action.' + action + enum, out, 'string')
    # asset
    if 'asset.assets.variety' in incident:
        if 'asset' not in out:
            out['asset'] = {}
        if 'assets' not in out['asset']:
            out['asset']['assets'] = []
        assets = parseComplex("asset.assets.variety", incident['asset.assets.variety'], ['variety', 'amount'])
        if len(assets):
            for i in assets:
                if 'amount' in i:
                    if isnum(i['amount']) is not None:
                        i['amount'] = isnum(i['amount'])
                    else:
                        del i['amount']
            out['asset']['assets'] = copy.deepcopy(assets)

    for enum in ['accessibility', 'ownership', 'management', 'hosting', 'cloud', 'notes']:
        addValue(incident, 'asset.' + enum, out, 'string')
    addValue(incident, 'asset.country', out, 'list')

    # attributes
    if 'attribute.confidentiality.data.variety' in incident:
        data = parseComplex("attribute.confidentiality.data.variety", incident['attribute.confidentiality.data.variety'], ['variety', 'amount'])
        if len(data):
            if 'attribute' not in out:
                out['attribute'] = {}
            if 'confidentiality' not in out['attribute']:
                out['attribute']['confidentiality'] = {}
            if 'data' not in out['attribute']['confidentiality']:
                out['attribute']['confidentiality']['data'] = []
            for i in data:
                if 'amount' in i:
                    if isnum(i['amount']) is not None:
                        i['amount'] = isnum(i['amount'])
                    else:
                        del i['amount']
            out['attribute']['confidentiality']['data'] = copy.deepcopy(data)
    addValue(incident, 'attribute.confidentiality.data_disclosure', out, 'string')
    addValue(incident, 'attribute.confidentiality.data_total', out, 'numeric')
    addValue(incident, 'attribute.confidentiality.state', out, 'list')
    addValue(incident, 'attribute.confidentiality.notes', out, 'string')

    addValue(incident, 'attribute.integrity.variety', out, 'list')
    addValue(incident, 'attribute.integrity.notes', out, 'string')

    addValue(incident, 'attribute.availability.variety', out, 'list')
    addValue(incident, 'attribute.availability.duration.unit', out, 'string')
    addValue(incident, 'attribute.availability.duration.value', out, 'numeric')
    addValue(incident, 'attribute.availability.notes', out, 'string')

    # timeline
    addValue(incident, 'timeline.incident.year', out, 'numeric')
    addValue(incident, 'timeline.incident.month', out, 'numeric')
    addValue(incident, 'timeline.incident.day', out, 'numeric')
    addValue(incident, 'timeline.incident.time', out, 'string')

    addValue(incident, 'timeline.compromise.unit', out, 'string')
    addValue(incident, 'timeline.compromise.value', out, 'numeric')
    addValue(incident, 'timeline.exfiltration.unit', out, 'string')
    addValue(incident, 'timeline.exfiltration.value', out, 'numeric')
    addValue(incident, 'timeline.discovery.unit', out, 'string')
    addValue(incident, 'timeline.discovery.value', out, 'numeric')
    addValue(incident, 'timeline.containment.unit', out, 'string')
    addValue(incident, 'timeline.containment.value', out, 'numeric')

    # trailer values
    for enum in ['discovery_method', 'targeted', 'control_failure', 'corrective_action']:
        addValue(incident, enum, out, 'string')
    if 'ioc.indicator' in incident:
        ioc = parseComplex("ioc.indicator", incident['ioc.indicator'], ['indicator', 'comment'])
        if len(ioc):
            out['ioc'] = copy.deepcopy(ioc)

    # impact
    for enum in ['overall_min_amount', 'overall_amount', 'overall_max_amount']:
        addValue(incident, 'impact.'+enum, out, 'numeric')
    # TODO handle impact.loss varieties
    for enum in ['overall_rating', 'iso_currency_code', 'notes']:
        addValue(incident, 'impact.'+enum, out, 'string')
    # plus
    plusfields = ['master_id', 'investigator', 'issue_id', 'casename', 'analyst',
            'analyst_notes', 'public_disclosure', 'analysis_status',
            'attack_difficulty_legacy', 'attack_difficulty_subsequent',
            'attack_difficulty_initial', 'security_maturity' ]
    if cfg["vcdb"]:
        plusfields.append('github')
    for enum in plusfields:
        addValue(incident, 'plus.'+enum, out, "string")
    addValue(incident, 'plus.dbir_year', out, "numeric")
    # addValue(incident, 'plus.external_region', out, "list")
    if cfg["vcdb"]:
        addValue(incident, 'plus.timeline.notification.year', out, "numeric")
        addValue(incident, 'plus.timeline.notification.month', out, "numeric")
        addValue(incident, 'plus.timeline.notification.day', out, "numeric")
    # Skipping: 'unknown_unknowns', useful_evidence', antiforensic_measures, unfollowed_policies,
    # countrol_inadequacy_legacy, pci
    # TODO dbir_year

    return out


def getCountryCode(countryfile):  # Removed default of 'all.json' - GDB
    # Fixed the hard-coded name - GDB
    country_codes = json.loads(open(countryfile).read())
    country_code_remap = {'Unknown':'000000'}
    for eachCountry in country_codes:
        try:
            country_code_remap[eachCountry['alpha-2']] = eachCountry['region-code']
        except:
            country_code_remap[eachCountry['alpha-2']] = "000"
        try:
            country_code_remap[eachCountry['alpha-2']] += eachCountry['sub-region-code']
        except:
            country_code_remap[eachCountry['alpha-2']] += "000"
    return country_code_remap


# jenums = openJSON("verisvz-enum.json")
# jscehma = openJSON("verisvz.json")


def main(cfg):
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

    try:
        # Added to file read to catch multiple columns with same name which causes second column to overwrite first. - GDB
        file_handle = open(cfg["input"], 'rU')
        csv_reader = csv.reader(file_handle)
        l = csv_reader.next()
        if len(l) > len(set(l)):
            logger.error(l)
            raise KeyError("Input file has multiple columns of the same name.  Please create unique columns and rerun.")
            file_handle.close()
            exit(1)
        else:
            file_handle.seek(0)
            infile = csv.DictReader(file_handle)
#        infile = csv.DictReader(open(args.filename,'rU'))  # Old File Read - gdb
    except IOError:
        logger.critical("ERROR: Input file not found.")
        exit(1)

    try:
        jschema = openJSON(cfg["schemafile"])
    except IOError:
        logger.critical("ERROR: Schema file not found.")
        exit(1)
    try:
        jenums = openJSON(cfg["enumfile"])
    except IOError:
        logger.critical("ERROR: Enumeration file not found.")
        exit(1)

    reqfields = reqSchema(jschema)
    sfields = parseSchema(jschema)

    for f in infile.fieldnames:
        if f not in sfields:
            if f != "repeat":
                logger.warning("column will not be used: %s. May be inaccurate for 'plus' columns.", f)
    if 'plus.analyst' not in infile.fieldnames:
        logger.warning("the optional plus.analyst field is not found in the source document")
    if 'source_id' not in infile.fieldnames:
        logger.warning("the optional source_id field is not found in the source document")

    row = 0
    for incident in infile:
        row += 1
        # have to look for white-space only and remove it
        try:
            incident = { x:incident[x].strip() for x in incident }
        except AttributeError as e:
            logger.error("Error removing white space from feature {0} on row {1}.".format(x, row))
            raise e

        #if 'incident_id' in incident:
        #    iid = incident['incident_id']
        #else:
        #    iid = "srcrow_" + str(row)
        # logger.warning("This includes the row number")
        iid = incident['incident_id']  # there should always be an incident ID so commented out above. - gdb 061316

        repeat = 1
        logger.info("-----> parsing incident %s", iid)
        if incident.has_key('repeat'):
            if incident['repeat'].lower()=="ignore" or incident['repeat'] == "0":
                logger.info("Skipping row %s", iid)
                continue
            repeat = isnum(incident['repeat'])
            if not repeat:
                repeat = 1
        if incident.has_key('security_incident'):
            if incident['security_incident'].lower()=="no":
                logger.info("Skipping row %s", iid)
                continue
        outjson = convertCSV(incident, cfg)
        country_region = getCountryCode(cfg["countryfile"])
        checkEnum(outjson, jenums, country_region, cfg)
        #addRules(outjson)  # moved to add_rules.py, imported and run by import_veris.py. -gdb 06/09/16


        # adding row number to help with reverse tracability in v1.3.1 per issue 112. -gdb 06/09/16
        outjson['plus']['row_number'] = row

        while repeat > 0:
            outjson['plus']['master_id'] = str(uuid.uuid4()).upper()
            yield iid, outjson
            # outjson['incident_id'] = str(uuid.uuid4()).upper()     ### HERE
            # outjson['plus']['master_id'] = outjson['incident_id']  ###
            repeat -= 1
            if repeat > 0:
                logger.info("Repeating %s more times on %s", repeat, iid)

    file_handle.close()

iid = ""  # setting global
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Convert Standard Excel (csv) format to VERIS 1.3 schema-compatible JSON files")
    parser.add_argument("-i", "--input", help="The csv file containing the data")
    parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument("-s","--schemafile", help="The JSON schema file")
    parser.add_argument("-e","--enumfile", help="The JSON file with VERIS enumerations")
    parser.add_argument("--vcdb",help="Convert the data for use in VCDB",action="store_true")
    parser.add_argument("--version", help="The version of veris in use")
    parser.add_argument('--conf', help='The location of the config file', default="./_checkValidity.cfg")
    parser.add_argument('--year', help='The DBIR year to assign tot he records.')
    parser.add_argument('--countryfile', help='The json file holdering the country mapping.')
    parser.add_argument('--source', help="Source_id to use for the incidents. Partner pseudonym.")
    parser.add_argument("-f", "--force_analyst", help="Override default analyst with --analyst.", action='store_true')
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("-o", "--output", help="directory where json files will be written")
    output_group.add_argument("-q", "--quiet", help="suppress the writing of json files.", action='store_true')
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}

    logger.setLevel(logging_remap[args['log_level']])

    # Parse the config file
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(args["conf"]))
        cfg_key = {
            'GENERAL': ['input', 'output'],
            'LOGGING': ['level', 'log_file'],
            'VERIS': ['version', 'schemafile', 'enumfile', 'vcdb', 'year', 'countryfile']
        }
        for section in cfg_key.keys():
            if config.has_section(section):
                for value in cfg_key[section]:
                    if value.lower() in config.options(section):
                        cfg[value] = config.get(section, value)
        if "year" in cfg:
            cfg["year"] = int(cfg["year"])
        else:
            cfg["year"] = int(datetime.now().year)
        cfg["vcdb"] = {True:True, False:False, "false":False, "true":True}[cfg["vcdb"].lower()]
        logger.debug("config import succeeded.")
    except Exception as e:
        logger.warning("config import failed.")
        #raise e
        pass

    #cfg.update({k:v for k,v in vars(args).iteritems() if k not in cfg.keys()})  # copy command line arguments to the 
    #cfg.update(vars(args))  # overwrite configuration file variables with 
    cfg.update(args)
    if 'quiet' in args and args['quiet'] == True:
        _ = cfg.pop('output')

    # if source missing, try and guess it from directory
    if 'source' not in cfg or not cfg['source']:
        cfg['source'] = cfg['input'].split("/")[-2].lower()
        cfg['source'] = ''.join(e for e in cfg['source'] if e.isalnum())
        logger.warning("Source not defined.  Using the directory of the input file {0} instead.".format(cfg['source']))

    # Quick test to replace any placeholders accidentally left in the config
    for k, v in cfg.iteritems():
        if k not in  ["repositories", "source"] and type(v) == str:
            cfg[k] = v.format(repositories=cfg["repositories"], partner_name=cfg["source"])

    logger.setLevel(logging_remap[cfg["log_level"]])
    if cfg["log_file"] is not None:
        fh = FileHandler(cfg["log_file"])
        fh.setLevel(logging_remap[cfg["log_level"]])
        logger.addHandler(fh)
    # format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    logger.debug(args)
    logger.debug(cfg)

    # call the main loop which yields json incidents
    logger.info("Output files will be written to %s",cfg["output"])
    for iid, incident_json in main(cfg):
        # write the json to a file
        if cfg["output"].endswith("/"):
            dest = cfg["output"] + incident_json['plus']['master_id'] + '.json'
            # dest = args.output + outjson['incident_id'] + '.json'
        else:
            dest = cfg["output"] + '/' + incident_json['plus']['master_id'] + '.json'
            # dest = args.output + '/' + outjson['incident_id'] + '.json'
        logger.info("%s: writing file to %s", iid, dest)
        try:
            fwrite = open(dest, 'w')
            fwrite.write(json.dumps(incident_json, indent=2, sort_keys=True))
            fwrite.close()
        except UnicodeDecodeError:
            print incident_json
