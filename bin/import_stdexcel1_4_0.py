#!/usr/bin/python

### As of 18-11-05 I have not updated this or tested it with 1.3.3 veris. - GDB

import json
import csv
import sys
import argparse
import os
import uuid
import hashlib  # convert incident_id to UUID
import copy
import logging
# import multiprocessing # used for multiprocessing logger
import re
from datetime import datetime
import configparser
from collections import defaultdict
import re
import operator
# import imp
import importlib
import zipfile  # to compress

script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    spec = importlib.util.spec_from_file_location("veris_logger", script_dir + "/veris_logger.py")
    veris_logger = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(veris_logger)
    # veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise
import platform  # to get created time

# Default Configuration Settings
cfg = {
    'log_level': 'warning',
    'log_file': None,
    'schemafile': "../verisc.json",
    'enumfile': "../verisc-enum.json",
    'mergedfile': "../verisc-merged.json",
    'vcdb': False,
    'version': "1.4.0",
    'countryfile': 'all.json',
    'output': os.getcwd(),
    'check': False,
    'repositories': "",
    'join': True
}


# logger = multiprocessing.get_logger()

# from https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


class CSVtoJSON():
    """Imports a CSV outputted by the standard excel survey gizmo form"""
    cfg = None
    jschema = None
    sfields = None
    # country_region = None
    script_version = "1.3.6"

    def __init__(self, cfg, file_version=None):
        veris_logger.updateLogger(cfg)
        logging.debug("Initializing CSVtoJSON object.")

        if file_version is None:
            file_version = cfg.get("file_version", None)
        if file_version is None:
            file_version = self.get_file_schema_version(cfg['input'])
        if file_version is None:
            logging.warning(
                "Could not determine veris version of {0}.  Please specify it as an argument to the class initialization, 'CSVtoJSON(cfg, file_version=<file version>)'".format(
                    cfg['input']))
        elif file_version != self.script_version:
            logging.warning("File veris version {0} does not match script veris version {1}.".format(file_version,
                                                                                                     self.script_version))
        cfg['file_version'] = file_version

        if type(cfg["schemafile"]) == dict:
            self.jschema = cfg["schemafile"]
        else:
            try:
                self.jschema = self.openJSON(cfg["schemafile"])
            except IOError:
                logging.critical("ERROR: Schema file not found.")
                raise
                # exit(1)

        self.sfields = self.parseSchema(self.jschema)
        self.cfg = cfg

    def get_file_schema_version(self, inFile):
        logging.info("Reading {0} to determine version.".format(inFile))
        with open(inFile, 'r') as filehandle:
            m = re.compile(r'(\.0+)*$')
            versions = defaultdict(int)
            csv_reader = csv.DictReader(filehandle)
            if "schema_version" in csv_reader.fieldnames:
                for row in csv_reader:
                    versions[m.sub('', row[
                        "schema_version"])] += 1  # the regex removes trailing '.0' to make counting easier
                version = max(versions.items(), key=operator.itemgetter(1))[
                    0]  # return the most common version. (They shoudl all be the same, but, you know.)
                if version not in ["1.2", "1.3", "1.3.1", "1.3.2", "1.3.3", "1.3.4","1.3.5", "1.3.6", "1.3.7", "1.4.0"]:
                    logging.warning(
                        "VERIS version {0} in file {1} does not appear to be a standard version.  \n".format(version,
                                                                                                             inFile) +
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
        if v['type'] == "object":
            for k, v2 in v['properties'].items():
                if len(base):
                    callout = base + "." + k
                else:
                    callout = k
                self.reqSchema(v2, callout, mykeylist)
        elif v['type'] == "array":
            self.reqSchema(v['items'], base, mykeylist)
        return mykeylist

    def parseSchema(self, v, base="", mykeylist=[]):
        "given schema in v, returns a list of concatenated keys in the schema"
        if v['type'] == "object":
            for k, v2 in v['properties'].items():
                if len(base):
                    callout = base + "." + k
                else:
                    callout = k
                self.parseSchema(v2, callout, mykeylist)
        # bypassing plus.event_chain below. It's stored as a serialized json object so we don't need to parse it's items. - GDB 201130
        elif v['type'] == "array" and base != "plus.event_chain":
            self.parseSchema(v['items'], base, mykeylist)
        else:
            mykeylist.append(base)
        return mykeylist

    def isnum(self, x):
        if type(x) not in [int, float]:  # 'long' removed for python3 - GDB 181116
            x = re.sub('[$,]', '', x)
        try:
            x = int(float(x))
        except:
            return None
        return x

    def isfloat(self, x):
        x = re.sub('[$,]', '', x)
        try:
            x = float(x)
        except:
            return
        return x

    def addValue(self, src, enum, dst, val="list"):
        "adding value to dst at key if present in src"
        # if src.has_key(enum):
        if enum in src:
            if len(src[enum]):
                allenum = enum.split('.')
                saved = dst
                for i in range(len(allenum) - 1):
                    # if not saved.has_key(allenum[i]):
                    if allenum[i] not in saved:
                        saved[allenum[i]] = {}
                    saved = saved[allenum[i]]
                if val == "list":
                    templist = [x.strip() for x in src[enum].split(',') if len(x) > 0]
                    saved[allenum[-1]] = [x for x in templist if len(x) > 0]
                elif val == "string":
                    # saved[allenum[-1]] = unicode(src[enum],errors='ignore')
                    # saved[allenum[-1]] = str(src[enum],errors='ignore') # python2
                    saved[allenum[-1]] = src[enum]  # python3 - gdb 181116
                elif val == "numeric":
                    if self.isfloat(src[enum]):
                        saved[allenum[-1]] = self.isfloat(src[enum])
                elif val == "integer":
                    if self.isnum(src[enum]):
                        saved[allenum[-1]] = self.isnum(src[enum])
                elif val == "logical":
                    if src[enum].lower() in ["", "no", "n", 'f', 'false']:
                        saved[allenum[-1]] = False
                    elif src[enum].lower() in ["yes", 'y', 't', 'true']:
                        saved[allenum[-1]] = True
                    elif src[enum] == allenum[
                        -1]:  # if the field and value are the same such as discover_method.unknown == unknown
                        saved[allenum[-1]] = True
                    else:
                        logging.warning("logical column {0} with value {1} did not match any rules. Marking False.")
                        saved[allenum[-1]] = False

    # def self.chkDefault(self, incident, enum, default):
    #     allenum = enum.split('.')
    #     saved = incident
    #     for i in range(len(allenum)-1):
    #         if not saved.has_key(allenum[i]):
    #             saved[allenum[i]] = {}
    #         saved = saved[allenum[i]]
    #     if not saved[allenum[-1]]:
    #         saved[allenum[-1]] = copy.deepcopy(default)

    def openJSON(self, filename):
        parsed = {}
        rawjson = open(filename).read()
        try:
            parsed = json.loads(rawjson)
        except:
            print("Unexpected error while loading", filename, "-", sys.exc_info()[1])
            parsed = None
        return parsed

    def parseComplex(self, field, inline, labels):
        regex = re.compile(r',+')  # parse on one or more consequtive commas
        units = [x.strip() for x in regex.split(inline)]
        retval = []
        for i in units:
            entry = [x.strip() for x in i.split(':')]
            out = {}
            for index, s in enumerate(entry):
                if index > len(labels):
                    logging.warning(
                        "%s: failed to parse complex field %s, more entries seperated by colons than labels, skipping",
                        iid, field)
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
        return (v)

    def convertCSV(self, incident):
        cfg = self.cfg

        out = {}
        out['schema_version'] = cfg["file_version"]
        # if incident.has_key("incident_id"):
        if "incident_id" in incident:
            incident['incident_id'] = str(incident['incident_id'])
            if len(incident['incident_id']):
                # out['incident_id'] = incident['incident_id']
                # Changing incident_id to UUID to prevent de-anonymiziation of incidents
                m = hashlib.md5(incident["incident_id"].encode('utf-8'))
                out["incident_id"] = str(uuid.UUID(bytes=m.digest())).upper()
            else:
                out['incident_id'] = str(uuid.uuid4()).upper()
        else:
            out['incident_id'] = str(uuid.uuid4()).upper()
        tmp = {}
        for enum in incident: tmp[enum] = self.cleanValue(incident, enum)
        incident = tmp
        for enum in ['campaign_id', 'source_id', 'reference', 'security_incident', 'confidence', 'summary',
                     'related_incidents', 'notes', 'schema_name']:
            self.addValue(incident, enum, out, "string")
        # victim
        for enum in ['victim_id', 'industry', 'employee_count', 'state',
                     'revenue.iso_currency_code', 'secondary.notes', 'notes']:
            self.addValue(incident, 'victim.' + enum, out, "string")
        self.addValue(incident, 'victim.revenue.amount', out, "integer")
        self.addValue(incident, 'victim.secondary.amount', out,
                      "integer")  # changed to integer from numeric to match schema. - GDB 181204
        self.addValue(incident, 'victim.secondary.victim_id', out, "list")
        self.addValue(incident, 'victim.locations_affected', out, "integer")
        self.addValue(incident, 'victim.country', out, "list")
        self.addValue(incident, "victim.government", out, "list")

        # actor
        for enum in ['motive', 'variety', 'country']:
            self.addValue(incident, 'actor.external.' + enum, out, 'list')
        self.addValue(incident, 'actor.external.notes', out, 'string')
        for enum in ['motive', 'variety']:
            self.addValue(incident, 'actor.internal.' + enum, out, 'list')
        self.addValue(incident, 'actor.internal.notes', out, 'string')
        for enum in ['motive', 'country']:
            self.addValue(incident, 'actor.partner.' + enum, out, 'list')
        self.addValue(incident, 'actor.partner.industry', out, 'string')
        self.addValue(incident, 'actor.partner.notes', out, 'string')

        # action
        action = "malware."
        for enum in ['variety', 'vector', "result"]:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['cve', 'name', 'notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "hacking."
        for enum in ['variety', 'vector', "result"]:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['cve', 'notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "social."
        for enum in ['variety', 'vector', 'target', "result"]:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "misuse."
        for enum in ['variety', 'vector', "result"]:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "physical."
        for enum in ['variety', 'vector', "result"]:
            self.addValue(incident, 'action.' + action + enum, out, 'list')
        for enum in ['notes']:
            self.addValue(incident, 'action.' + action + enum, out, 'string')
        action = "error."
        for enum in ['variety', 'vector', "result"]:
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

        for enum in ['notes']:  # accessability & governance - obscelete as of 1.3.3 - GDB 181116
            self.addValue(incident, 'asset.' + enum, out, 'string')
        for enum in ['ownership', 'hosting', 'management',
                     'cloud']:  # accessability & governance - obscelete as of 1.3.3 - GDB 181116
            self.addValue(incident, 'asset.' + enum, out, 'list')
        self.addValue(incident, 'asset.country', out, 'list')
        ### cloud now required
        # per vz-risk/VERIS issue #225 and #236
        if 'cloud' not in out.get('asset', {}):
            if 'asset' not in out:
                out['asset'] = {}
            out['asset']['cloud'] = ['Unknown']

        # attributes
        if 'attribute.confidentiality.data.variety' in incident:
            data = self.parseComplex("attribute.confidentiality.data.variety",
                                     incident['attribute.confidentiality.data.variety'], ['variety', 'amount'])
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

        # discovery method  - GDB 181116
        for enum in ["external", "internal", "partner"]:
            self.addValue(incident, 'discovery_method.' + enum + ".variety", out, 'list')
        self.addValue(incident, 'discovery_method.unknown', out, 'logical')
        self.addValue(incident, 'discovery_method.other', out, 'logical')

        # value chain - veris 1.3.3 GDB 181116
        for enum in ["development", "non-distribution services", "targeting", "distribution", "cash-out",
                     "money laundering"]:
            self.addValue(incident, 'value_chain.' + enum, out, 'list')

        # trailer values
        for enum in ['discovery_notes', 'targeted', 'control_failure', 'corrective_action', 'cost_corrective_action']:
            self.addValue(incident, enum, out, 'string')
        if 'ioc.indicator' in incident:
            ioc = self.parseComplex("ioc.indicator", incident['ioc.indicator'], ['indicator', 'comment'])
            if len(ioc):
                out['ioc'] = copy.deepcopy(ioc)

        # impact
        for enum in ['overall_min_amount', 'overall_amount', 'overall_max_amount']:
            self.addValue(incident, 'impact.' + enum, out, 'numeric')
        # handle impact.loss varieties  - GDB 171114
        if incident.get('impact.loss.variety', ''):
            if 'impact' not in out:
                out['impact'] = {}
            if 'loss' not in out['impact']:
                out['impact']['loss'] = []
            losses = self.parseComplex("impact.loss.variety", incident['impact.loss.variety'], ['variety', 'amount'])
            if len(losses):
                for i in losses:
                    if 'amount' in i:
                        if self.isnum(i['amount']) is not None:
                            i['amount'] = self.isnum(i['amount'])
                        else:
                            del i['amount']
                out['impact']['loss'] = copy.deepcopy(losses)
        # Ok, so I lied in the error.  If you have impact.loss.amount and its a number & impact.overall_amount doesn't exist, I'll take impact.loss.amount as impact.overall_amount. - gdb 171114
        if "impact.loss.amount" in incident and self.isnum(
                incident["impact.loss.amount"]) is not None and "overall_amount" not in out.get('impact', {}):
            if 'impact' not in out:
                out['impact'] = {}
            out['impact']['overall_amount'] = self.isnum(incident["impact.loss.amount"])
        for enum in ['overall_rating', 'iso_currency_code', 'notes']:
            self.addValue(incident, 'impact.' + enum, out, 'string')
        # plus
        out['plus'] = {}
        plusfields = ['master_id', 'investigator', 'issue_id', 'casename', 'analyst',
                      'analyst_notes', 'analysis_status',  # 'public_disclosure', - obscelete as of 1.3.3 - GDB 181116
                      'attack_difficulty_legacy', 'attack_difficulty_subsequent',
                      'attack_difficulty_initial', 'security_maturity',
                      'attribute.confidentiality.data_abuse']  # - GDB 181116
        if cfg["vcdb"]:
            plusfields.append('github')
        for enum in plusfields:
            self.addValue(incident, 'plus.' + enum, out, "string")
        self.addValue(incident, 'plus.dbir_year', out, "integer")
        # add plus create/modified
        out['plus']['modified'] = self.cfg['plus.modified']
        out['plus']['created'] = self.cfg['plus.created']
        # self.addValue(incident, 'plus.external_region', out, "list")
        if cfg["vcdb"]:
            self.addValue(incident, 'plus.timeline.notification.year', out, "numeric")
            self.addValue(incident, 'plus.timeline.notification.month', out, "numeric")
            self.addValue(incident, 'plus.timeline.notification.day', out, "numeric")
        # Skipping: 'unknown_unknowns', useful_evidence', antiforensic_measures, unfollowed_policies,
        # countrol_inadequacy_legacy, pci
        if incident.get("plus.event_chain", None):
            try:
                out["plus"]["event_chain"] = json.loads(incident["plus.event_chain"])
            except:
                logging.warning(
                    "plus.event_chain is not valid json to decode: {0}".format(incident["plus.event_chain"]))

        return out

    # def self.getCountryCode(self, countryfile):  # Removed default of 'all.json' - GDB
    #     # Fixed the hard-coded name - GDB
    #     country_codes = json.loads(open(countryfile).read())
    #     country_code_remap = {'Unknown':'000000'}
    #     for eachCountry in country_codes:
    #         try:
    #             country_code_remap[eachCountry['alpha-2']] = eachCountry['region-code']
    #         except:
    #             country_code_remap[eachCountry['alpha-2']] = "000"
    #         try:
    #             country_code_remap[eachCountry['alpha-2']] += eachCountry['sub-region-code']
    #         except:
    #             country_code_remap[eachCountry['alpha-2']] += "000"
    #     return country_code_remap

    def main(self, cfg=None):
        if cfg == None:
            cfg = self.cfg
        else:
            self.__init__(cfg)
        format_design = ("- " + "/".join(cfg["input"].split("/")[-2:]))
        veris_logger.updateLogger(cfg, format_design)

        # formatter = logging.Formatter(FORMAT.format("- " + "/".join(cfg["input"].split("/")[-2:])))
        try:
            # adding created/modified times - GDB 180109
            self.cfg['plus.created'] = datetime.fromtimestamp(creation_date(cfg['input'])).strftime(
                '%Y-%m-%dT%H:%M:%SZ')
            self.cfg['plus.modified'] = datetime.fromtimestamp(os.path.getmtime(cfg['input'])).strftime(
                '%Y-%m-%dT%H:%M:%SZ')
            # Added to file read to catch multiple columns with same name which causes second column to overwrite first. - GDB
            file_handle = open(cfg["input"], 'r')
            csv_reader = csv.reader(file_handle)
            # l = csv_reader.next()
            l = next(csv_reader)
            if len(l) > len(set(l)):
                logging.error(l)
                file_handle.close()
                raise KeyError(
                    "Input file has multiple columns of the same name.  Please create unique columns and rerun.")
                # exit(1)
            else:
                file_handle.seek(0)
                infile = csv.DictReader(file_handle)
            # infile = csv.DictReader(open(args.filename,'rU'))  # Old File Read - gdb
        except IOError:
            logging.critical("ERROR: Input file not found.")
            raise
            # exit(1)

        ## Below unnecessary in python3. - GDB 181116
        ## I think it might still be necessary.  Going to catch the error rather tahn ignore the line completely. - GDB 190122
        try:
            infile.fieldnames = [f.decode('unicode_escape').encode('ascii', 'ignore').decode() for f in
                                 infile.fieldnames]  # remove unicode - gdb 170130
        except AttributeError:  # if we get an attribute error, f is already a string and doesn't need decoding. - GDG 190122
            infile.fieldnames = [f.encode('ascii', 'ignore').decode() for f in
                                 infile.fieldnames]  # remove unicode - gdb 170130

        for f in infile.fieldnames:
            if f not in self.sfields:
                if f != "repeat":
                    logging.warning(
                        "Unless it's 'repeat', column will not be used: \"%s\" and may be inaccurate for 'plus' columns.",
                        f)
        if 'plus.analyst' not in infile.fieldnames:
            logging.warning("the optional plus.analyst field is not found in the source document")
        if 'source_id' not in infile.fieldnames:
            logging.warning("the optional source_id field is not found in the source document")
        if 'impact.loss.amount' in infile.fieldnames:
            logging.error(
                "impact.loss.amount found.  Values in impact.loss.amount WILL NOT be in included in the incident json.  For overall loss amounts, use impact.overall_amount.  For loss variety amounts, in 'impact.loss', populatie it with 'variety1:amount1,variety2:amount2,etc'.")  # added 17114 to deal with lost impact.loss.amount data.

        row = 0
        for incident in infile:
            row += 1
            # have to look for white-space only and remove it
            try:
                incident = {x: incident[x].strip() for x in incident}
            except AttributeError as e:
                logging.error(incident)
                logging.error("Error removing white space on row {0}.".format(row))
                raise e

            # if 'incident_id' in incident:
            #    iid = incident['incident_id']
            # else:
            #    iid = "srcrow_" + str(row)
            # logger.warning("This includes the row number")
            try:
                iid = incident[
                    'incident_id']  # there should always be an incident ID so commented out above. - gdb 061316
            except:
                logging.warning("No incident_id in record.  Using row number instead.")
                incident['incident_id'] = str(row)
                iid = incident['incident_id']
                # logging.error("keys: {0}.".format(incident.keys()))
                # logging.error("keys: {0}.".format(list(incident.keys())))
                # raise

            repeat = 1
            logging.info("-----> parsing incident %s", iid)
            # if incident.has_key('repeat'):
            if 'repeat' in incident:
                if incident['repeat'].lower() == "ignore" or incident['repeat'] == "0":
                    logging.info("Skipping row %s because 'repeat' is either 'ignore' or '0'.", iid)
                    continue
                repeat = self.isnum(incident['repeat'])
                if not repeat:
                    repeat = 1
            # if incident.has_key('security_incident'):
            if 'security_incident' in incident:
                if incident['security_incident'].lower() == "no":
                    logging.info("Skipping row %s because 'security_incident' is 'no'.", iid)
                    continue
            outjson = self.convertCSV(incident)
            # self.country_region = self.getCountryCode(cfg["countryfile"])

            # addRules(outjson)  # moved to add_rules.py, imported and run by import_veris.py. -gdb 06/09/16

            # adding row number to help with reverse tracability in v1.3.1 per issue 112. -gdb 06/09/16
            if 'plus' not in outjson:
                outjson['plus'] = {}
            outjson['plus']['row_number'] = row

            while repeat > 0:
                outjson['plus']['master_id'] = str(uuid.uuid4()).upper()
                # print(outjson['plus']['master_id']) # DEBUG
                yield iid, outjson
                # outjson['incident_id'] = str(uuid.uuid4()).upper()     ### HERE
                # outjson['plus']['master_id'] = outjson['incident_id']  ###
                repeat -= 1
                if repeat > 0:
                    logging.info("Repeating %s more times on %s", repeat, iid)

        file_handle.close()


iid = ""  # setting global
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Convert Standard Excel (csv) format to VERIS 1.3.1 schema-compatible JSON files")
    parser.add_argument("-i", "--input", help="The csv file containing the data")
    parser.add_argument("-l", "--log_level", choices=["critical", "warning", "info", "debug"],
                        help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument("-m", "--mergedfile", help="The fully merged json schema file.")
    parser.add_argument("-s", "--schemafile", help="The JSON schema file")
    parser.add_argument("-e", "--enumfile", help="The JSON file with VERIS enumerations")
    parser.add_argument("--vcdb", help="Convert the data for use in VCDB", action="store_true")
    parser.add_argument("--file_version", help="The version of veris in use")
    parser.add_argument('--conf', help='The location of the config file', default="./_checkValidity.cfg")
    parser.add_argument('--year', help='The DBIR year to assign tot he records.')
    parser.add_argument('-c', '--countryfile', help='The json file holdering the country mapping.')
    parser.add_argument('--source', help="Source_id to use for the incidents. Partner pseudonym.")
    parser.add_argument('-a', '--analyst',
                        help="The analyst to use if no analyst exists in record or if --force_analyst is set.")
    parser.add_argument("-f", "--force_analyst", help="Override default analyst with --analyst.", action='store_true')
    parser.add_argument("-j", "--join", help="output a zip file containing json joined in a single list.",
                        action='store_true')
    parser.add_argument('--size',
                        help='The maximum number of json to join in a list within a single file.  ' + \
                             'If more files exist than the limit, additional files will be created.',
                        type=int,
                        default=25000)
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("-o", "--output", help="directory where json files will be written")
    output_group.add_argument("--check",
                              help="Generate VERIS json records from the input csv, but do not write them to disk. " +
                                   "This is to allow finding errors in the input csv without creating any files.",
                              action='store_true')
    args = parser.parse_args()
    args = {k: v for k, v in vars(args).items() if v is not None}

    try:
        cfg["log_level"] = args['log_level']
    except KeyError:
        pass

    # Parse the config file
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(args["conf"]))
        cfg_key = {
            'GENERAL': ['report', 'input', 'output', 'analysis', 'year', 'force_analyst', 'file_version', 'database',
                        'check'],
            'LOGGING': ['log_level', 'log_file'],
            'REPO': ['veris', 'dbir_private'],
            'VERIS': ['mergedfile', 'enumfile', 'schemafile', 'labelsfile', 'countryfile']
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
        veris_logger.updateLogger(cfg)
        logging.debug("config import succeeded.")
    except Exception as e:
        logging.warning("config import failed.")
        # raise e
        pass

    # cfg.update({k:v for k,v in vars(args).iteritems() if k not in cfg.keys()})  # copy command line arguments to the
    # cfg.update(vars(args))  # overwrite configuration file variables with
    cfg.update(args)
    cfg["vcdb"] = {True: True, False: False, "false": False, "true": True}[str(cfg.get("vcdb", 'false')).lower()]
    cfg["check"] = {True: True, False: False, "false": False, "true": True}[str(cfg.get("check", 'false')).lower()]
    if cfg["mergedfile"] != "../verisc-merged.json" and cfg["schemafile"] == "../verisc.json":
        logging.warning("It appears a mergedfile was defined but not as schemafile.  This script " +
                        "_only_ uses the schemafile and enumfile, not the mergedfile.  You make get results due" +
                        "to default values, but the wrong schema is probably being used.")

    ### Removed below. removing 'output' does nothing. - gdb 082516
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

    veris_logger.updateLogger(cfg)

    logging.debug(args)
    logging.debug(cfg)

    importStdExcel = CSVtoJSON(cfg)

    # call the main loop which yields json incidents
    if not cfg.get('check', False):
        logging.info("Output files will be written to %s", cfg["output"])
    else:
        logging.info("'check' setting is {0} so files will not be written.".format(cfg.get('check', False)))
    # If joining
    if not cfg.get('check', False) and cfg.get('join', True):
        zf = zipfile.ZipFile(os.path.join(cfg["output"].rstrip("/") + "/", cfg['source'] + ".json.zip"), mode='w')
        i = 0  # count incidents
    for iid, incident_json in importStdExcel.main():
        if not cfg.get('check', False):
            if cfg.get('join', True):
                if i % cfg['size'] == 0:
                    if i != 0:
                        try:
                            incidents_str = json.dumps(incidents)
                            zf.writestr(cfg['source'] + "_" + str(int(i // cfg['size']) - 1) + ".json",
                                        incidents_str + "\n",
                                        zipfile.ZIP_DEFLATED)
                        except UnicodeDecodeError:
                            logging.critical("Some kind of unicode error in or before response %s. " + \
                                             "Unfortunately because the JSON is joined, failing rather than moving on.",
                                             iid)
                            raise
                    incidents = [copy.deepcopy(
                        incident_json)]  # if we don't deep copy, we get a reference that has the wrong master_id
                else:
                    incidents.append(copy.deepcopy(
                        incident_json))  # if we don't deep copy, we get a reference that has the wrong master_id
                i += 1
            else:
                # write the json to a file
                dest = cfg["output"].rstrip("/") + '/' + incident_json['plus']['master_id'] + '.json'
                # dest = args.output + '/' + outjson['incident_id'] + '.json'
                logging.info("%s: writing file to %s", iid, dest)
                try:
                    with open(dest, 'w') as fwrite:
                        json.dump(incident_json, fwrite, indent=2, sort_keys=True, separators=(',', ': '))
                except UnicodeDecodeError:
                    logging.critical("Some kind of unicode error in response %s. Movin on.", iid)
                    logging.critical(incident_json)

    if not cfg.get('check', False) and cfg.get('join', True):
        try:
            incidents_str = json.dumps(incidents)
            zf.writestr(cfg['source'] + "_" + str(int(i // cfg['size'])) + ".json",
                        incidents_str + "\n",
                        zipfile.ZIP_DEFLATED)
        except UnicodeDecodeError:
            logging.critical("Some kind of unicode error in or before response %s. " + \
                             "Unfortunately because the JSON is joined, failing rather than moving on.", iid)
            raise
        zf.close()