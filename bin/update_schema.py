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

########### NOT USER EDITABLE ABOVE THIS POINT #################


# USER VARIABLES
cfg = {
    server: "http://192.168.121.134",  # CHANGEME
    port: 7474, # CHANGEME
    conf: "/tmp/verum.cfg",  # CHANGEME
    loglevel: logging.DEBUG,
    log: None
}

########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
from py2neo import neo4j, cypher  # CHANGEME
import networkx as nx  # CHANGEME
import argparse
import ConfigParser

## SETUP
__author__ = "Gabriel Bassett"
logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG,
                 50: logging.CRITICAL, 40: logging.ERROR, 30: logging.WARNING, 20: logging.INFO, 10: logging.DEBUG, 0: logging.CRITICAL}
FORMAT = '%(asctime)19s - %(processName)s - %(levelname)s - {0}%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT.format(""), datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger()



## GLOBAL EXECUTION
# Connect to database
G = neo4j.GraphDatabaseService(NEODB)
g = nx.DiGraph()
NEODB = args.db



## FUNCTION DEFINITION
pass



## MAIN LOOP EXECUTION
def main():
    logging.info('Beginning main loop.')

    logging.info('Ending main loop.')

if __name__ == "__main__":

    ## The general Approach to config parsing (Probably not the best way)
    ## 1. create a dictionary called 'cfg' of fallback values (up at the top of the file)
    ## 2. parse the arguments (args) and turn into a dictionary if the value is not None
    ## 3. Use the config from the command line parser to read the config file and update the 'cfg' dictionary
    ## 4. Update the cfg dictionary with the arguements (args) from the command line

    # Parse Arguments (should correspond to user variables)
    parser = argparse.ArgumentParser(description='This script processes a graph.')
    parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument('--conf', help='The location of the config file')
    # <add arguments here>
    parser.add_argument('--db', help='URL of the neo4j graph database')  # CHANGEME
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}

    # Parse the config file
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(args["conf"]))
        cfg_key = {
            'NEO4J': ['server', 'port'], # CHANGEME
            'LOGGING': ['loglevel', 'log_file']
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

    main()