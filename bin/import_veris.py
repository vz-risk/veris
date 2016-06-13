#!/usr/bin/env python
"""
 AUTHOR: Gabriel Bassett
 DATE: 06-09-16
 DEPENDENCIES: <a list of modules requiring installation>

 DESCRIPTION:
 Given a reviewed veris csv, generate veris json.

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

########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import ConfigParser
import imp
import os
import json

## SETUP
__author__ = "Gabriel Bassett"

# Default Configuration Settings
cfg = {
    'log_level': 'warning',
    'log_file': None,
    'schemafile': "../vcdb/veris.json",
    'enumfile': "../vcdb/veris-enum.json",
    'vcdb':False,
    'version':"1.3",
    'countryfile':'all.json',
    'output': os.getcwd(),
    'quiet': False,
    'repositories': ""
}

#logger = multiprocessing.get_logger()
logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG,
                 50: logging.CRITICAL, 40: logging.ERROR, 30: logging.WARNING, 20: logging.INFO, 10: logging.DEBUG, 0: logging.CRITICAL}
FORMAT = '%(asctime)19s - %(processName)s {0} - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT.format(""), datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger()



## FUNCTION DEFINITION
pass



## MAIN LOOP EXECUTION
def main(cfg):
    logger.info('Beginning main loop.')

    # import the 4 different veris conversion scripts
    scripts = {"vzir": cfg.get("dbir-private", "").rstrip("/") + "/bin/sg-to-dbir1_3.py",
               "vcdb": cfg.get("dbir-private", "").rstrip("/") + "/bin/sg-to-vcdb1_3.py",
               "sg": cfg.get("dbir-private", "").rstrip("/") + "/bin/sgpartner_to_dbir.py",
               "stdexcel": cfg.get("veris", "").rstrip("/") + "/bin/import_stdexcel.py"
               }
    for name, script in scripts.iteritems():
        try:
            logger.debug("Importing {0} from {1}.".format(name, scripts[name]))
            scripts[name] = imp.load_source(name, script)
        except Exception as e:
            logger.warning("{0} with file {1} didn't import due to {2}".format(name, scripts[name], e))
            scripts[name] = None


    # get the partner name
    source = cfg['input'].split("/")[-2].lower()
    source = ''.join([e for e in source if e.isalnum()])

    if source not in cfg:
        cfg['source'] = source

    logger.info("Starting import of {0}.".format(source))
    #print("Starting import of {0}.".format(source))

## This functionality will remain in import_all_data.py - GDB 6/9/16
#    # set the output Directory
#    outDir = cfg['output'].rstrip("/") + "/" + source
#    if not os.path.exists(outDir):
#        os.makedirs(outDir)
#
#    existing_files = glob.glob(outDir + "/*.json")
#
#    # If there are files in the output directory and "clear_output" is set, delete files in target directory
#    if not cfg['clear'] and existing_files:
#        logging.warning("Existing files in {0} directory and clear is False.  Skipping import.".format(source))
#        return None
#    else:
#        for json_file in existing_files:
#            if os.path.isfile(json_file):
#                os.remove(json_file)
    

    # Figure out the file type
    ## If partner is 'vzir', use vzir.
    if source == "vzir":
        script = "vzir"
    ## If partner is 'vcdb', use vcdb
    elif source == "vcdb":
        script = "vcdb"
    ## Look at column names
    with open(cfg['input'], 'rU') as filehandle:
        line = filehandle.readline()  # read the column headers. SurveyGizmo has lots of ":" while stdexcel has "."
    c_count = line.count(":")
    p_count = line.count(".")
    ### choose based on column names
    if c_count > p_count:
        script = "sg"
    else:
        script = "stdexcel"

    # run the import script  
    # TODO: Replace below block with call in scripts[script].main()
#    subprocess.call([
#        "python",
#        scripts[script],
#        "-i",
#        cfg['inFile'],
#        "-o",
#        outDir,
#        "--conf",
#        cfg['conf'],
#        "--source",
#        source
#    ])
    for iid, incident_json in scripts[script].main(cfg):
        yield iid, incident_json


    logger.info('Ending main loop.')



# do the whole config thing thing
if __name__ == '__main__':

    ## Gabe
    ## The general Apprach to config parsing (Probably not the best way)
    ## 1. create a dictionary called 'cfg' of fallback values (up at the top of the file)
    ## 2. parse the arguments (args) and turn into a dictionary if the value is not None
    ## 3. Use the config from the command line parser to read the config file and update the 'cfg' dictionary
    ## 4. Update the cfg dictionary with the arguements (args) from the command line

    parser = argparse.ArgumentParser(description="This script takes a csv file, chooses a parser, and outputs veris JSON. It does not apply " + 
                                                 "additional rules or validate against the schema.")
    parser.add_argument("-i", "--input", required=True, help="The csv file containing the veris data")
    parser.add_argument("-o", "--output", required=True, help="directory where json files will be written")
    parser.add_argument("--veris", required=False, help="The location of the veris_scripts repository.")
    parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument("--dbir-private", required=False, help="The location of the dbirR repository.")
    parser.add_argument("-s","--schemafile", help="The JSON schema file")
    parser.add_argument("-e","--enumfile", help="The JSON file with VERIS enumerations")
    parser.add_argument("--vcdb",help="Convert the data for use in VCDB",action="store_true")
    parser.add_argument("--version", help="The version of veris in use")
    parser.add_argument('--conf', help='The location of the config file', default="./_checkValidity.cfg")
    parser.add_argument('--year', help='The DBIR year to assign tot he records.')
    parser.add_argument('--countryfile', help='The json file holdering the country mapping.')
    parser.add_argument('--source', help="Source_id to use for the incidents. Partner pseudonym.")
    parser.add_argument("-f", "--force_analyst", help="Override default analyst with --analyst.", action='store_true')
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}

    # Parse the config file
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(args["conf"]))
        cfg_key = {
            'GENERAL': ['input', 'output', 'dbirR', 'veris_scripts'],
            'LOGGING': ['level', 'log_file'],
            'VERIS': ['version', 'schemafile', 'enumfile', 'vcdb', 'year', 'countryfile']
        }
        for section in cfg_key.keys():
            if config.has_section(section):
                for value in cfg_key[section]:
                    if value.lower() in config.options(section):
                        cfg[value] = config.get(section, value)
        if "year" in cfg:
            cfg["year"] = int(cfg["year"])
        else:
            cfg["year"] = int(datetime.now().year)
        cfg["vcdb"] = {True:True, False:False, "false":False, "true":True}[cfg["vcdb"].lower()]
        logger.debug("config import succeeded.")
    except Exception as e:
        logger.warning("config import failed with error {0}.".format(e))
        #raise e
        pass

    cfg.update(args)


    logger.setLevel(logging_remap[cfg["log_level"]])
    #logger.basicConfig(level=logging_remap[cfg["log_level"]],
    #      format='%(asctime)19s %(levelname)8s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    if cfg["log_file"] is not None:
        logger.filename = cfg["log_file"]

    logger.debug(args)
    logger.debug(cfg)

    # TODO - Paralellize these steps per record. (Code is in main because when run as module, code is run in import_all_partners)
    for iid, incident_json in main(cfg):

        # TODO: run correlated fields using script


        # TODO: verify records


        # write the json to a file
        if cfg["output"].endswith("/"):
            dest = cfg["output"] + incident_json['plus']['master_id'] + '.json'
            # dest = args.output + outjson['incident_id'] + '.json'
        else:
            dest = cfg["output"] + '/' + incident_json['plus']['master_id'] + '.json'
            # dest = args.output + '/' + outjson['incident_id'] + '.json'
        logger.info("%s: writing file to %s", iid, dest)
        try:
            fwrite = open(dest, 'w')
            fwrite.write(json.dumps(incident_json, indent=2, sort_keys=True))
            fwrite.close()
        except UnicodeDecodeError:
            print incident_json
