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
    out['plus'] = {}
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
            with open(dest, 'w') as fwrite:
                json.dump(incident_json, fwrite, indent=2, sort_keys=True, separators=(',', ': '))
        except UnicodeDecodeError:
            logging.critical("Some kind of unicode error in response %s. Movin on.", iid)
            logging.critical(incident_json)
