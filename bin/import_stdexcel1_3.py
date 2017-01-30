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
import re
from datetime import datetime
import ConfigParser
from collections import defaultdict
import re
import operator
import imp
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise

# Default Configuration Settings
cfg = {
    'log_level': 'warning',
    'log_file': None,
    'schemafile': "../verisc.json",
    'enumfile': "../verisc-enum.json",
    'mergedfile': "../verisc-merged",
    'vcdb':False,
    'version':"1.3",
    'countryfile':'all.json',
    'output': os.getcwd(),
    'check': False,
    'repositories': ""
}

class CSVtoJSON():
    """Imports a CSV outputted by the standard excel survey gizmo form"""
    jmerged = None
    jschema = None
    jenums = None
    cfg = None
    # reqfields=None
    sfields = None
    # country_code_remap = None
    script_version = "1.3"


    def __init__(self, cfg, file_version=None):
        veris_logger.updateLogger(cfg)
        logging.debug("Initializing CSVtoJSON object.")

        if file_version is None:
            file_version = cfg.get("file_version", None)
        if file_version is None:
            file_version = self.get_file_schema_version(cfg['input'])
        if file_version is None:
            logging.warning("Could not determine veris version of {0}.  Please specify it as an argument to the class initialization, 'CSVtoJSON(cfg, file_version=<file version>)'".format(cfg['input']))
        elif file_version != self.script_version:
            logging.warning("File veris version {0} does not match script veris version {1}.".format(file_version, self.script_version))
        cfg['file_version'] = file_version

        if type(cfg["mergedfile"]) == dict:
            self.jmerged = cfg["mergedfile"]
        else:
            try:
                self.jmerged = self.openJSON(cfg["mergedfile"])
            except IOError:
                logging.warning("Merged file not found.")
        if type(cfg["schemafile"]) == dict:
            self.jschema = cfg["schemafile"]
        else:
            try:
                self.jschema = self.openJSON(cfg["schemafile"])
            except IOError:
                logging.warning("Schema file not found.")
        if type(cfg["enumfile"]) == dict:
            self.jenums = cfg["enumfile"]
        else:
            try:
                self.jenums = self.openJSON(cfg["enumfile"])
            except IOError:
                logging.critical("Enumeration file not found.")
                raise
                # exit(1)

        # self.reqfields = self.reqSchema(self.jschema)
        try:
            self.sfields = self.parseSchema(self.jmerged)
        except TypeError:
            try:
                self.sfields = self.parseSchema(self.jschema)
            except TypeError:
                logging.critical("No merged or schema file available to create field names from.")
                raise
                # exit(1)

        self.cfg = cfg

    def get_file_schema_version(self, inFile):
        logging.info("Reading {0} to determine version.".format(inFile))
        with open(inFile, 'rU') as filehandle:
            m = re.compile(r'(\.0+)*$')
            versions = defaultdict(int)
            csv_reader = csv.DictReader(filehandle)
            if "schema_version" in csv_reader.fieldnames:
                for row in csv_reader:
                    versions[m.sub('', row["schema_version"])] += 1 # the regex removes trailing '.0' to make counting easier
                version = max(versions.iteritems(), key=operator.itemgetter(1))[0]  # return the most common version. (They shoudl all be the same, but, you know.)
                if version not in ["1.2", "1.3", "1.3.1", "1.4"]:
                    logging.warning("VERIS version {0} in file {1} does not appear to be a standard version.  \n".format(version, inFile) + 
                                   "Please ensure it is correct as it is used for upgrading VERIS files to the report version.")
                if not version:
                    logging.warning("No VERIS version found in file {0}.".format(inFile))
                    return None
                else:
                    return version
            else:
                logging.warning("No VERIS version found in file {0}.".format(inFile))
                return None


    def reqSchema(self, v, base="", mykeylist={}):
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
                self.reqSchema(v2, callout, mykeylist)
        elif v['type']=="array":
            self.reqSchema(v['items'], base, mykeylist)
        return mykeylist


    def parseSchema(self, v, base="", mykeylist=[]):
        "given schema in v, returns a list of concatenated keys in the schema"
        if v['type']=="object":
            for k,v2 in v['properties'].items():
                if len(base):
                    callout = base + "." + k
                else:
                    callout = k
                self.parseSchema(v2, callout, mykeylist)
        elif v['type']=="array":
            self.parseSchema(v['items'], base, mykeylist)
        else:
            mykeylist.append(base)
        return mykeylist


    def isnum(self, x):
        x = re.sub('[$,]', '', x)
        try:
            x=int(float(x))
        except:
            return None
        return x


    def isfloat(self, x):
        x = re.sub('[$,]', '', x)
        try:
            x=float(x)
        except:
            return
        return x


    def addValue(self, src, enum, dst, val="list"):
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
                    if self.isfloat(src[enum]):
                        saved[allenum[-1]] = self.isfloat(src[enum])
                elif val=="integer":
                    if self.isnum(src[enum]):
                        saved[allenum[-1]] = self.isnum(src[enum])


    def chkDefault(self, incident, enum, default):
        allenum = enum.split('.')
        saved = incident
        for i in range(len(allenum)-1):
            if not saved.has_key(allenum[i]):
                saved[allenum[i]] = {}
            saved = saved[allenum[i]]
        if not saved[allenum[-1]]:
            saved[allenum[-1]] = copy.deepcopy(default)


    def openJSON(self, filename):
        parsed = {}
        rawjson = open(filename).read()
        try:
            parsed = json.loads(rawjson)
        except:
            print "Unexpected error while loading", filename, "-", sys.exc_info()[1]
            parsed = None
        return parsed


    # def compareFromTo(self, label, fromArray, toArray):
    #     if isinstance(fromArray, basestring):
    #         if fromArray not in toArray:
    #             logging.warning("%s: %s has invalid enumeration: \"%s\"", iid, label, fromArray)
    #     else:
    #         if len(fromArray) == 0:
    #             logging.warning("%s: %s has no values in enumeration", iid, label)
    #         for item in fromArray:
    #             if item not in toArray:
    #                 logging.warning("%s: %s has invalid enumeration: \"%s\"", iid, label, item)


    # def compareCountryFromTo(self, label, fromArray, toArray):
    #     if isinstance(fromArray, basestring):
    #         if fromArray not in toArray:
    #             logging.warning("%s: %s has invalid enumeration[1]: \"%s\"", iid, label, fromArray)
    #     else:
    #         if len(fromArray) == 0:
    #             logging.warning("%s: %s has no values in enumeration", iid, label)
    #         for idx, item in enumerate(fromArray):
    #             if item not in toArray:
    #                 if item == "USA":
    #                     logging.warning("%s: %s was set to 'USA', converting to 'US'", iid, label)
    #                     fromArray[idx] = "US"
    #                 elif item == "UK":
    #                     logging.warning("%s: %s was set to 'UK', converting to 'GB'", iid, label)
    #                     fromArray[idx] = "GB"
    #                 else:
    #                     fromArray[idx] = "Unknown"
    #                     logging.warning("%s: %s has invalid enumeration[2]: \"%s\", converting to 'Unknown'", iid, label, item)
    #     if type(fromArray) == "str":
    #         fromArray = [ fromArray ]
    #     return(fromArray)


    # def checkIndustry(self, label, industry):
    #     if not industry.isdigit() and not industry in [ "31-33", "44-45", "48-49" ]:
    #         logging.warning("%s: %s is not numbers: \"%s\"", iid, label, industry)
    #         # retString.append("must be numbers or one of 31-33, 44-45, 48-49")


    def parseComplex(self, field, inline, labels):
        regex = re.compile(r',+') # parse on one or more consequtive commas
        units = [x.strip() for x in regex.split(inline)]
        retval = []
        for i in units:
            entry = [x.strip() for x in i.split(':')]
            out = {}
            for index, s in enumerate(entry):
                if index > len(labels):
                    logging.warning("%s: failed to parse complex field %s, more entries seperated by colons than labels, skipping", iid, field)
                    return
                elif len(s):
                    out[labels[index]] = s
            if len(out) > 0:
                retval.append(copy.deepcopy(out))
        return retval


    def cleanValue(self, incident, enum):
        v = re.sub("^[,]+", "", incident[enum])
        v = re.sub("[,]+$", "", v)
        v = re.sub("[,]+", ",", v)
        return(v)


    def convertCSV(self, incident):
        cfg = self.cfg

        out = {}
        out['schema_version'] = cfg["file_version"]
        if incident.has_key("incident_id"):
            if len(incident['incident_id']):
                # out['incident_id'] = incident['incident_id']
                # Changing incident_id to UUID to prevent de-anonymiziation of incidents
                m = hashlib.md5(incident["incident_id"])
                out["incident_id"] = str(uuid.UUID(bytes=m.digest())).upper()
            else:
                out['incident_id'] = str(uuid.uuid4()).upper()
        else:
            out['incident_id'] = str(uuid.uuid4()).upper()
        tmp = {}
        for enum in incident: tmp[enum] = self.cleanValue(incident, enum)
        incident = tmp
        for enum in ['source_id', 'reference', 'security_incident', 'confidence', 'summary', 'related_incidents', 'notes']:
            self.addValue(incident, enum, out, "string")
        # victim
        for enum in ['victim_id', 'industry', 'employee_count', 'state',
                'revenue.iso_currency_code', 'secondary.notes', 'notes']:
            self.addValue(incident, 'victim.'+enum, out, "string")
        self.addValue(incident, 'victim.revenue.amount', out, "integer")
        self.addValue(incident, 'victim.secondary.amount', out, "numeric")
        self.addValue(incident, 'victim.secondary.victim_id', out, "list")
        self.addValue(incident, 'victim.locations_affected', out, "integer")
        self.addValue(incident, 'victim.country', out, "list")

        # actor
        for enum in ['motive', 'variety', 'country']:
            self.addValue(incident, 'actor.external.'+enum, out, 'list')
        self.addValue(incident, 'actor.external.notes', out, 'string')
        for enum in ['motive', 'variety']:
            self.addValue(incident, 'actor.internal.'+enum, out, 'list')
        self.addValue(incident, 'actor.internal.notes', out, 'string')
        for enum in ['motive', 'country']:
            self.addValue(incident, 'actor.partner.'+enum, out, 'list')
        self.addValue(incident, 'actor.partner.industry', out, 'string')
        self.addValue(incident, 'actor.partner.notes', out, 'string')

        # action
        action = "malware."
        for enum in ['variety', 'vector']:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['cve', 'name', 'notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "hacking."
        for enum in ['variety', 'vector']:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['cve', 'notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "social."
        for enum in ['variety', 'vector', 'target']:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "misuse."
        for enum in ['variety', 'vector']:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "physical."
        for enum in ['variety', 'vector', 'vector']:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "error."
        for enum in ['variety', 'vector']:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "environmental."
        for enum in ['variety']:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        # asset
        if 'asset.assets.variety' in incident:
            if 'asset' not in out:
                out['asset'] = {}
            if 'assets' not in out['asset']:
                out['asset']['assets'] = []
            assets = self.parseComplex("asset.assets.variety", incident['asset.assets.variety'], ['variety', 'amount'])
            if len(assets):
                for i in assets:
                    if 'amount' in i:
                        if self.isnum(i['amount']) is not None:
                            i['amount'] = self.isnum(i['amount'])
                        else:
                            del i['amount']
                out['asset']['assets'] = copy.deepcopy(assets)

        for enum in ['accessibility', 'ownership', 'management', 'hosting', 'cloud', 'notes']:
            self.addValue(incident, 'asset.' + enum, out, 'string')
        self.addValue(incident, 'asset.country', out, 'list')

        # attributes
        if 'attribute.confidentiality.data.variety' in incident:
            data = self.parseComplex("attribute.confidentiality.data.variety", incident['attribute.confidentiality.data.variety'], ['variety', 'amount'])
            if len(data):
                if 'attribute' not in out:
                    out['attribute'] = {}
                if 'confidentiality' not in out['attribute']:
                    out['attribute']['confidentiality'] = {}
                if 'data' not in out['attribute']['confidentiality']:
                    out['attribute']['confidentiality']['data'] = []
                for i in data:
                    if 'amount' in i:
                        if self.isnum(i['amount']) is not None:
                            i['amount'] = self.isnum(i['amount'])
                        else:
                            del i['amount']
                out['attribute']['confidentiality']['data'] = copy.deepcopy(data)
        self.addValue(incident, 'attribute.confidentiality.data_disclosure', out, 'string')
        self.addValue(incident, 'attribute.confidentiality.data_total', out, 'integer')
        self.addValue(incident, 'attribute.confidentiality.state', out, 'list')
        self.addValue(incident, 'attribute.confidentiality.notes', out, 'string')

        self.addValue(incident, 'attribute.integrity.variety', out, 'list')
        self.addValue(incident, 'attribute.integrity.notes', out, 'string')

        self.addValue(incident, 'attribute.availability.variety', out, 'list')
        self.addValue(incident, 'attribute.availability.duration.unit', out, 'string')
        self.addValue(incident, 'attribute.availability.duration.value', out, 'numeric')
        self.addValue(incident, 'attribute.availability.notes', out, 'string')

        # timeline
        self.addValue(incident, 'timeline.incident.year', out, 'integer')
        self.addValue(incident, 'timeline.incident.month', out, 'integer')
        self.addValue(incident, 'timeline.incident.day', out, 'integer')
        self.addValue(incident, 'timeline.incident.time', out, 'string')

        self.addValue(incident, 'timeline.compromise.unit', out, 'string')
        self.addValue(incident, 'timeline.compromise.value', out, 'numeric')
        self.addValue(incident, 'timeline.exfiltration.unit', out, 'string')
        self.addValue(incident, 'timeline.exfiltration.value', out, 'numeric')
        self.addValue(incident, 'timeline.discovery.unit', out, 'string')
        self.addValue(incident, 'timeline.discovery.value', out, 'numeric')
        self.addValue(incident, 'timeline.containment.unit', out, 'string')
        self.addValue(incident, 'timeline.containment.value', out, 'numeric')

        # trailer values
        for enum in ['discovery_method', 'targeted', 'control_failure', 'corrective_action']:
            self.addValue(incident, enum, out, 'string')
        if 'ioc.indicator' in incident:
            ioc = self.parseComplex("ioc.indicator", incident['ioc.indicator'], ['indicator', 'comment'])
            if len(ioc):
                out['ioc'] = copy.deepcopy(ioc)

        # impact
        for enum in ['overall_min_amount', 'overall_amount', 'overall_max_amount']:
            self.addValue(incident, 'impact.'+enum, out, 'numeric')
        # TODO handle impact.loss varieties
        for enum in ['overall_rating', 'iso_currency_code', 'notes']:
            self.addValue(incident, 'impact.'+enum, out, 'string')
        # plus
        plusfields = ['master_id', 'investigator', 'issue_id', 'casename', 'analyst',
                'analyst_notes', 'public_disclosure', 'analysis_status',
                'attack_difficulty_legacy', 'attack_difficulty_subsequent',
                'attack_difficulty_initial', 'security_maturity' ]
        if cfg["vcdb"]:
            plusfields.append('github')
        for enum in plusfields:
            self.addValue(incident, 'plus.'+enum, out, "string")
        self.addValue(incident, 'plus.dbir_year', out, "integer")
        self.addValue(incident, 'plus.external_region', out, "list") # TODO: Make this change region name to region code. - gdb 06/21/16
        if cfg["vcdb"]:
            self.addValue(incident, 'plus.timeline.notification.year', out, "numeric")
            self.addValue(incident, 'plus.timeline.notification.month', out, "numeric")
            self.addValue(incident, 'plus.timeline.notification.day', out, "numeric")
        # Skipping: 'unknown_unknowns', useful_evidence', antiforensic_measures, unfollowed_policies,
        # countrol_inadequacy_legacy, pci
        # TODO dbir_year

        return out


    def main(self, cfg=None):
        if cfg == None:
            cfg = self.cfg
        else:
            self.__init__(cfg)

        try:
            # Added to file read to catch multiple columns with same name which causes second column to overwrite first. - GDB
            file_handle = open(cfg["input"], 'rU')
            csv_reader = csv.reader(file_handle)
            l = csv_reader.next()
            if len(l) > len(set(l)):
                logging.error(l)
                raise KeyError("Input file has multiple columns of the same name.  Please create unique columns and rerun.")
                # exit(1)
            else:
                file_handle.seek(0)
                infile = csv.DictReader(file_handle)
            # infile = csv.DictReader(open(args.filename,'rU'))  # Old File Read - gdb
        except IOError:
            logging.critical("ERROR: Input file not found.")
            raise
            # exit(1)

        for f in infile.fieldnames:
            if f not in self.sfields:
                if f != "repeat":
                    logging.warning("column will not be used: %s. May be inaccurate for 'plus' columns.", f)
        if 'plus.analyst' not in infile.fieldnames:
            logging.warning("the optional plus.analyst field is not found in the source document")
        if 'source_id' not in infile.fieldnames:
            logging.warning("the optional source_id field is not found in the source document")

        row = 0
        for incident in infile:
            incident = {k.decode('unicode_escape').encode('ascii', 'ignore'):v for k,v in incident.iteritems()} # remove unicode keys - 170130
            row += 1
            # have to look for white-space only and remove it
            try:
                incident = { x:incident[x].strip() for x in incident }
            except AttributeError as e:
                logging.error("Error removing white space from feature {0} on row {1}.".format(x, row))
                raise e

            if 'incident_id' in incident:
                iid = incident['incident_id']
            else:
                iid = "srcrow_" + str(row)
            logging.debug("Starting incident {0} on row {1}.".format(iid, row))
            # logging.warning("This includes the row number")
            repeat = 1
            logging.info("-----> parsing incident %s", iid)
            if incident.has_key('repeat'):
                if incident['repeat'].lower()=="ignore" or incident['repeat'] == "0":
                    logging.info("Skipping row %s because 'repeat' is either 'ignore' or '0'.", iid)
                    continue
                repeat = self.isnum(incident['repeat'])
                if not repeat:
                    repeat = 1
            if incident.has_key('security_incident'):
                if incident['security_incident'].lower()=="no":
                    logging.info("Skipping row %s because security_incident is 'no'.", iid)
                    continue
            outjson = self.convertCSV(incident)

            while repeat > 0:
                if 'plus' not in outjson:
                    outjson['plus'] = {}
                outjson['plus']['master_id'] = str(uuid.uuid4()).upper()
                yield iid, outjson
                # outjson['incident_id'] = str(uuid.uuid4()).upper()     ### HERE
                # outjson['plus']['master_id'] = outjson['incident_id']  ###
                repeat -= 1
                if repeat > 0:
                    logging.info("Repeating %s more times on %s", repeat, iid)


iid = ""  # setting global
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert Standard Excel (csv) format to VERIS 1.3 schema-compatible JSON files")
    parser.add_argument("-i", "--input", help="The csv file containing the data")
    parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument("-m","--mergedfile", help="The fully merged json schema file.")
    parser.add_argument("-s","--schemafile", help="The JSON schema file")
    parser.add_argument("-e","--enumfile", help="The JSON file with VERIS enumerations")
    parser.add_argument("--vcdb",help="Convert the data for use in VCDB",action="store_true")
    parser.add_argument("--version", help="The version of veris in use")
    parser.add_argument('--conf', help='The location of the config file', default="./_checkValidity.cfg")
    parser.add_argument('--year', help='The DBIR year to assign tot he records.')
    parser.add_argument('-c', '--countryfile', help='The json file holdering the country mapping.')
    parser.add_argument('--source', help="Source_id to use for the incidents. Partner pseudonym.")
    parser.add_argument('-a', '--analyst', help="The analyst to use if no analyst exists in record or if --force_analyst is set.")
    parser.add_argument("-f", "--force_analyst", help="Override default analyst with --analyst.", action='store_true')
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("-o", "--output", help="directory where json files will be written")
    output_group.add_argument("--check", help="Generate VERIS json records from the input csv, but do not write them to disk. " + 
                              "This is to allow finding errors in the input csv without creating any files.", action='store_true')
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}

    logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG}

    # Parse the config file
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

    #cfg.update({k:v for k,v in vars(args).iteritems() if k not in cfg.keys()})  # copy command line arguments to the 
    #cfg.update(vars(args))  # overwrite configuration file variables with 
    cfg.update(args)

    cfg["vcdb"] = {True:True, False:False, "false":False, "true":True}[str(cfg.get("vcdb", 'false')).lower()]
    cfg["check"] = {True:True, False:False, "false":False, "true":True}[str(cfg.get("check", 'false')).lower()]
    
    if cfg.get('check', False) == True:
        # _ = cfg.pop('output')
        logging.info("Output files will not be written")
    else:
        logging.info("Output files will be written to %s", cfg["output"])

    # if source missing, try and guess it from directory
    if 'source' not in cfg or not cfg['source']:
        cfg['source'] = cfg['input'].split("/")[-2].lower()
        cfg['source'] = ''.join(e for e in cfg['source'] if e.isalnum())
        logging.warning("Source not defined.  Using the directory of the input file {0} instead.".format(cfg['source']))

    # Quick test to replace any placeholders accidentally left in the config
    # for k, v in cfg.iteritems():
    #     if k not in  ["repositories", "source"] and type(v) == str:
    #         cfg[k] = v.format(repositories=cfg["repositories"], partner_name=cfg["source"])


    # logging.basicConfig(level=logging_remap[cfg["log_level"]],
    #       format='%(asctime)19s %(levelname)8s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    # if cfg["log_file"] is not None:
    #     logging.FileHandler(cfg["log_file"])
    # format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    veris_logger.updateLogger(cfg)

    logging.debug(args)
    logging.debug(cfg)

    importStdExcel = CSVtoJSON(cfg)


    # call the main loop which yields json incidents
    if not cfg.get('check', False):
        logging.info("Output files will be written to %s",cfg["output"])
    else:
        logging.info("'check' setting is {0} so files will not be written.".format(cfg.get('check', False)))
    for iid, incident_json in importStdExcel.main():
        if not cfg.get('check', False):
            # write the json to a file
            if cfg["output"].endswith("/"):
                dest = cfg["output"] + incident_json['plus']['master_id'] + '.json'
                # dest = args.output + outjson['incident_id'] + '.json'
            else:
                dest = cfg["output"] + '/' + incident_json['plus']['master_id'] + '.json'
                # dest = args.output + '/' + outjson['incident_id'] + '.json'
            logging.info("%s: writing file to %s", iid, dest)
            try:
                fwrite = open(dest, 'w')
                fwrite.write(json.dumps(incident_json, indent=2, sort_keys=True))
                fwrite.close()
            except UnicodeDecodeError:
                print incident_json

