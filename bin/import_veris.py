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
import imp
import os
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise

########### NOT USER EDITABLE ABOVE THIS POINT #################


# USER VARIABLES
dateFmt = '%m/%d/%Y %H:%M:%S'
########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import ConfigParser
import json
from datetime import datetime
from jsonschema import ValidationError, Draft4Validator
import ntpath

## SETUP
__author__ = "Gabriel Bassett"

# Default Configuration Settings
cfg = {
    'log_level': 'warning',
    'log_file': None,
    'schemafile': "../vcdb/verisc.json",
    'enumfile': "../veris/verisc-enum.json",
    'mergedfile': "../veris/verisc-merged.json",
    'vcdb':False,
    'version':"1.3",
    'countryfile':'all.json',
    'output': os.getcwd(),
    'check': False,
    'repositories': ""
}


## FUNCTION DEFINITION
# from http://chase-seibert.github.io/blog/2014/04/23/python-imp-examples.html
def import_from_dotted_path(dotted_names, path=None):
    """ import_from_dotted_path('foo.bar') -> from foo import bar; return bar """
    next_module, remaining_names = dotted_names.split('.', 1)
    fp, pathname, description = imp.find_module(next_module, path)
    module = imp.load_module(next_module, fp, pathname, description)
    if hasattr(module, remaining_names):
        return getattr(module, remaining_names)
    if '.' not in remaining_names:
        return module
    return import_from_dotted_path(remaining_names, path=module.__path__)

class importVeris():
    scripts = {"stdexcel": "../bin/import_stdexcel.py"}
    cfg = None
    rules = None
    mergeSchema = None
    checkValidity = None
    validator = None

    def __init__(self, cfg=None, scripts=None):
        self.cfg = cfg
        veris_logger.updateLogger(cfg, None, dateFmt) 
        if scripts is not None:
            self.scripts = json.loads(scripts)
        else:
            ## I feel bad about this hard coding.  Sorry. - gdb 081516
            if cfg['version'] == "1.3":
                self.scripts = {"vzir": cfg.get("dbir_private", "").rstrip("/") + "/bin/sg-to-vzir1_3.py",
                           "vcdb": cfg.get("dbir_private", "").rstrip("/") + "/bin/sg-to-vcdb1_3.py",
                           "sg": cfg.get("dbir_private", "").rstrip("/") + "/bin/sg-to-partner1_3.py",
                           "stdexcel": cfg.get("veris", "").rstrip("/") + "/bin/import_stdexcel1_3.py"
                           }
            elif cfg['version'] == "1.3.1":
                self.scripts = {"vzir": cfg.get("dbir_private", "").rstrip("/") + "/bin/sg-to-vzir1_3_1.py",
                               "vcdb": cfg.get("dbir_private", "").rstrip("/") + "/bin/sg-to-vcdb1_3_1.py",
                               "sg": cfg.get("dbir_private", "").rstrip("/") + "/bin/sg-to-partner1_3_1.py",
                               "stdexcel": cfg.get("veris", "").rstrip("/") + "/bin/import_stdexcel1_3_1.py"
                               }
            else:
                raise AttributeError("Cannot find scripts.  Please pass in a dictionary with a keys of 'vzir', 'vcdb', 'sg', and 'stdexcel' and values of a valid path to the import file.")

        for name, script in self.scripts.iteritems():
            # try:
                # logger.debug("Importing {0} from {1}.".format(name, self.scripts[name]))
                # # split the filename out to file and name portions.
                # head, tail = ntpath.split(script)
                # # strip the '.py' off the file
                # tail = tail.rstrip(".py")
                # # Import
                # self.scripts[name] = import_from_dotted_path(".".join([tail, "CSVtoJSON"]), [head])

            try:
                logging.debug("Importing {0} from {1}.".format(name, self.scripts[name]))
                self.scripts[name] = imp.load_source(name, script)
            except Exception as e:
                logging.warning("{0} with file {1} didn't import due to {2}".format(name, self.scripts[name], e))
                self.scripts[name] = None
        # import
       # import the rules module
        self.rules = imp.load_source("addrules", cfg.get("veris", "../").rstrip("/") + "/bin/rules.py")
        # import the merge schemas module
        self.mergeSchema = imp.load_source("mergeSchema", cfg.get("veris", "../").rstrip("/") + "/bin/mergeSchema.py")
        # import validation module
        self.checkValidity = imp.load_source("checkValidity", cfg.get("veris", "../").rstrip("/") + "/bin/checkValidity.py")

        # create validator
        if os.path.isfile(cfg.get('mergedfile', '')):
            with open(cfg['mergedfile'], 'r') as filehandle:
                merged = json.load(filehandle)
        else:
            with open(cfg['schemafile'], 'r') as filehandle:
                schema = json.load(filehandle)
            with open(cfg['labelsfile'], 'r') as filehandle:
                labels = json.load(filehandle)
            merged = self.mergeSchema.merge(schema, labels)
        self.validator = Draft4Validator(merged)

    ## MAIN LOOP EXECUTION
    def main(self, cfg=None):
        if cfg is None:
            cfg = self.cfg
        veris_logger.updateLogger(cfg, None, dateFmt)
        logging.info('Beginning main loop.')

        # get the partner name
        if 'source' in cfg:
            source = cfg['source']
        else:
            source = cfg['input'].split("/")[-2].lower()
            source = ''.join([e for e in source if e.isalnum()])
            cfg['source'] = source

        logging.info("Starting import of {0}.".format(source))
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
        ## Look at column names
        with open(cfg['input'], 'rU') as filehandle:
            line = filehandle.readline()  # read the column headers. SurveyGizmo has lots of ":" while stdexcel has "."
        c_count = line.count(":")
        p_count = line.count(".")
        ### choose based on column names
        if c_count > p_count:
            script = "sg"
            ## If partner is 'vzir', use vzir.
            if source == "vzir":
                script = "vzir"
            ## If partner is 'vcdb', use vcdb
            elif source == "vcdb":
                script = "vcdb"
        else:
            script = "stdexcel"
        logging.debug("File type is {0}.".format(script))

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
        try:
            logging.warning("Script is {0}.".format(script))
            impVERIS = self.scripts[script].CSVtoJSON(cfg)
        except AttributeError:
            logging.debug("Raising AttributeError configuring script {0}.".format(script))
            raise

        for iid, incident_json in impVERIS.main():

            # run correlated fields using script
            incident_json = self.rules.makeValid(incident_json, cfg)
            incident_json = self.rules.addRules(incident_json, cfg)


            # Verify records
            try:
                #validate(incident, schema)
                self.validator.validate(incident_json)
                self.checkValidity.main(incident_json)
            except ValidationError as e:
                offendingPath = '.'.join(str(x) for x in e.path)
                if "row_number" in incident_json.get("plus", {}):
                    logging.warning("ERROR in {0} at line {1} from {2}: {3}".format(
                        incident_json["incident_id"], incident_json['plus']['row_number'], cfg['input'], e.message))
                else:
                    logging.warning("ERROR in {0} from {1}: {2}".format(incident_json["incident_id"], cfg['input'], e.message))
                #logging.warning("ERROR in %s. %s %s" % (eachFile, offendingPath, e.message)) # replaced with above. - gdb 06/11/16

            # return the updated, validated, incident
            yield iid, incident_json


        logging.info('Ending main loop.')



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
    parser.add_argument("--dbir_private", required=False, help="The location of the dbirR repository.")
    parser.add_argument('-a', '--analyst', help="The analyst to use if no analyst exists in record or if --force_analyst is set.")
    parser.add_argument("-m","--mergedfile", help="The fully merged json schema file.")
    parser.add_argument("-s","--schemafile", help="The JSON schema file")
    parser.add_argument("-e","--enumfile", help="The JSON file with VERIS enumerations")
    parser.add_argument("--labelfile", help="The JSON file with VERIS labels.  Required along with schemafile if mergedfile not provided.")

    parser.add_argument("--vcdb",help="Convert the data for use in VCDB",action="store_true")
    parser.add_argument("--version", help="The version of veris in use")
    parser.add_argument('--conf', help='The location of the config file', default="./_checkValidity.cfg")
    parser.add_argument('--year', help='The DBIR year to assign tot he records.')
    parser.add_argument('--countryfile', help='The json file holdering the country mapping.')
    parser.add_argument('--source', help="Source_id to use for the incidents. Partner pseudonym.")
    parser.add_argument("-f", "--force_analyst", help="Override default analyst with --analyst.", action='store_true')
    parser.add_argument("--check", help="Generate VERIS json records from the input csv, but do not write them to disk. " + 
                              "This is to allow finding errors in the input csv without creating any files.", action='store_true')
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).iteritems() if v is not None}

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
        if "year" in cfg:
            cfg["year"] = int(cfg["year"])
        else:
            cfg["year"] = int(datetime.now().year)
        veris_logger.updateLogger(cfg, None, dateFmt) 
        logging.debug("config import succeeded.")
    except Exception as e:
        logging.warning("config import failed with error {0}.".format(e))
        #raise e
        pass

    cfg.update(args)

    if cfg.get('check', False) == True:
        # _ = cfg.pop('output')
        logging.info("Output files will not be written")
    else:
        logging.info("Output files will be written to %s", cfg["output"])

    cfg["vcdb"] = {True:True, False:False, "false":False, "true":True}[str(cfg.get("vcdb", 'false')).lower()]
    cfg["check"] = {True:True, False:False, "false":False, "true":True}[str(cfg.get("check", 'false')).lower()]

    veris_logger.updateLogger(cfg, None, dateFmt) 
    logging.debug(args)
    logging.debug(cfg)

    # Instantiate the class
    inV = importVeris(cfg)

    if not cfg.get('check', False):
        logging.info("Output files will be written to %s",cfg["output"])
    else:
        logging.info("'check' setting is {0} so files will not be written.".format(cfg.get('check', False)))
    for iid, incident_json in inV.main(cfg):
        if not cfg.get('check', False):    
            # write the json to a file
            if cfg["output"].endswith("/"):
                dest = cfg["output"] + incident_json['plus']['master_id'] + '.json'
                # dest = args.output + outjson['incident_id'] + '.json'
            else:
                dest = cfg["output"] + '/' + incident_json['plus']['master_id'] + '.json'
                # dest = args.output + '/' + outjson['incident_id'] + '.json'
            logging.info("%s: writing file to %s", iid, dest)
            try:
                fwrite = open(dest, 'w')
                fwrite.write(json.dumps(incident_json, indent=2, sort_keys=True))
                fwrite.close()
            except UnicodeDecodeError:
                print incident_json
