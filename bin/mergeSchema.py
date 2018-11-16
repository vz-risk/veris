# Produces a schema file which is the combination of
# of a schema, an enumeration, and a plus section

import jsonschema
import json
import argparse
import logging
import copy
import os
#import importlib
import imp
from collections import OrderedDict
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    #spec = importlib.util.spec_from_file_location("veris_logger", script_dir + "/veris_logger.py")
    #veris_logger = importlib.util.module_from_spec(spec)
    #spec.loader.exec_module(veris_logger)
    veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise

#DEFAULTSCHEMA = "../verisc.json"
#DEFAULTLABELS = "../verisc-labels.json"
#MERGED = '../verisc-merged.json'
#KEYNAMES = '../keynames-real.txt'
#ENUM = "../verisc-enum.json"
DEFAULTSCHEMA = None
DEFAULTLABELS = None
MERGED = None
KEYNAMES = None
ENUM = None

def deepGetAttr(od, name):
    if len(name) > 1:
        return deepGetAttr(od[name[0]], name[1:])
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
#         except:
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

def keynames(d, lbl, name, keys=set()):
    if d['type'] == "object":
        lbl = lbl + "properties."
        for k, v in d['properties'].items():
            keys = keys.union(keynames(v, lbl, name + "." + k))
    elif d['type'] == "array":
        lbl = lbl + "items."
        keys = keys.union(keynames(d['items'], lbl, name))
    else:
        keys.add(name[1:])
    return keys


def recurse_keys(d, lbl, keys=set()):
    for k, v in d.items():
        if type(v) in [OrderedDict, dict]:
            keys = keys.union(recurse_keys(v, (lbl + (k,)), keys))
        else:
            keys.add(lbl)
    return keys


def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring


def merge(schema, labels):
    # get the keys to join
    veris_logger.updateLogger()
    logging.debug(labels.keys())
    keys = recurse_keys(labels, ())
    logging.debug(keys)

    # convert to objects to help with parsing
    # schema = objdict(schema)
    # labels = objdict(labels)

    # Add the enumerations to the schema file
    for key in keys:
        name = "properties."
        for i in range(len(key)):
            # tacking 'properties.' on to the end of 'items.' rather than having separate logic for arrays and objects
            #   is kind of a hack, but I think it'll work for all intended uses for the script. - gdb 06/03/16
            name = name + key[i] + "." + {"array": "items.properties.", "object": "properties."}.get(deepGetAttr(schema, "{0}{1}.type".format(name, key[i]).split(".")), "") # append properties or nothing
        logging.info("Updating key " + name)
        try:
            logging.debug("Adding keys {0}".format(deepGetAttr(labels, key).keys()))
        except:
            logging.debug(key)
            raise
        try:
            schema = deepSetAttr(schema, "{0}{1}".format(rchop(name, "properties."), "enum").split("."), deepGetAttr(labels, key).keys())
        except:
            logging.debug("{0}{1}".format(rchop(name, "properties."), "enum"))
            raise

    return schema

def enums(schema, labels):
    # convert to objects to help with parsing
    veris_logger.updateLogger()
    # schema = objdict(schema)
    # labels = objdict(labels)
    keys = recurse_keys(labels, ())
    logging.debug(keys)
    if args.enum is not None:
        veris_enum = copy.deepcopy(labels)
        for key in keys:
            veris_enum = deepSetAttr(veris_enum, key, deepGetAttr(labels, key).keys())
    return veris_enum



if __name__ == '__main__':
    descriptionText = """This script merges the schema file and labels file.
    Optionally, it can also generate the 
enums file and the keynames file.  
Keys will be ordered by the schema file, but
enums will be ordered by the labels file."""
    parser = argparse.ArgumentParser(description=descriptionText)
    parser.add_argument("-s", "--schema",
                        help="schema file. (Normally '../verisc.json'.)", default=DEFAULTSCHEMA)
    parser.add_argument("--labels",
                        help="the labels file. (Normally '../verisc-labels.json'.", default=DEFAULTLABELS)
    parser.add_argument("-o", "--output",
                        help="the location of the merged output file. (Normally '../verisc-merged.json'.)", default=MERGED)
    parser.add_argument("-e", "--enum", help="The name of the enums file if desired. (Normally '../verisc-enum.json'.)", default=None)
    parser.add_argument("-k", "--keynames", help="The name of the keynames file if desired. (normally '../keynames-real.txt'.)", default=None)
    parser.add_argument("-l", "--logging", choices=["critical", "warning", "info", "debug"],
                        help="Minimum logging level to display",
                        default="warning")
    args = parser.parse_args()
    level = args.logging
    cfg = {
    'log_level': level
    }
    veris_logger.updateLogger(cfg)
 
    with open(args.schema, 'r') as filehandle:
        schema = json.load(filehandle, object_pairs_hook=OrderedDict)
    with open(args.labels, 'r') as filehandle:
        labels = json.load(filehandle, object_pairs_hook=OrderedDict)
    #schema = json.loads(open(args.schema).read())
    #labels = json.loads(open(args.labels).read())

     # write the merged schema
    merged = merge(schema, labels)
    with open(args.output, 'w') as outfile_handle:
        json.dump(merged, outfile_handle, sort_keys=False, indent=2)

    # write the keys out
    if args.keynames is not None:
        keynames = keynames(schema, "", "")
        keynames = list(keynames)
        keynames.sort()
        with open(args.keynames, 'w') as keynames_handle:
            for keyname in keynames:
                keynames_handle.write(keyname + "\n")

    # write the enums out
    if args.enum is not None:
        veris_enum = enums(schema, labels)
        with open(args.enum, 'w') as enum_handle:
            json.dump(veris_enum, enum_handle, sort_keys=False, indent=2)
