#!/usr/bin/python

import simplejson as json
import sys
import os
import csv
import glob
import re

# text file containing the full names of the fields
fieldnames = "keynames-real.txt"
# the name of the output file - if exists, it will overwrite.
outputFile = "veris.csv"
# the filter to read in all the json files
fileglob = "data/*.json"

def getHeader(label):
    temp = re.sub("_", " ", label)
    return ':'.join([ n.capitalize() for n in temp.split('.') ])

def handledict(output, label, datadict, arraylist):
    "general function to determine how to handle value"
    debug = True
    if debug: print "\trunning with label: " + label
    mylist = datadict.items()
    for k,v in mylist:
        alabel = k
        if label:
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


keyfields = []
# F = open("keyfields-pub.txt")

F = open(fieldnames)
rawinput = F.readlines()
for line in rawinput:
    foo = line.strip("\n")
    keyfields.append(foo)

# print out the line here, we are iterated as much as we can be
outfile = open(outputFile, "w")
writer = csv.DictWriter(outfile, fieldnames=keyfields)

keylabels = [ getHeader(label) for label in keyfields ]
headers = {}
for i in range(len(keylabels)):
    headers[keyfields[i]] = keylabels[i]
# headers=dict( (n,n) for n in keyfields)
writer.writerow(headers)


# for filename in glob.glob("src2/vz_Westp-ddb-news*.json"):
for filename in glob.glob(fileglob):
    print filename
    json_data=open(filename).read()
    try:
        data = json.loads(json_data)
    except:
        print sys.argv[1], " Unexpected error:", sys.exc_info()[1]
    debug = True
    output = {}
    arraylist = {}
    handledict(output, "", data, arraylist)
    mylist = arraylist.items()
    print "\t" + "output returned has " + str(len(output)) + " items"
    print output
    keylist = []
    combos = 1
    for k,v in mylist:
        keylist.append(k)
        combos = combos * len(output[k])

    # print "Arrays found in",keylist
    print "\t\t" + str(len(keylist)) + " combinations:",combos
    recursive(output, keylist)
