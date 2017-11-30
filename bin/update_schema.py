#!/usr/bin/env python
"""
 AUTHOR: Gabriel Bassett
 DATE: <06-20-2016>
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

########### NOT USER EDITABLE ABOVE THIS POINT #################


# USER VARIABLES
cfg = {
    "input": None,
    "update": None,
    "output": None,
    "log_level": "warning",
    "log_file": None
}

########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import ConfigParser
import json
import pprint
import ipdb
import os
import imp
from collections import OrderedDict
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise

## SETUP
__author__ = "Gabriel Bassett"

## GLOBAL EXECUTION
pass



## CLASS AND FUNCTION DEFINITION
def deepGetAttr(od, name):
    if len(name) > 1:
        try:
            return deepGetAttr(od[name[0]], name[1:])
        except:
            logging.error(name)
            raise
    else:
        return od[name[0]]
    
def deepSetAttr(od, name, value):
    if len(name) > 1:
        od[name[0]] = deepSetAttr(od.get(name[0], {}), name[1:], value)
    else:
        od[name[0]] = value
    return od

# class objdict(dict):
#     def __getattr__(self, name):
#         try:
#             return self.recursive_getattr(self, name)
#         except Exception as e:
#             raise AttributeError("No such attribute: " + name)

#     def __setattr__(self, name, value):
#         try:
#             self.recursive_setattr(self, name, value)
#         except:
#             raise AttributeError("No such attribute: " + name)
    
#     def __delattr__(self, name):
#         try:
#             self.recursive_delattr(self, name)
#         except:
#             raise AttributeError("No such attribute: " + name)

#     def recursive_setattr(self, o, name, value):
#         name = name.split(".", 1)
#         if len(name) > 1:
#             self.recursive_setattr(o[name[0]], name[1], value)
#         else:
#             o[name[0]] = value

#     def recursive_getattr(self, o, name):
#         name = name.split(".", 1)
#         if len(name) > 1:
#             return self.recursive_getattr(o[name[0]], name[1])
#         else:
#             return o[name[0]]

#     def recursive_delattr(self, o, name):
#         name = name.split(".", 1)
#         if len(name) > 1:
#             self.recursive_delattr(o[name[0]], name[1])
#         else:
#             del o[name[0]]



def update_instance(inInstance, updateInstance):
    # update each of the items in the Instance (other than 'properties' or 'items')
    for item in updateInstance.keys():
        if item == "":
            pass # otherwise we get a recursive call
        if item == "properties":
            if "properties" not in inInstance:
                inInstance['properties'] = {}
        elif item == "items":
            if "items" not in inInstance:
                inInstance["items"] == {}
        elif item not in inInstance:
            inInstance[item] = updateInstance[item]
        elif type(inInstance[item]) == list:
            inInstance[item] = inInstance['item'] + [i for i in updateInstance[item] if i not in inInnstance['item']] # replace set-based join to maintain order
        elif type(inInstance[item]) == dict :
            inInstance[item].update(updateInstance[item])
        else:
            inInstance[item] == updateInstance[item]
    return inInstance


## MAIN LOOP EXECUTION
def main(cfg):
    veris_logger.updateLogger(cfg)
    logging.info('Beginning main loop.')

    # Open the files
    with open(cfg["input"], 'r') as filehandle:
        inFile = json.load(filehandle, object_pairs_hook=OrderedDict)
    with open(cfg["update"], 'r') as filehandle:
        updateFile = json.load(filehandle, object_pairs_hook=OrderedDict)

    logging.debug("Updating root of schema.")
    inFile = update_instance(inFile, updateFile)
    if 'description' in updateFile.keys():
        inFile['description'] = updateFile['description']

    queue = []
    for instance in updateFile.get('properties', {}):
        queue.append(["properties", instance])
    for instance in updateFile.get('items', {}):
        queue.append(["items" , instance])

    # create object representations of dicts
    # oInFile = objdict(inFile)
    # oUpdateFile = objdict(updateFile)

    # for each property in the update
#    ipdb.set_trace()  # debugging hook
    for instance in queue:
        logging.debug("Updating {0} in schema.".format(instance))
        updateInstance = deepGetAttr(updateFile, instance)

        # if the object exists in the schema, update it with the properties in the update.
        try:
            inInstance = deepGetAttr(inFile, instance)
            inInstance = update_instance(inInstance, updateInstance)
            # save the instance back to the schema
            inFile = deepSetAttr(inFile, instance, inInstance)

            # queue properties
            try:
                for inst in deepGetAttr(updateFile, instance)['properties'].keys():
                    queue.append(instance + ["properties", inst])
            except KeyError:
                pass # clearly not an object with attributes to add

            # queue items
            try:
                for inst in deepGetAttr(updateFile, instance)['items'].keys():
                    queue.append(instance + ["items", inst])
            except KeyError:
                pass # clearly not an object with attributes to add


        # if it is not, add it to the schema as a property to the correct object
        except (AttributeError, KeyError):
            inFile = deepSetAttr(inFile, instance, updateInstance)


    logging.info('Ending main loop.')
    return inFile

if __name__ == "__main__":

    ## The general Approach to config parsing (Probably not the best way)
    ## 1. create a dictionary called 'cfg' of fallback values (up at the top of the file)
    ## 2. parse the arguments (args) and turn into a dictionary if the value is not None
    ## 3. Use the config from the command line parser to read the config file and update the 'cfg' dictionary
    ## 4. Update the cfg dictionary with the arguements (args) from the command line

    # Parse Arguments (should correspond to user variables)
    parser = argparse.ArgumentParser(description='Takes a json schema file and an update file (also a schema file) and updates the original with the updates.')
    parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument('--conf', help='The location of the config file')
    parser.add_argument('-i', '--input', required=True, help='The schema file to be updated.')
    parser.add_argument('-u', '--update', required=True, help='The schema files to update the input file with (only additions/modifications to labels.)')
    parser.add_argument('-o', '--output', required=True, help='The labels file to be outputted.')
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
        veris_logger.updateLogger(cfg)
        logging.debug("config import succeeded.")
    except Exception as e:
        logging.warning("config import failed with error {0}.".format(e))
        #raise e
        pass

    cfg.update(args)
    veris_logger.updateLogger(cfg)

    logging.debug(args)
    logging.debug(cfg)

    outFile = main(cfg)

    with open(cfg["output"], 'w') as filehandle:
        json.dump(outFile, filehandle, indent=2, sort_keys=False)
