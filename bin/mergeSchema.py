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

def recurse_keys(d, lbl):
    keys = set()
    for k,v in d.iteritems():
        if type(v) == dict:
            keys = keys.union(recurse_keys(v, (lbl + (k,))))
        else:
            keys.add(lbl)
        return keys


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
    parser.add_argument("--logging", choices=["critical",
                                                    "warning", "info"],
                        help="Minimum logging level to display",
                        default="warning")
    args = parser.parse_args()
    logging_remap = {'warning': logging.WARNING, 'critical': logging.CRITICAL,
                     'info': logging.INFO}
    logging.basicConfig(level=logging_remap[args.logging])
    schema = objdict(json.loads(open(args.schema).read()))
    labels = objdict(json.loads(open(args.labels).read()))
    # get the keys to join
    keys = recurse_keys(labels, ())
    # write the keys out
    if args.keynames is not None:
        with open(args.keynames, 'w') as keynames_handle:
            for key in keys:
                keynames_handle.write(".".join(key) + "\n")
    # write the enums out
    if args.enum is not None:
        veris_enum = copy.deepcopy(labels)
        for key in keys:
            setattr(veris_enum, ".".join(key), getattr(labels, ".".join(key)).keys())
        with open(args.enum, 'w') as enum_handle:
            json.dump(veris_enum, enum_handle)
    # Add the enumerations to the schema file
    for key in keys:
        setattr(schema, "properties." + ".properties.".join(key) + ".enum", getattr(labels, ".".join(key)).keys())
    # write the merged schema
    with open(args.output, 'w') as outfile_handle:
        json.dump(schema, outfile_handle, sort_keys=True, indent=2)
