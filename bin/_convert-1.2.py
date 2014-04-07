#!/usr/bin/python

import simplejson as json
import sys
import os
import csv
import glob
import re
import copy

# set globs to "source" : "dest" for json files
# can create more than one if multiple locations
globs = { "veris/*.json" : "new-veris/" }

json_data=open("country_to_code.json").read()
countryMap = json.loads(json_data)
to_version = "1.2"

def fixCountry(country):
    # convert to 1.1 naming
    if country=="Russian Federation":
        country = "Russia"
    if country=="United States of America":
        country = "United States"
    if country=="":
        country = "Unknown"
    # convert to 1.2 naming
    if countryMap.has_key(country):
        country = countryMap[country]
    elif len(country) > 2 and not (country=="Unknown" or country=="Other"):
        print filename, "Invalid Country Found:", country
    return country


for g,outprefix in globs.items():
    print g, outprefix
    for filename in glob.glob(g):
        # print filename
        json_data=open(filename).read()
        try:
            incident = json.loads(json_data)
        except:
            print filename, " Unexpected error:", sys.exc_info()[1]
        ##
        ## Top level variables
        ##
        incident['schema_version'] = to_version
        if incident.has_key('security_compromise'):
            incident['security_incident'] = incident.pop('security_compromise')
            if incident['security_incident'] == "No":
                incident['security_incident'] = "Near miss"  # we have not entered False Alarms
    
    
        ##
        ## Victim
        ##
        if incident.has_key('victim'):
            for n,i in enumerate(incident['victim']):
                if incident['victim'][n].has_key('country'):
                    # print "found victim country",incident['victim'][n]['country'],"to",fixCountry(incident['victim'][n]['country'])
                    incident['victim'][n]['country'] = fixCountry(incident['victim'][n]['country'])
                    # print "now victim country",incident['victim'][n]['country']
        ##
        ## Actor
        ##
        if incident.has_key('actor'):
            if incident['actor'].has_key('external'):
                if incident['actor']['external'].has_key('country'):
                    for n,i in enumerate(incident['actor']['external']['country']):
                        incident['actor']['external']['country'][n] = fixCountry(i)
                if incident['actor']['external'].has_key('variety'):
                    for n,i in enumerate(incident['actor']['external']['variety']):
                        if i=="State-sponsored":
                            incident['actor']['external']['variety'][n] = "State-affiliated"
                if incident['actor']['external'].has_key('role'):
                    incident['actor']['external'].pop("role", None)
            if incident['actor'].has_key('internal'):
                if incident['actor']['internal'].has_key('variety'):
                    for n,i in enumerate(incident['actor']['internal']['variety']):
                        if i=="Administrator":
                            incident['actor']['internal']['variety'][n] = "System admin"
                if incident['actor']['internal'].has_key('role'):
                    incident['actor']['internal'].pop("role", None)
            if incident['actor'].has_key('partner'):
                if incident['actor']['partner'].has_key('country'):
                    for n,i in enumerate(incident['actor']['partner']['country']):
                        incident['actor']['partner']['country'][n] = fixCountry(i)
                if incident['actor']['partner'].has_key('role'):
                    incident['actor']['partner'].pop("role", None)
        ##
        ## Action
        ##
        if incident.has_key('action'):
            if incident['action'].has_key('malware'):
                if incident['action']['malware'].has_key('variety'):
                    for n,i in enumerate(incident['action']['malware']['variety']):
                        if i=="Client-side":
                            incident['action']['malware']['variety'][n] = "Client-side attack"
                        if i=="Spyware":
                            incident['action']['malware']['variety'][n] = "Spyware/Keylogger"
                        if i=="Utility":
                            incident['action']['malware']['variety'][n] = "Adminware"
                if incident['action']['malware'].has_key('cve'):
                    if isinstance(incident['action']['malware']['cve'], list):
                        incident['action']['malware']['cve'] = ', '.join(incident['action']['malware']['cve'])
                if incident['action']['malware'].has_key('name'):
                    if isinstance(incident['action']['malware']['name'], list):
                        incident['action']['malware']['name'] = ', '.join(incident['action']['malware']['name'])
            if incident['action'].has_key('hacking'):
                if incident['action']['hacking'].has_key('variety'):
                    for n,i in enumerate(incident['action']['hacking']['variety']):
                        if i=="Backdoor or C2":
                            incident['action']['hacking']['variety'][n] = "Use of backdoor or C2"
                        if i=="Stolen creds":
                            incident['action']['hacking']['variety'][n] = "Use of stolen creds"
                if incident['action']['hacking'].has_key('vector'):
                    for n,i in enumerate(incident['action']['hacking']['vector']):
                        if i=="Shell":
                            incident['action']['hacking']['vector'][n] = "Command shell"
                if incident['action']['hacking'].has_key('cve'):
                    if isinstance(incident['action']['hacking']['cve'], list):
                        incident['action']['hacking']['cve'] = ', '.join(incident['action']['hacking']['cve'])
                if incident['action']['hacking'].has_key('name'):
                    if isinstance(incident['action']['hacking']['name'], list):
                        incident['action']['hacking']['name'] = ', '.join(incident['action']['hacking']['name'])
            if incident['action'].has_key('social'):
                if incident['action']['social'].has_key('target'):
                    for n,i in enumerate(incident['action']['social']['target']):
                        if i=="Administrator":
                            incident['action']['social']['target'][n] = "System admin"
        ##
        ## Asset
        ##
        if incident.has_key('asset'):
            if incident['asset'].has_key('assets'):
                for n,i in enumerate(incident['asset']['assets']):
                    if incident['asset']['assets'][n].has_key('variety'):
                        if incident['asset']['assets'][n]['variety'] == "P - Administrator":
                            incident['asset']['assets'][n]['variety'] = "P - System admin"
                        if incident['asset']['assets'][n]['variety'] == "U - ATM":
                            incident['asset']['assets'][n]['variety'] = "T - ATM"
                        if incident['asset']['assets'][n]['variety'] == "U - Gas terminal":
                            incident['asset']['assets'][n]['variety'] = "T - Gas terminal"
                        if incident['asset']['assets'][n]['variety'] == "U - PED pad":
                            incident['asset']['assets'][n]['variety'] = "T - PED pad"
                        if incident['asset']['assets'][n]['variety'] == "U - Kiosk":
                            incident['asset']['assets'][n]['variety'] = "T - Kiosk"
                        if incident['asset']['assets'][n]['variety'] == "S - Other server":
                            incident['asset']['assets'][n]['variety'] = "S - Other"
            if incident['asset'].has_key('personal'):
                if isinstance(incident['asset']['personal'], bool):
                    if incident['asset']['personal'] == True:
                        incident['asset']['ownership'] = "Employee"
                    else:
                        incident['asset']['ownership'] = "Unknown"
                incident['asset'].pop("personal", None)
            if incident['asset'].has_key('management'):
                if isinstance(incident['asset']['management'], bool):
                    if incident['asset']['management'] == True:
                        incident['asset']['management'] = "External"
                    else:
                        incident['asset']['management'] = "Unknown"
            if incident['asset'].has_key('hosting'):
                if isinstance(incident['asset']['hosting'], bool):
                    if incident['asset']['hosting'] == True:
                        incident['asset']['hosting'] = "External"
                    else:
                        incident['asset']['hosting'] = "Unknown"
            if incident['asset'].has_key('cloud'):
                incident['asset']['cloud'] = "Unknown"
        ##
        ## Attributes
        ##
        if incident.has_key('attribute'):
            if incident['attribute'].has_key('integrity'):
                if incident['attribute']['integrity'].has_key('variety'):
                    for n,i in enumerate(incident['attribute']['integrity']['variety']):
                        if i=="Modified configuration":
                            incident['attribute']['integrity']['variety'][n] = "Modify configuration"
                        if i=="Modified privileges":
                            incident['attribute']['integrity']['variety'][n] = "Modify privileges"
                        if i=="Modified data":
                            incident['attribute']['integrity']['variety'][n] = "Modify data"
    
    
        ##
        ## Timeline
        ##
        if incident.has_key('timeline'):
            if incident['timeline'].has_key('investigation'):
                incident['timeline'].pop("investigation", None)
        # remove investigations

        # some other checks that I'll probably remove
        if incident.has_key('impact'):
            if not incident.has_key('overall_rating'):
                incident['impact']['overall_rating'] = "Unknown" 
        else:
            incident['impact'] = {}
            incident['impact']['overall_rating'] = "Unknown"
        if incident['action'].has_key('social'):
            if incident['attribute'].has_key('integrity'):
                if incident['attribute']['integrity'].has_key('variety'):
                    if "Alter behavior" not in incident['attribute']['integrity']['variety']:
                        incident['attribute']['integrity']['variety'].append("Alter behavior")
                else:
                    incident['attribute']['integrity']['variety'] = [ "Alter behavior" ]
            else:
                incident['attribute']['integrity'] = {}
                incident['attribute']['integrity']['variety'] = [ "Alter behavior" ]
        if incident['action'].has_key('malware'):
            if incident['attribute'].has_key('integrity'):
                if incident['attribute']['integrity'].has_key('variety'):
                    if "Software installation" not in incident['attribute']['integrity']['variety']:
                        incident['attribute']['integrity']['variety'].append("Software installation")
                else:
                    incident['attribute']['integrity']['variety'] = [ "Software installation" ]
            else:
                incident['attribute']['integrity'] = {}
                incident['attribute']['integrity']['variety'] = [ "Software installation" ]
        if incident['action'].has_key('hacking'):
            if incident['action']['hacking'].has_key('variety'):
                if "SQLi" in incident['action']['hacking']['variety']:
                    if incident['attribute'].has_key('integrity'):
                        if incident['attribute']['integrity'].has_key('variety'):
                            if "Misappropriation" not in incident['attribute']['integrity']['variety']:
                                incident['attribute']['integrity']['variety'].append("Misappropriation")
                        else:
                            incident['attribute']['integrity']['variety'] = [ "Misappropriation" ]
                    else:
                        incident['attribute']['integrity'] = {}
                        incident['attribute']['integrity']['variety'] = [ "Misappropriation" ]
            if incident['action'].has_key('social'):
                if incident['action']['social'].has_key('target'):
                    if incident['asset'].has_key('assets'):
                        variety_list = []
                        for item in incident['asset']['assets']:
                            if item.has_key('variety'):
                                variety_list.append(item['variety'])
                        for item in incident['action']['social']['target']:
                            checkItem = "P - " + item
                            if item == "Unknown":
                                checkItem = "P - Other"
                            if checkItem not in variety_list:
                                # hope this exists and is an array
                                incident['asset']['assets'].append({ 'variety' : checkItem })
                    else:
                        incident['asset']['assets'] = []
                        for item in incident['action']['social']['target']:
                            checkItem = "P - " + item
                            if item == "Unknown":
                                checkItem = "P - Other"
                            if checkItem not in variety_list:
                                incident['asset']['assets'].append({ 'variety' : checkItem })
        
        if incident['asset'].has_key("assets"):
            if any("POS" in s['variety'] for s in incident['asset']['assets']):
                if incident['action'].has_key('hacking'):
                    if "Desktop sharing" in incident['action']['hacking']['vector']:
                        if incident['asset']['management'] == "External" or incident['asset']['hosting'] == "External":
                            print filename, "Partner vector"
                            incident['action']['hacking']['vector'].append("Partner")


        dest = outprefix + os.path.split(filename)[-1]
        # print dest
        fwrite  = open(dest, 'w')
        fwrite.write(json.dumps(incident, indent=2))
        fwrite.close()

