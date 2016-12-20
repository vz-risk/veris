import json as sj
import argparse
import logging
from glob import glob
import os
from fnmatch import fnmatch
import ConfigParser
from tqdm import tqdm
import imp
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise

cfg = {
    'log_level': 'warning',
    'log_file': None,
    'countryfile':'./all.json'
}


def main(cfg):
    veris_logger.updateLogger(cfg)

    logging.warning("Converting files from {0} to {1}.".format(cfg["input"], cfg["output"]))
    for root, dirnames, filenames in tqdm(os.walk(cfg['input'])):
      logging.warning("starting parsing of directory {0}.".format(root))
      filenames = filter(lambda fname: fnmatch(fname, "*.json"), filenames)
      if filenames:
        dir_ = os.path.join(cfg['output'], root[len(cfg['input']):]) # if we don't strip the input, we get duplicate directories 
        logging.warning("Output directory is {0}.".format(dir_))
        if not os.path.isdir(dir_):
            os.makedirs(dir_)
        for fname in filenames:
            in_fname = os.path.join(root,fname)
            out_fname = os.path.join(dir_, fname)

            logging.info("Now processing %s" % in_fname)
            try:
                incident = sj.loads(open(in_fname).read())
            except sj.scanner.JSONDecodeError:
                logging.warning(
                    "ERROR: %s did not parse properly. Skipping" % in_fname)
                continue

            # Update the schema version
            incident['schema_version'] = "1.4"

            # Add hierarchy to assets
            # Issue 111, Commit 9a3d1de
            asset_map = {   'S ': 'server',
                            'M ': 'media',
                            'P ': 'people',
                            'N ': 'network',
                            'U ': 'user device',
                            'T ': 'public terminal',
                            'E ': 'embedded' }
            old_assets = incident['asset'].pop("assets")
            new_assets = list()
            for old_asset in old_assets:
                variety = asset['variety']
                new_asset = {
                    "varity": variety[4:].capitalize(),
                }
                if "amount" in old_asset.keys():
                    new_asset['amount'] = old_asset['amount']
                if [asset_map[variety[:2]] not in new_asset.keys():
                    new_assets[[asset_map[variety[:2]]] = []
                new_assets[asset_map[variety[:2]]].append(new_asset)
            incident.['asset']['assets'] = new_assets

            # Add hierarchy to discovery_method
            # Issue 121, Commit 9a3d1de
            disc_map = { "Int": "internal",
                         "Ext": "external",
                         "Prt": "partner"}
            discovery_method = incident.pop('discovery_method')
            if discovery_method == "Unknown":
                incident['discovery_method'] = {'unknown': {}}
            elif discovery_method == 'Other':
                incident['discovery_method'] = {'other': {}}
            else:
                incident['discovery_method'] = {disc_map[discovery_method[:3]]: {"variety": discovery_method[6:].capitalize()}}

            # Now to save the incidenta
            logging.info("Writing new file to %s" % out_fname)
            with open(out_fname, 'w') as outfile:
                sj.dump(incident, outfile, indent=2, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    descriptionText = "Converts VERIS 1.3 incidents to v1.3.1"
    helpText = "output file to write new files. Default is to overwrite."
    parser = argparse.ArgumentParser(description=descriptionText)
    parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument("-i", "--input", required=True,
                        help="top level folder to search for incidents")
    parser.add_argument("-o", "--output", required=True,
                        help=helpText)
    parser.add_argument('--countryfile', help='The json file holdering the country mapping.')
    parser.add_argument('--conf', help='The location of the config file', default="../user/data_flow.cfg")
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}

    # logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG} # defined above. - gdb 080716

    # Parse the config file
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(args["conf"]))
        cfg_key = {
            'GENERAL': ['report', 'input', 'output', 'analysis', 'year', 'force_analyst', 'version', 'database', 'check'],
            'LOGGING': ['log_level', 'log_file'],
            'REPO': ['veris', 'dbir_private'],
            'VERIS': ['mergedfile', 'enumfile', 'schemafile', 'labelsfile', 'countryfile']
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
    # place any unique config file parsing here
    if "input" in cfg:
        cfg["input"] = [l.strip() for l in cfg["input"].split(" ,")]  # spit to list

    cfg.update(args)

    veris_logger.updateLogger(cfg)

    # assert args.path != args.output, "Source and destination must differ"

    main(cfg)

