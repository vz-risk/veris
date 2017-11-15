#!/usr/bin/env python
"""
 AUTHOR: Gabriel Bassett
 DATE: 06-07-16
 DEPENDENCIES: <a list of modules requiring installation>

 DESCRIPTION:
 <A description of the software>

 NOTES:
 <No Notes>

 ISSUES:
 <No Issues>

 TODO:
 <No TODO>

"""
# PRE-USER SETUP
import logging
import os
import imp
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise


########### NOT USER EDITABLE ABOVE THIS POINT #################


# USER VARIABLES
LOGLEVEL = logging.DEBUG
LOG = None
FORMAT = {
    "string": "free text",
    "array": "enum",
    "number": "integer",
    "integer": "integer",
    "list": "enum",
    "boolean": "true/false"
}
FORMAT_OVERRIDE = {
    "victim.secondary.victim_id": "free text",
    "security_incident": "enum",
    "confidence": "enum",
    "victim.empoyee_count": "enum",
    "victim.revenue.iso_currency_code": "enum",
    "actor.partner.industry": "enum",
    "asset.cloud": "enum",
    "attribute.confidentiality.state": "enum",
    "attribute.confidentiality.data_disclosure": "enum",
    "attribute.availability.duration.unit": "enum",
    "timeline.compromise.unit": "enum",
    "timeline.exfiltration.unit": "enum",
    "timeline.containment.unit": "enum",
    "timeline.discovery.unit string": "enum",
    "discovery_method": "enum",
    "targeted": "enum",
    "cost_corrective_action": "enum",
    "impact.overall_rating": "enum",
    "impact.loss.variety": "enum",
    "impact.loss.rating": "enum",
    "impact.iso_currency_code": "enum",
    "attribute.availability.duration.value": "float",
    "attribute.availability.duration.value": "float",
    "timeline.compromise.value": "float",
    "timeline.exfiltration.value": "float",
    "timeline.containment.value": "float",
    "timeline.discovery.value": "float",
    "impact.overall_min_amount": "float",
    "impact.overall_amount": "float",
    "impact.overall_max_amount": "float",
    "impact.loss.min_amount": "float",
    "impact.loss.amount": "float",
    "impact.loss.max_amount": "float"
}
NOTES = {
    "repeat": "# of how many times to repeat this row, or \"ignore\" to simply skip the entire record",
    "incident_id": "leave blank for auto-generation of incident ID.  Any incident_id will be hashed to a UUID to ensure anonymity.",
    "campaign_id": "generate a UUID and put it into the fields of related incidents",
    "victim.industry": "NAICS code.  2-6 numbers, with \"00\" representing unknown",
    "victim.country": "2-char ISO country code",
    "victim.secondary.amount": "will not understand abbreviations e.g. \"10 million\ is an error, should be \"10000000\"",
    "victim.revenue.amount": "will not understand abbreviations e.g. \"10 million\ is an error, should be \"10000000\"",
    "asset.assets.variety": "optionally, amount seperated by \":\", e.g. \"S - File:2, U - Desktop:10\"",
    "attribute.confidentiality.data.variety": "optionally, amount seperated by \":\", e.g. \"Payment:2000, Credentials\", (blank amounts are treated as unknown)",
    "attribute.availability.duration.value": "decimals allowed",
    "impact.loss.variety": "optionally, amount separated by \":\", e.g. \"Asset and fraud, Legal and regulatory:5000, Response and recovery: 1000000\", (blank amounts are treated as unknown).  Place total amounts where you don't know the variety in \"impact.total_amount\"."
}
ORDER = [
    "repeat",
    "incident_id",
    "source_id",
    "reference",
    "confidence",
    "summary",
    "campaign_id",
    "notes",
    "timeline",
    "victim",
    "actor",
    "action",
    "assest",
    "attribute",
    "discovery_method",
    "discovery_notes",
    "targeted"
]
DEFAULT_COLUMNS = [
    "repeat",
    "incident_id"
]
ENUMS_OVERRIDE = {
    "actor.external.country": "country",
    "actor.partner.country": "country",
    "asset.country": "country",
    "victim.country": "country",
    "impact.iso_currency_code": "iso_currency_code",
    "victim.revenue.iso_currency_code": "iso_currency_code"
}
INFILE = "../verisc-merged.json"
OUTFILE = "../VERIS_Standard_Excel.xlsx"
LABELS = "../verisc-labels.json"
MAX_EXAMPLES = 20


########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import json
import xlsxwriter
import glob
import random

## SETUP
__author__ = "Gabriel Bassett"

# Parse Arguments (should correspond to user variables)
parser = argparse.ArgumentParser(description='This script generates the VERIS_Standard_Excel.xlsx file from the veris schema.')
parser.add_argument('-d', '--debug',
                    help='Print lots of debugging statements',
                    action="store_const", dest="loglevel", const=logging.DEBUG,
                    default=LOGLEVEL
                   )
parser.add_argument('-v', '--verbose',
                    help='Be verbose',
                    action="store_const", dest="loglevel", const=logging.INFO
                   )
parser.add_argument('--log', help='Location of log file', default=LOG)
parser.add_argument('-s', '--schema', help='The merged schema file to generate the standard excel file based on.', default=INFILE)
parser.add_argument('-l', '--labels', help='If desired, include a labels file and they will be included in the standard excel.', default=LABELS)
parser.add_argument('-t', '--test_examples', help=  'A directory of veris json files to convert to examples. ' +
                                                    '(VCDB is a good option for this, but note the VCDB schema is not the same as verisc.) ' +
                                                    'If more than {0}, {0} will be randomly chosen.'.format(MAX_EXAMPLES), type=str, default=None)
parser.add_argument('-o', '--output', help='The excel file name to write (including xlsx extension).', default=OUTFILE)
args = parser.parse_args()

filename=None
level=None
## Set up Logging
if args.log is not None:
    filename=args.log
    level=args.loglevel
else:
    level=args.loglevel

cfg = {
    'log_level': level,
    'log_file': filename
}


## GLOBAL EXECUTION
with open(args.schema, 'r') as filehandle:
    schema = json.load(filehandle)

try:
    with open(args.labels, 'r') as filehandle:
        labels = json.load(filehandle)
    add_labels = True
except:
    add_labels = False


## FUNCTION DEFINITION
def recurse_schema(d, lbl, name):
    keys=set()
    enums=dict()
    if d['type'] == "object":
        lbl = lbl + "properties."
        for k, v in d['properties'].iteritems():
            r_k, r_e = recurse_schema(v, lbl, name + "." + k)
            keys = keys.union(r_k)
            enums.update(r_e)
    elif d['type'] == "array":
        lbl = lbl + "items."
        r_k, r_e = recurse_schema(d['items'], lbl, name)
        keys = keys.union(r_k)
        enums.update(r_e)
    else:
        keys.add((name[1:], d['type']))
        if 'enum' in d:
            enums[name[1:]] = d['enum']
    return keys, enums


def recurse_labels(d, name):
    labels_list=dict()
    for k, v in d.iteritems():
        if type(v) == dict:
            labels_list.update(recurse_labels(v, name + "." + k))
        else:
            if name[1:] in labels_list:
                labels_list[name[1:]].append((k, v))
            else:
                labels_list[name[1:]] = [(k, v)]
    return labels_list


def recurse_veris(o, name):
    flat_dict=dict()
    if type(o) == dict:
        for k, v in o.iteritems():
            flat_dict.update(recurse_veris(v, name + "." + k))
    elif type(o) == list:
        for item in o:
            if type(item) == dict:
                    if "amount" in item:
                        enum = u"{0}:{1}".format(item["variety"], item['amount'])
                    else:
                        enum = u'{0}'.format(item["variety"])
                    if name[1:] + ".variety" in flat_dict:
                        flat_dict[name[1:] + ".variety"] = flat_dict[name[1:] + ".variety"] + ",{0}".format(enum)
                    else:
                        flat_dict[name[1:] + ".variety"] = u"{0}".format(enum)
            else:
                if name[1:] in flat_dict:
                    flat_dict[name[1:]] = flat_dict[name[1:]] + u",{0}".format(item)
                else:
                    flat_dict[name[1:]] = u"{0}".format(item)
    else:
        flat_dict[name[1:]] = unicode(o)
    return flat_dict

## MAIN LOOP EXECUTION
def main():
    veris_logger.updateLogger(cfg)
    logging.info('Beginning main loop.')

    # Create spreadsheets
    workbook = xlsxwriter.Workbook(args.output)
    list_of_headings = workbook.add_worksheet("List of Headings")
    enumerations = workbook.add_worksheet("Enumerations")
    example = workbook.add_worksheet("Example")

    # Pull in objects and type from verisc.json  Maybe add format. Add some ordering.  Add some hard-coded notes.  Add hard-coded order.
    row = 0
    keynames, keyenums = recurse_schema(schema, "", "")
    sorted_keynames = []
    for i in range(len(ORDER)):
        sorted_keynames = sorted_keynames + sorted([k for k in keynames if k[0].startswith(ORDER[i])])
    sorted_keynames = sorted_keynames + sorted(list(set(keynames).difference(sorted_keynames)))
    list_of_headings.write(row, 0, "keyname")
    list_of_headings.write(row, 1, "format")
    list_of_headings.write(row, 2, "notes")
    row += 1
    for keyname, keytype in sorted_keynames:
        list_of_headings.write(row, 0, keyname)
        list_of_headings.write(row, 1, FORMAT_OVERRIDE.get(keyname, FORMAT[keytype]))
        list_of_headings.write(row, 2, NOTES.get(keyname, ""))
        row += 1

    # Object, enumeration, (probably label too)
    if add_labels:
        # parse enums and labels from labels file
        labels_dict = recurse_labels(labels, "")
        sorted_labels_list = []
        for i in range(len(ORDER)):
            sorted_labels_list = sorted_labels_list + sorted([{k: labels_dict[k]} for k in labels_dict.keys()  if k.startswith(ORDER[i])])
        missing_keys = set(labels_dict.keys()).difference([k.keys()[0] for k in sorted_labels_list])
        for k in missing_keys:
            sorted_labels_list.append({k: labels_dict[k]})
        # parse enums from schema
        row = 0
        enumerations.write(row, 0, "Enumerations for {0}".format(schema['description']))
        row += 1
        enumerations.write(row, 0, "keyname")
        enumerations.write(row, 1, "enumeration")
        enumerations.write(row, 2, "label")
        row += 1
        for keyname in  sorted_labels_list:
            k = keyname.keys()[0]
            enumerations.write(row, 0, k)
            for enum_label in keyname[k]:
                enumerations.write(row, 1, enum_label[0])
                enumerations.write(row, 2, enum_label[1])
                row += 1
    else:
        # parse enums from schema
        sorted_schema_list = []
        for i in range(len(ORDER)):
            sorted_schema_list = sorted_schema_list + sorted([{k: keyenums[k]} for k in keyenums.keys()  if k.startswith(ORDER[i])])
        missing_keys = set(keyenums.keys()).difference([k.keys()[0] for k in sorted_schema_list])
        for k in missing_keys:
            sorted_schema_list.append({k: keyenums[k]})
        row = 0
        enumerations.write(row, 0, "Enumerations for {0}".format(schema['description']))
        row += 1
        enumerations.write(row, 0, "keyname")
        enumerations.write(row, 1, "enumeration")
        row += 1
        for keyname in  sorted_schema_list:
            k = keyname.keys()[0]
            enumerations.write(row, 0, k)
            for enum in keyname[k]:
                enumerations.write(row, 1, enum)
                row += 1


    # Build examples from Test VERIS records.
    if args.test_examples is not None:
        try:
            if not os.path.isdir(args.test_examples): raise ValueError("Directory does not exist.")
            testfiles = glob.glob(args.test_examples.rstrip("/") + "/*.json")
            if len(testfiles) <= 0: raise ValueError("No test files found in directory.")
            if len(testfiles) > MAX_EXAMPLES:
                testfiles = random.sample(testfiles, MAX_EXAMPLES)
            #logging.debug(testfiles)
            # read in and flatten files
            records = []
            for filename in testfiles:
                with open(filename, 'r') as filehandle:
                    j = json.load(filehandle)
                    #logging.debug(j)
                    record = recurse_veris(j, "")
                    #logging.debug(record)
                records.append(record)
            # get columns
            columns = set(DEFAULT_COLUMNS)
            for record in records:
                #logging.debug(record.keys())
                columns = columns.union(record.keys())
            #logging.debug(columns)
            # order columns
            sorted_columns = []
            for i in range(len(ORDER)):
                sorted_columns = sorted_columns + sorted([k for k in columns if k.startswith(ORDER[i])])
            sorted_columns = sorted_columns + sorted(list(set(columns).difference(sorted_columns)))
            #logging.debug(sorted_columns)
            # write header
            row = 0
            for i in range(len(sorted_columns)):
                example.write(row, i, sorted_columns[i])
            row += 1
            #logging.debug(records)
            for record in records:
                for k, v in record.iteritems():
                    example.write(row, sorted_columns.index(k), v)
                row += 1
            # add a 'repeat' for the last 2
            example.write(row-2, 0, 25) # 25 is just hardcoded number for example
            example.write(row-1, 0, 5) # 5 is just hardcoded number for example
        except:
            logging.info("No test files found.")

    workbook.close()
    logging.info('Ending main loop.')

if __name__ == "__main__":
    main()
