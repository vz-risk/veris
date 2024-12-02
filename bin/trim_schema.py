#!/usr/bin/env python
"""
 AUTHOR: Phil Langlois
 DATE: <10-09-2024>
 DEPENDENCIES: <a list of modules requiring installation>


 DESCRIPTION:
 Takes the parent schema and makes children schemas by using a diff-schema which defines which fields + enums should be dropped

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
import configparser
import json
import pprint
# import ipdb
import os
from importlib import util
from collections import OrderedDict

script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    spec = util.spec_from_file_location("veris_logger", script_dir + "/veris_logger.py")
    veris_logger = util.module_from_spec(spec)
    spec.loader.exec_module(veris_logger)
    # veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise

## SETUP
__author__ = "Phil Langlois"

## GLOBAL EXECUTION
pass


## CLASS AND FUNCTION DEFINITION
def deepGetAttr(od, name):
    if len(name) > 1:
        try:
            return deepGetAttr(od[name[0]], name[1:])
        except:
            logging.error(f"failed getting attribute {name}")
            raise
    else:
        return od[name[0]]


def deepSetAttr(od, name, value):
    try:
        if len(name) > 1:
            od[name[0]] = deepSetAttr(od.get(name[0], {}), name[1:], value)
        else:
            od[name[0]] = value
        return od
    except Exception as e:
        logging.error(f"failed to do thing {e}")

## Update process should probably be as follows
## descend the tree of the Update file and get the furtherest branch
## remove the branches in reverse order (from further out to in)
## build FULL queue from update file (what are all the branches)
## then go through the pruning process starting from furthest branch
## if the branch has no properties, it should be dropped (meaning all of it's branches were removed)

def update_instance(inInstance, updateInstance):
    # update each of the items in the Instance (other than 'properties' or 'items')
    for item in updateInstance.keys():
        if item == "":
            pass  # otherwise we get a recursive call
        if item == "properties":
            if not inInstance[item]:
                inInstance.pop(item)
        elif item == "items":
            inInstance.pop(item)
        elif item == "type":
            pass
        elif type(inInstance[item]) == list:
            try:
                for x in updateInstance[item]:
                    # remove the value from updateInstance
                    if x in inInstance[item]:
                        inInstance[item].pop(inInstance.index(x))
                    else:
                        pass
            except Exception as e:
                logging.error(f"failed parsing list {item} : {e}")
        elif type(inInstance[item]) == dict:
            inInstance[item].pop(updateInstance[item])
        elif not inInstance[item]:
            inInstance.pop(item)
        else:
            inInstance.pop(item, None)
    return inInstance

def remove_empty_branches(inInstance):
    fields_to_keep = ['type', 'schema_name']

    trimmed_inInstance = inInstance.copy()
    for element in trimmed_inInstance.keys():
        if len(inInstance[element]) < 3 and element not in fields_to_keep:
            inInstance.pop(element)
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
    if 'description' in updateFile.keys():
        inFile['description'] = updateFile['description']

    queue = []
    for instance in updateFile.get('properties', {}):
        queue.append(["properties", instance])
    for instance in updateFile.get('items', {}):
        queue.append(["items", instance])
    for instance in queue:
        try:
            for inst in deepGetAttr(updateFile, instance)['properties'].keys():
                queue.append(instance + ["properties", inst])
        except KeyError:
            print("{0} failed to find property".format(instance))
            # pass  # clearly not an object with attributes to add
        except Exception as e:
            print(f"i goofed {e}")
    # we now have a list of possible enuemrations we could remove


    for instance in reversed(queue):
        # trim the leaves of the branches
        fields_to_avoid = ['schema_name', 'type']
        # assure we're not removing key fields from our schema
        if not any(check in fields_to_avoid for check in instance):
        # pull what we'll be updating
            inInstance = deepGetAttr(inFile, instance)

            updateInstance = deepGetAttr(updateFile, instance)

            inInstance = update_instance(inInstance, updateInstance)

            inFile = deepSetAttr(inFile, instance, inInstance)

    # trim the empty branches:
    for instance in reversed(queue):
        # this loop goes up the full tree as defined in queue and removes branches that have no leaves
        # it leaves the top level of the schema alone by assuring that the depth is more than 2 elements
        # it can also be used to ignore certain values

        fields_to_avoid = ['schema_name']
        if not any(check in fields_to_avoid for check in instance) and len(instance)>2:
            inInstance = deepGetAttr(inFile, instance[:-1]) #go up one in the property tree
            inInstance = remove_empty_branches(inInstance)
            inFile = deepSetAttr(inFile, instance[:-1], inInstance)
    return inFile


if __name__ == "__main__":

    ## The general Approach to config parsing (Probably not the best way)
    ## 1. create a dictionary called 'cfg' of fallback values (up at the top of the file)
    ## 2. parse the arguments (args) and turn into a dictionary if the value is not None
    ## 3. Use the config from the command line parser to read the config file and update the 'cfg' dictionary
    ## 4. Update the cfg dictionary with the arguements (args) from the command line

    # Parse Arguments (should correspond to user variables)
    parser = argparse.ArgumentParser(
        description='Takes a json schema file and an update file (also a schema file) and updates the original with the updates.')
    parser.add_argument("-l", "--log_level", choices=["critical", "warning", "info", "debug"],
                        help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument('--conf', help='The location of the config file')
    parser.add_argument('-i', '--input', required=True, help='The schema file to be updated.')
    parser.add_argument('-u', '--update', required=True,
                        help='The schema files to update the input file with (only additions/modifications to labels.)')
    parser.add_argument('-o', '--output', required=True, help='The labels file to be outputted.')
    args = parser.parse_args()
    args = {k: v for k, v in vars(args).items() if v is not None}

    # Parse the config file
    try:
        config = configparser.ConfigParser()
        config.read_file(open(args["conf"]))
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
        # raise e
        pass

    cfg.update(args)
    veris_logger.updateLogger(cfg)

    logging.debug(args)
    logging.debug(cfg)

    outFile = main(cfg)

    with open(cfg["output"], 'w') as filehandle:
        json.dump(outFile, filehandle, indent=2, sort_keys=False)
