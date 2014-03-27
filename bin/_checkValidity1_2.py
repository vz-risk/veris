#!/usr/bin/python

import simplejson as json
from jsonschema import Draft3Validator
import sys
import os
import csv
import glob

# leveraging jsonschema 2.0 now

# file with the enumerations
enumfile = "verisc-enum.json"
# the full JSON schema (from github)
verisschema = "verisc.json"
# the fileglob to find files to open and iterate through
fileglobs = [ "veris/*.json" ]

def handleAny(output, label, v):
    "handling any single instance"
    debug = False
    if debug: print "trying to parse " + label
    if (type(v) is dict):
        mylist = v.items()
        for dictkey,dictval in mylist:
            alabel = dictkey
            if label:
                alabel = ".".join([label, dictkey])
            handleAny(output, alabel, dictval)
    elif (type(v) is list):
        for listkey in v:
            handleAny(output, label, listkey)
    elif (type(v) in [str, int, bool]):
        if debug: print "\t** YES! ** Found string already:", label
        if label not in output:
            output.append(label)
        else:
            if debug: print "\tbut found the length of label to be zero:",label
    else:
        if debug: print "*******unknown type: ", type(v)

def compareFromTo(fromArray, toArray):
    retString = []
    if isinstance(fromArray, basestring):
        if fromArray not in toArray:
            retString.append(fromArray)
    else:
        for item in fromArray:
            if item not in toArray:
                retString.append(item)
    return retString

def checkIndustry(industry):
    retString = []
    # if len(industry) != 6:
        # retString.append("must be length of 6")
    if not industry.isdigit():
        retString.append("must be numbers")
    return retString

def parseSchema(v, base, mykeylist=[]):
    "handling any single instance"
    debug = False
    if debug: print "ENTER:",base
    if v['type']=="object":
        if debug: print "trying to parse object"
        for k,v2 in v['properties'].items():
            if len(base):
                callout = base + "." + k
            else:
                callout = k
            if debug: print "  object calling with base of " + base
            parseSchema(v2, callout, mykeylist)
    elif v['type']=="array":
        if debug: print "trying to parse array: "
        if debug: print "  array calling with base of " + base
        parseSchema(v['items'], base, mykeylist)
    else:
        if debug: print "trying to parse " + v['type']
        mykeylist.append(base)
    return mykeylist


# load up the enumerations defintion
enum_data=open(enumfile).read()
try:
    edata = json.loads(enum_data)
except:
    print "error loading enum data:", sys.exc_info()[1]


# Load up list of all the fields expected
# vkeys = [line.strip() for line in open(verisfields)]

# load up the schema 
json_schema=open(verisschema).read()
try:
    jschema = json.loads(json_schema)
except:
    print "veris schema--Unexpected error:", sys.exc_info()[1]

# load up a list of all the fields expected from the schema
vkeys = parseSchema(jschema, "")

print "loaded up ",len(vkeys),"keys"

filecount = 0
for fileglob in fileglobs:
    # print "looking at",fileglob
    for filename in glob.glob(fileglob):
        # print "Loading File:", filename
        # first validate the syntax is valid
        json_data=open(filename).read()
        jdata = {}
        try:
            jdata = json.loads(json_data)
        except:
            print filename, ": While loading JSON, Unexpected error:", sys.exc_info()[1]
    
        if not jdata:
            print filename, ": Error loading this file, skipping further processing"
            continue
        filecount += 1
        # now validate it matches the schema
        v = Draft3Validator(jschema)
        for error in sorted(v.iter_errors(jdata), key=str):
            print filename, "Validator:", error.message
    
        # now validate there aren't any extra fields we aren't expecting 
        output = []
        handleAny(output, "", jdata)
        for lkey in output:
            if lkey not in vkeys:
                print filename, ": unknown key:", lkey
    
        # now go through the enumerations and validate they are expected
        errList = dict()
        if jdata.has_key('security_incident'):
            errList['security_incident'] = compareFromTo(jdata['security_incident'], edata['security_incident'])
        if jdata.has_key('public_disclosure'):
            errList['public_disclosure'] = compareFromTo(jdata['public_disclosure'], edata['public_disclosure'])
        for index,victim in enumerate(jdata['victim']):
            if victim.has_key('employee_count'):
                errList['victim.' + str(index) + '.employee_count'] = compareFromTo(victim['employee_count'], edata['victim']['employee_count'])
            if victim.has_key('industry'):
                errList['victim.' + str(index) + '.industry'] = checkIndustry(victim['industry'])
            if victim.has_key('country'):
                errList['victim.' + str(index) + '.country'] = compareFromTo(victim['country'], edata['country'])
        for actor in ['external', 'internal', 'partner']:
            if jdata['actor'].has_key(actor):
                if jdata['actor'][actor].has_key('motive'):
                    errList['actor.' + actor + '.motive'] = compareFromTo(jdata['actor'][actor]['motive'], edata['actor']['motive'])
                #if jdata['actor'][actor].has_key('role'):
                #    errList['actor.' + actor + '.role'] = compareFromTo(jdata['actor'][actor]['role'], edata['actor']['role'])
                if jdata['actor'][actor].has_key('variety'):
                    errList['actor.' + actor + '.variety'] = compareFromTo(jdata['actor'][actor]['variety'], edata['actor'][actor]['variety'])
                if jdata['actor'][actor].has_key('country'):
                    errList['actor.' + actor + '.country'] = compareFromTo(jdata['actor'][actor]['country'], edata['country'])
                if jdata['actor'][actor].has_key('industry'):
                    errList['actor.' + actor + '.industry'] = checkIndustry(jdata['actor'][actor]['industry'])
        for action in ['malware', 'hacking', 'social', 'misuse', 'physical', 'error', 'environmental']:
            if jdata['action'].has_key(action):
                for method in ['variety', 'vector', 'target', 'location']:
                    if jdata['action'][action].has_key(method):
                        errList['action.' + action + '.' + method] = compareFromTo(jdata['action'][action][method], edata['action'][action][method])
        if jdata.has_key('asset'):
            if jdata['asset'].has_key('assets'):
                for index, asset in enumerate(jdata['asset']['assets']):
                    errList['asset.assets.' + str(index)] = compareFromTo(asset['variety'], edata['asset']['variety'])
                    # errList['asset.assets.' + str(index)] = [ "this help: " + asset['variety'] ]
            for method in ["cloud"]:
                if jdata['asset'].has_key(method):
                    errList['asset.' + method] = compareFromTo(jdata['asset'][method], edata['asset'][method])
                    
        if jdata.has_key('attribute'):
            if jdata['attribute'].has_key('confidentiality'):
                if jdata['attribute']['confidentiality'].has_key('data'):
                    for index, datatype in enumerate(jdata['attribute']['confidentiality']['data']):
                        errList['attribute.confidentiality.data.' + str(index)] = compareFromTo(datatype['variety'], edata['attribute']['confidentiality']['data']['variety'])
                if jdata['attribute']['confidentiality'].has_key('data_disclosure'):
                    errList['attribute.confidentiality.data_disclosure'] = compareFromTo(jdata['attribute']['confidentiality']['data_disclosure'], edata['attribute']['confidentiality']['data_disclosure'])
                if jdata['attribute']['confidentiality'].has_key('state'):
                    errList['attribute.confidentiality.state'] = compareFromTo(jdata['attribute']['confidentiality']['state'], edata['attribute']['confidentiality']['state'])
            for attribute in ['integrity', 'availability']:
                if jdata['attribute'].has_key(attribute):
                    if jdata['attribute'][attribute].has_key('variety'):
                        errList['attribute.' + attribute + '.variety'] = compareFromTo(jdata['attribute'][attribute]['variety'], edata['attribute'][attribute]['variety'])
        if jdata.has_key('timeline'):
            for timeline in ['compromise', 'exfiltration', 'discovery', 'containment']:
                if jdata['timeline'].has_key(timeline):
                    if jdata['timeline'][timeline].has_key('unit'):
                        errList['timeline.' + timeline + '.unit'] = compareFromTo(jdata['timeline'][timeline]['unit'], edata['timeline']['unit'])
        if jdata.has_key('discovery_method'):
            errList['discovery_method'] = compareFromTo(jdata['discovery_method'], edata['discovery_method'])
        if jdata.has_key('cost_corrective_action'):
            errList['cost_corrective_action'] = compareFromTo(jdata['cost_corrective_action'], edata['cost_corrective_action'])
        if jdata.has_key('impact'):
            if jdata.has_key('overall_rating'):
                errList['overall_rating'] = compareFromTo(jdata['impact']['overall_rating'], edata['impact']['overall_rating'])
            if jdata.has_key('iso_currency_code'):
                errList['iso_currency_code'] = compareFromTo(jdata['impact']['iso_currency_code'], edata['iso_currency_code'])
            if jdata['impact'].has_key('loss'):
                for index, loss in enumerate(jdata['impact']['loss']):
                    if loss.has_key('variety'):
                        errList['impact.loss.variety' + str(index)] = compareFromTo(loss['variety'], edata['impact']['loss']['variety'])
                    if loss.has_key('rating'):
                        errList['impact.loss.rating' + str(index)] = compareFromTo(loss['rating'], edata['impact']['loss']['rating'])
        # place any "plus" checks here if you'd like
        # phew, now print out any errors
        for k, v in errList.iteritems():
            if len(v):
                for item in v:
                    print filename, "Invalid Enum:", k, "=> \"" + str(item) + "\""
        # validation rules
        valError = []
        if jdata['action'].has_key('malware'):
            if jdata['attribute'].has_key('integrity'):
                if jdata['attribute']['integrity'].has_key('variety'):
                    if "Software installation" not in jdata['attribute']['integrity']['variety']:
                        valError.append("malware: missing attribute.integrity.variety \"Software installation\" associated with malware")
                else:
                    valError.append("malware: missing integrity [variety section] and variety \"Software installation\" associated with malware")
            else:
                valError.append("malware: missing integrity [entire section] and variety \"Software installation\" associated with malware")
        # any social attribute.integrity.variety = "altered human behavior"
        if jdata['action'].has_key('social'):
            if jdata['attribute'].has_key('integrity'):
                if jdata['attribute']['integrity'].has_key('variety'):
                    if "Alter behavior" not in jdata['attribute']['integrity']['variety']:
                        valError.append("social: missing attribute.integrity.variety \"Alter behavior\" associated with social")
                else:
                    valError.append("social: missing integrity [variety section] and variety \"Alter behavior\" associated with social")
            else:
                valError.append("social: missing integrity [entire section] and variety \"Alter behavior\" associated with social")
        # if social target exists, then it should also be in asset.variety
        if jdata['action'].has_key('social'):
            if jdata['action']['social'].has_key('target'):
                if jdata['asset'].has_key('assets'):
                    variety_list = []
                    for item in jdata['asset']['assets']:
                        if item.has_key('variety'):
                            variety_list.append(item['variety'])
                    for item in jdata['action']['social']['target']:
                        checkItem = "P - " + item
                        if item == "Unknown":
                            checkItem = "P - Other"
                        if checkItem not in variety_list:
                            valError.append("Asset missing: \"" + checkItem + "\" (social target \"" + item + "\" found)")
                else:
                    valError.append("Missing Asset section (social targets are specified")
        # hacking.variety = SQLi then attribute.integrity = "misapproproatiation"
        if jdata['action'].has_key('hacking'):
            if jdata['action']['hacking'].has_key('variety'):
                if "SQLi" in jdata['action']['hacking']['variety']:
                    if jdata['attribute'].has_key('integrity'):
                        if jdata['attribute']['integrity'].has_key('variety'):
                            if "Misappropriation" not in jdata['attribute']['integrity']['variety']:
                                valError.append("SQLi: missing attribute.integrity.variety \"Misappropriation\" associated with SQLi")
                        else:
                            valError.append("SQLi: missing integrity [variety section] and variety \"Misappropriation\" associated with SQLi")
                    else:
                        valError.append("SQLi: missing integrity [entire section] and variety \"Misappropriation\" associated with SQLi")
        if jdata['security_incident']=="Confirmed" and not len(jdata['attribute']):
            valError.append("No attributes listed, but security incident is confirmed?")
    
    
        for k in valError:
            print filename, k
            # if data_disclosure = Y then security compromise must be Confirmed
print "Parse",filecount,"files."
