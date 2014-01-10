#!/usr/bin/python

import simplejson as json
import sys
import os
import csv
import re
import glob

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
           key = key.encode('utf-8')
        if isinstance(value, unicode):
           value = value.encode('utf-8')
        elif isinstance(value, list):
           value = _decode_list(value)
        elif isinstance(value, dict):
           value = _decode_dict(value)
        rv[key] = value
    return rv

def getHeader(label):
    temp = re.sub("_", " ", label)
    return ':'.join([ n.capitalize() for n in temp.split('.') ])

def handledict(output, label, datadict, arraylist):
    "general function to determine how to handle value"
    skip = [ 'partner_data', 'plus' ]
    debug = True
    if debug: print "\trunning with dict label: " + label
    if label.startswith('plus'):
        if debug: print "\tskipping " + label
        return
    mylist = datadict.items()
    for k,v in mylist:
        alabel = k
        if label:
            if k in skip:
                if debug: print "\t\tskipping label: " + k
                continue
            alabel = ".".join([label, k])
            if (label == "actor" or label == "action" or label == "attribute"):
                if output.get(label) is None:
                    output[label] = k.capitalize()
                else:
                    if (type(output[label]) is str):
                        output[label] = [output[label], k.capitalize()]
                        arraylist[label] = 1
                    elif (type(output[label]) is list):
                        output[label].append(k.capitalize())
                        arraylist[label] = 1
        handleAny(output, alabel, v, arraylist)

def handleAny(output, label, v, arraylist):
    "handling any single instance"
    debug = True
    if debug: print "\ttrying to parse " + label
    if (type(v) is dict):
        handledict(output, label, v, arraylist)
    elif (type(v) is str):
        if output.get(label) is not None:
            if (type(output[label]) is str):
                if label.startswith("victim"):
                    print "skipping duplicate victim field..."
                elif label.startswith("plus"):
                    print "skipping all plus extensions..."
                else:
                    if debug: print "\t\t** YES! ** Found string already"
                    output[label] = [output[label], v]
                    arraylist[label] = 1
                    if debug: print "\t\tconverted to list: " + label + " to " + v
            elif (type(output[label]) is list):
                output[label].append(v)
                if debug: print "\t\tappended to list: " + label + " to " + v
                arraylist[label] = 1
            else:
                if debug: print "\t\t---------- > weird, not sure what to do with " + label + ": " + str(type(v))
                if debug: print "\t\tand output label is " + str(type(output[label]))
                if debug: print "\t\tand tempoget is " + str(type(tempoget))
        else:
            if debug: print "\t\tsimply assigning: " + label + " to " + v
            output[label] = v
    elif (type(v) is int):
        if debug: print "\t\tsimply assigning: " + label + " to " + str(v) + " (int)"
        output[label] = v
    elif (type(v) is list):
        for onev in v:
            handleAny(output, label, onev, arraylist)
    else:
        if debug: print "*******unknown type: ", type(v)

def recursive(alldata, localnames):
    "Stare at this long enough and it's quite simple"
    debug = True
    # if debug: print "\t-> attempting to dump " + str(len(alldata))
    if not len(localnames):  # we don't care about order?
        if debug: print "\t-> not length of localnames, dumping as is"
        writer.writerow(alldata)
        return
    localdata = dict(alldata)
    ifield = localnames[0]
    for n in alldata[ifield]:
        localdata[ifield] = n
        if (len(localnames) > 1):
            sendon = localnames[1:len(localnames)]
            recursive(localdata, sendon)
        else:
            writer.writerow(localdata)

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

# load up the schema 
# the full JSON schema (from github)
verisschema = "verisc.json"

json_schema=open(verisschema).read()
try:
    jschema = json.loads(json_schema)
except:
    print "veris schema--Unexpected error:", sys.exc_info()[1]

# load up a list of all the fields expected from the schema
keyfields = parseSchema(jschema, "")

for i in keyfields:
    its = i.split('.')
    if its[0] == "actor" or its[0] == "action" or its[0] == "attribute":
        # newkey = '.'.join([ its[0], its[1] ])
        if its[0] not in keyfields:
            keyfields.append(its[0])

print keyfields

#keyfields = []
#F = open("keyfields-pub.txt")
#rawinput = F.readlines()
#for line in rawinput:
#    foo = line.strip("\n")
#    keyfields.append(foo)

# print out the line here, we are iterated as much as we can be
outfile = open("pubfact-table.csv", "w")
writer = csv.DictWriter(outfile, fieldnames=keyfields)
# headers=dict( (n,n) for n in keyfields)
keylabels = [ getHeader(label) for label in keyfields ]
headers = {}
for i in range(len(keylabels)):
        headers[keyfields[i]] = keylabels[i]

writer.writerow(headers)

# for filename in glob.glob("src2/vz_Westp-ddb-news*.json"):
for filename in glob.glob("../vcdb/data/json/*.json"): # "../github/veris/vcdb/*.json"):
    print "************", filename, "************"
    json_data=open(filename).read()
    try:
        #auto-handling unicode object hook derived from
        #http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-unicode-ones-from-json-in-python
        data = json.loads(json_data, object_hook=_decode_dict)
    except:
        print sys.argv[1], " Unexpected error:", sys.exc_info()[1]
    debug = True
    output = {}
    arraylist = {}
    handledict(output, "", data, arraylist)
    mylist = arraylist.items()
    keylist = []
    combos = 1
    for k,v in mylist:
        keylist.append(k)
        combos = combos * len(output[k])

    # print "Arrays found in",keylist
    print "here"
    print "\t\t" + str(len(keylist)) + " combinations:",combos
    recursive(output, keylist)

#clean up the open file
outfile.close()