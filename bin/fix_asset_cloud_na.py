import json as sj
import argparse
import logging
from glob import glob
import os
from fnmatch import fnmatch
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

            if incident['schema_version'] == "2":
                if 'sequence' in incident:
                    for i in range(len(incident['sequence'])):
                        if 'asset' in incident['sequence'][i]:
                            if 'cloud' in incident['sequence'][i]['asset']:
                                if incident['sequence'][i]['asset']['cloud'].lower() == u'na':
                                    _ = incident['sequence'][i]['asset'].pop('cloud')
                            if len(incident['sequence'][i]['asset']) == 0:
                                _ = incident['sequence'][i].pop('asset')

            else:
                if 'asset' in incident:
                    if 'cloud' in incident['asset']:
                        if incident['asset']['cloud'].lower() == u'na':
                            _ = incident['asset'].pop('cloud')
                    if len(incident['asset']) == 0:
                        _ = incident.pop('asset')


            if 'plus' in incident:
                if 'timeline' in incident['plus']:
                    if 'notification' in incident['plus']['timeline']:
                        if len(incident['plus']['timeline']['notification']) == 0:
                            _ = incident['plus']['timeline'].pop('notification')
                    if len(incident['plus']['timeline']) == 0:
                        _ = incident['plus'].pop('timeline')
                if len(incident['plus']) == 0:
                    _ = incident.pop('plus')

            with open(out_fname, 'w') as outfile:
                sj.dump(incident, outfile, indent=2, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    descriptionText = "removes empty 'timeline.notification' features from VERIS json"
    helpText = "output file to write new files. Default is to overwrite."
    parser = argparse.ArgumentParser(description=descriptionText)
    parser.add_argument("-i", "--input", required=True,
                        help="top level folder to search for incidents")
    parser.add_argument("-o", "--output", required=True,
                        help=helpText)
    parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')

    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}
    cfg.update(args)

    main(cfg)