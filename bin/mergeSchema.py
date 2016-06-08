# Produces a schema file which is the combination of
# of a schema, an enumeration, and a plus section

import json
import jsonschema
import argparse
import logging
import copy

DEFAULTSCHEMA = "../verisc.json"
DEFAULTLABELS = "../verisc-labels.json"
MERGED = '../verisc-merged.json'
KEYNAMES = '../keynames-real.txt'
ENUM = "../verisc-enum.json"


class objdict(dict):
    def __getattr__(self, name):
        try:
            return self.recursive_getattr(self, name)
        except:
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

def recurse_schema(d, lbl, name, keys=set()):
    if d['type'] == "object":
        lbl = lbl + "properties."
        for k, v in d['properties'].iteritems():
            keys = keys.union(recurse_schema(v, lbl, name + "." + k))
    elif d['type'] == "array":
        lbl = lbl + "items."
        keys = keys.union(recurse_schema(d['items'], lbl, name))
    else:
        keys.add(name[1:])
    return keys


def recurse_keys(d, lbl, keys=set()):
    for k, v in d.iteritems():
        if type(v) == dict:
            keys = keys.union(recurse_keys(v, (lbl + (k,)), keys))
        else:
            keys.add(lbl)
    return keys

def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring


if __name__ == '__main__':
    descriptionText = """This script merges the schema file and labels file.
    Optionally, it can also generate the enums file and the keynames file."""
    parser = argparse.ArgumentParser(description=descriptionText)
    parser.add_argument("-s", "--schema",
                        help="schema file.", default=DEFAULTSCHEMA)
    parser.add_argument("-l", "--labels",
                        help="the labels file.", default=DEFAULTLABELS)
    parser.add_argument("-o", "--output",
                        help="the location of the merged output file.", default=MERGED)
    parser.add_argument("-e", "--enum", help="The name of the enums file if desired. (Normally '../<schame name>-enum.json'.)", default=None)
    parser.add_argument("-k", "--keynames", help="The name of the keynames file if desired. (normally '../keynames-real.txt'.)", default=None)
    parser.add_argument("--logging", choices=["critical", "warning", "info", "debug"],
                        help="Minimum logging level to display",
                        default="warning")
    args = parser.parse_args()
    logging_remap = {'warning': logging.WARNING, 'critical': logging.CRITICAL,
                     'info': logging.INFO, 'debug': logging.DEBUG}
    logging.basicConfig(level=logging_remap[args.logging])
    with open(args.schema, 'r') as filehandle:
        schema = json.load(filehandle)
    with open(args.labels, 'r') as filehandle:
        labels = json.load(filehandle)
    #schema = json.loads(open(args.schema).read())
    #labels = json.loads(open(args.labels).read())
    # get the keys to join
    logging.debug(labels.keys())
    keys = recurse_keys(labels, ())
    logging.debug(keys)
    # write the keys out
    if args.keynames is not None:
        keynames = recurse_schema(schema, "", "")
        keynames = list(keynames)
        keynames.sort()
        with open(args.keynames, 'w') as keynames_handle:
            for keyname in keynames:
                keynames_handle.write(keyname + "\n")
    # convert to objects to help with parsing
    schema = objdict(schema)
    labels = objdict(labels)
    # write the enums out
    if args.enum is not None:
        veris_enum = copy.deepcopy(labels)
        for key in keys:
            setattr(veris_enum, ".".join(key), getattr(labels, ".".join(key)).keys())
        with open(args.enum, 'w') as enum_handle:
            json.dump(veris_enum, enum_handle, sort_keys=True, indent=2)
    # Add the enumerations to the schema file
    for key in keys:
        name = "properties."
        for i in range(len(key)):
            # tacking 'properties.' on to the end of 'items.' rather than having separate logic for arrays and objects
            #   is kind of a hack, but I think it'll work for all intended uses for the script. - gdb 06/03/16
            name = name + key[i] + "." + {"array": "items.properties.", "object": "properties."}.get(getattr(schema, name + key[i] + ".type"), "") # append properties or nothing
        logging.info("Updating key " + name)
        logging.debug("Adding keys {0}".format(getattr(labels, ".".join(key)).keys()))
        setattr(schema, rchop(name, "properties.") + "enum", getattr(labels, ".".join(key)).keys())
    # write the merged schema
    with open(args.output, 'w') as outfile_handle:
        json.dump(schema, outfile_handle, sort_keys=True, indent=2)
