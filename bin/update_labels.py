#!/usr/bin/env python
"""
 AUTHOR: Gabriel Bassett
 DATE: <01-23-2015>
 DEPENDENCIES: <a list of modules requiring installation>
 Copyright 2015 Gabriel Bassett

 LICENSE:
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.

 DESCRIPTION:
Takes an input labels file, an update labels file, and adds/changes
any labels in the update file but not the labels file

 NOTES:
 <No Notes>

 ISSUES:
 <No Issues>

 TODO:
 <No TODO>

"""
# PRE-USER SETUP
import logging

########### NOT USER EDITABLE ABOVE THIS POINT #################


# USER VARIABLES
cfg = {
    "input": None,
    "update": None,
    "output": None,
    "log_level": "debug",
    "log_file": None
}

########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import ConfigParser
import json

## SETUP
__author__ = "Gabriel Bassett"
logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG,
                 50: logging.CRITICAL, 40: logging.ERROR, 30: logging.WARNING, 20: logging.INFO, 10: logging.DEBUG, 0: logging.CRITICAL}
FORMAT = '%(asctime)19s - %(processName)s - %(levelname)s - {0}%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT.format(""), datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger()



## GLOBAL EXECUTION
pass


## CLASS AND FUNCTION DEFINITION
class objdict(dict):
    def __getattr__(self, name):
        try:
            return self.recursive_getattr(self, name)
        except Exception as e:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        try:
            self.recursive_setattr(self, name, value)
        except:
            raise AttributeError("No such attribute: " + name)
    
    def __delattr__(self, name):
        try:
            self.recursive_delattr(self, name)
        except:
            raise AttributeError("No such attribute: " + name)

    def recursive_setattr(self, o, name, value):
        name = name.split(".", 1)
        if len(name) > 1:
            self.recursive_setattr(o[name[0]], name[1], value)
        else:
            o[name[0]] = value

    def recursive_getattr(self, o, name):
        name = name.split(".", 1)
        if len(name) > 1:
            return self.recursive_getattr(o[name[0]], name[1])
        else:
            return o[name[0]]

    def recursive_delattr(self, o, name):
        name = name.split(".", 1)
        if len(name) > 1:
            self.recursive_delattr(o[name[0]], name[1])
        else:
            del o[name[0]]


def recurse_keys(d, lbl, keys=dict()):
    for k, v in d.iteritems():
        if type(v) == dict:
            keys.update(recurse_keys(v, lbl + "." + k, keys))
        else:
            if lbl[1:] in keys:
                keys[lbl[1:]].add(k)
            else:
                keys[lbl[1:]] = set([k])
    return keys


## MAIN LOOP EXECUTION
def main(cfg):
    logger.info('Beginning main loop.')
    # Open the files
    with open(cfg["input"], 'r') as filehandle:
        inFile = json.load(filehandle)
    with open(cfg["update"], 'r') as filehandle:
        updateFile = json.load(filehandle)

#    inKeys = recurse_keys(inFile, "")
    updateKeys = recurse_keys(updateFile, "")

    oInFile = objdict(inFile)
    oUpdateFile = objdict(updateFile)

    for key in updateKeys.keys():
        # if the key is in the infile, just merge the value
        logger.debug("")
        try:
            value = getattr(oInFile, key)
            value.update(getattr(oUpdateFile, key))
            logger.debug("Updating existing key {0}.".format(key))
            setattr(oInFile, key, value)
        except AttributeError:
            #logger.debug(e.message)
            # dd the key to the schema
            keyList = key.split(".")
            if keyList[0] not in oInFile.keys():
                setattr(oInFile, keyList[0], {})
                logger.debug("Adding root key {0}.".format(keyList[0]))
            for i in range(1, len(keyList)-1):
                if keyList[i] not in getattr(oInFile, ".".join(keyList[:i])):
                    if keyList[0] == "attribute":
                        print "i+1 {0} not in {1}".format(keyList[i]), getattr(oInFile, ".".join(keyList[:i]))
                        print "wiping " + ".".join(keyList[:i]) + " on step " + str(i)
                    setattr(oInFile, ".".join(keyList[:i+1]), {})
            logger.debug("adding key {0}.".format(key))
            setattr(oInFile, key, getattr(oUpdateFile, key))


    logger.info('Ending main loop.')

    return dict(oInFile)

if __name__ == "__main__":

    ## The general Approach to config parsing (Probably not the best way)
    ## 1. create a dictionary called 'cfg' of fallback values (up at the top of the file)
    ## 2. parse the arguments (args) and turn into a dictionary if the value is not None
    ## 3. Use the config from the command line parser to read the config file and update the 'cfg' dictionary
    ## 4. Update the cfg dictionary with the arguements (args) from the command line

    # Parse Arguments (should correspond to user variables)
    parser = argparse.ArgumentParser(description='This script takes a schema labels file and a file of updates to it and adds the updates to the original file.')
    parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument('--conf', help='The location of the config file')
    parser.add_argument('--input', required=True, help='The labels file to be updated.')
    parser.add_argument('--update', required=True, help='The labels file to update the input file with (only additions/modifications to labels.)')
    parser.add_argument('--output', required=True, help='The labels file to be outputted.')
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}

    # Parse the config file
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(args["conf"]))
        cfg_key = {
            'GENERAL': ['input', 'update', 'output'], 
            'LOGGING': ['log_level', 'log_file']
        }
        for section in cfg_key.keys():
            if config.has_section(section):
                for value in cfg_key[section]:
                    if value.lower() in config.options(section):
                        cfg[value] = config.get(section, value)
        logger.debug("config import succeeded.")
    except Exception as e:
        logger.warning("config import failed with error {0}.".format(e))
        #raise e
        pass

    cfg.update(args)

    #formatter = logging.Formatter(FORMAT.format("- " + "/".join(cfg["input"].split("/")[-2:])))
    formatter = logging.Formatter(FORMAT.format(""))
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

    logger.debug(args)
    logger.debug(cfg)

    outFile = main(cfg)

    with open(cfg["output"], 'w') as filehandle:
        json.dump(outFile, filehandle, indent=2, sort_keys=True)