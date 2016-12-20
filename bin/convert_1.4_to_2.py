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
            incident['schema_version'] = "2"

            # Add sequencing
            # Issue 127, Commit 3db2960
            incident['stage'] = [{'timeline':{}}]
            incident['stage'][0]['action'] = incident.pop('action')
            incident['stage'][0]['actor'] = incident.pop('actor')
            incident['stage'][0]['asset'] = incident.pop('asset')
            incident['stage'][0]['attribute'] = incident.pop('attribute')
            incident['stage'][0]['victim'] = incident.pop('victim')
            incident['stage'][0]['discovery_method'] = incident.pop('discovery_method')
            if 'confidence' in incident:
                incident['stage'][0]['confidence'] = incident.pop('confidence')
            if 'control_failure' in incident.keys(control_failure)
                incident['stage'][0]['control_failure'] = incident.pop('control_failure')
            if 'discovery_notes' in incident.keys():
                incident['stage'][0]['discovery_notes'] = incident.pop('discovery_notes')
            if 'compromise' in incident['timeline']:
                incident['stage'][0]['timeline']['compromise'] = incident['timeline'].pop('compromise')
            if 'exfiltration' in incident['timeline']:
                incident['stage'][0]['timeline']['exfiltration'] = incident['timeline'].pop('exfiltration')
            if 'discovery' in incident['timeline']:
                incident['stage'][0]['timeline']['discovery'] = incident['timeline'].pop('discovery')
            if 'containment' in incident['timeline']:
                incident['stage'][0]['timeline']['containment'] = incident['timeline'].pop('containment')


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

