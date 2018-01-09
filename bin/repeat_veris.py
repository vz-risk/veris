#!/usr/bin/env python
"""
 AUTHOR: Gabriel Bassett
 DATE: 2018
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
 A quick script to duplicate incidents

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
LOGLEVEL = logging.DEBUG
LOG = None

########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import simplejson
from datetime import datetime
import uuid
import os
import copy

## SETUP
__author__ = "Gabriel Bassett"

# Parse Arguments (should correspond to user variables)
parser = argparse.ArgumentParser(description='This script duplicates incidents')
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
# <add arguments here>
parser.add_argument('-i', '--input', help='Incident VERIS JSON _file_ to duplicate') 
parser.add_argument('-o', '--output', help='Output _directory_ for duplicates. If not included, the directory of the input file will be used.', default=None) 
parser.add_argument('-r', '--repeats', help='The number of times to repeat the incident.  ' + 
                                            'If the incident happened 10 times, put in 9, (9 repeats + the original).', type=int)
parser.add_argument('--same', help='By default, the incident_id will be set to the new master_id.  ' + 
                                   'In some specific cases, it may be correct to keep the incident_id the same. (For example, if it was the same incident ' +
                                   'but resulted in several incidents at various companies, this can be used to generate duplicates and the victim information' +
                                   'changed manually.)  If you are unsure, _do not use this_.', action="store_true")
args = parser.parse_args()

## Set up Logging
if args.log is not None:
    logging.basicConfig(filename=args.log, level=args.loglevel)
else:
    logging.basicConfig(level=args.loglevel)
# <add other setup here>


## GLOBAL EXECUTION
# Convert args to a dictionary
args = {k:v for k,v in vars(args).iteritems() if v is not None}


## FUNCTION DEFINITION
pass



## MAIN LOOP EXECUTION
def main(args):
    logging.info('Beginning main loop.')
    if 'output' not in args.keys():
        args['output'] = os.path.dirname(args['input'])
        logging.info('No output path supplied so setting it to {0}'.format(args['output']))

    logging.info("About to repeat incident {0} {1} times resulting in {2} total incidents (repeats + 1 original) stored to {3}".format(args['input'], args['repeats'], args['repeats'] + 1, args['output']))
    with open(args['input'], 'r') as filehandle:
        incident = simplejson.load(filehandle)
        if 'plus' not in incident.keys():
            raise KeyError("A plus section must exist in the incident to duplicate.  Please ensure this is a complete VERIS incident JSON file.")
    for i in range(args['repeats']):
        incident_copy = copy.deepcopy(incident)
        # update the master and incident_id's
        incident_copy['plus']['master_id'] = str(uuid.uuid4()).upper()
        if not args['same']:
            incident_copy['incident_id'] = incident_copy['plus']['master_id']
        # update modified datetime
        incident_copy['plus']['modified'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        # save the file
        try:
            out_filename = os.path.join(args['output'], incident_copy['plus']['master_id'] + '.json')
            logging.info("Writing copy {0}".format(out_filename))
            with open(out_filename,'w') as outfile:
                simplejson.dump(incident_copy, outfile, sort_keys=True, indent=2, separators=(',', ': '))
        except UnicodeDecodeError:
            logging.critical("Some kind of unicode error.")
            logging.critical(incident_copy)
            raise
    logging.info('Ending main loop.')

if __name__ == "__main__":
    main(args)