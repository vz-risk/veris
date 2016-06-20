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
    "log_level": "debug",
    "log_file": None
}

########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import ConfigParser
import json
import pprint

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
        if not name:
            return dict(self)
        else:
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



## MAIN LOOP EXECUTION
def main(cfg):
    logger.info('Beginning main loop.')

    # Open the files
    with open(cfg["input"], 'r') as filehandle:
        inFile = json.load(filehandle)
    with open(cfg["update"], 'r') as filehandle:
        updateFile = json.load(filehandle)

#    inKeys = recurse_keys(inFile, "")
#    updateKeys = recurse_keys(updateFile, "")

    oInFile = objdict(inFile)
    oUpdateFile = objdict(updateFile)

    queue = [""]
## Not sure this is needed as the original "" parse should add properties and items - gdb 061916
#    for instance in updateFile.get('properties', {}):
#        queue.append("properties." + instance)
#    for instance in updateFile.get('items', {}):
#        queue.append("items." + instance)
    # for each property in the update
    for instance in queue:
        updateInstance = getattr(oUpdateFile, instance)

        # if the object exists in the schema, update it with the properties in the update.
        try:
            inInstance = getattr(oInFile, instance)

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
                    inInstance[item] = list(set(inInstance[item]).union(updateInstance[item]))
                elif type(inInstance[item]) == dict :
                    inInstance[item].update(updateInstance[item])
                else:
                    inInstance[item] == updateInstance[item]

            # save the instance back to the schema
            setattr(oInFile, instance, inInstance)

            # queue properties
            try:
                for inst in getattr(oUpdateFile, instance)['properties'].keys():
                    queue.append(str(instance + ".properties." + inst).lstrip("."))
            except KeyError:
                pass # clearly not an object with attributes to add

            # queue items
            try:
                for inst in getattr(oUpdateFile, instance)['items'].keys():
                    queue.append(str(instance + ".items." + inst).lstrip("."))
            except KeyError:
                pass # clearly not an object with attributes to add


        # if it is not, add it to the schema as a property to the correct object
        except AttributeError:
            #split = instance.rfind(".")
            #getattr(oInFile, instance[:split])[split+1:] = updateInstance
            setattr(oInFile, instance, updateInstance)


    logger.info('Ending main loop.')
    return dict(oInFile)

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
    parser.add_argument('--input', required=True, help='The schema file to be updated.')
    parser.add_argument('--update', required=True, help='The schema files to update the input file with (only additions/modifications to labels.)')
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

    with open("/Users/v685573/tmp/test.txt", 'w') as filehandle:
        pprint.pprint(outFile, filehandle)

    with open(cfg["output"], 'w') as filehandle:
        json.dump(outFile, filehandle, indent=2, sort_keys=True)