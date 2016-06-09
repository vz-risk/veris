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
import importlib

## SETUP
__author__ = "Gabriel Bassett"




## FUNCTION DEFINITION
pass



## MAIN LOOP EXECUTION
def main(cfg, logger):
    logger.info('Beginning main loop.')

    # import the 4 different veris conversion scripts
    scripts = {"vzir": cfg["dbir-private"].rstrip("/") + "/bin/sg-to-dbir1_3.py",
               "vcdb": cfg["dbir-private"].rstrip("/") + "/bin/sg-to-vcdb1_3.py",
               "sg": cfg["dbir-private"].rstrip("/") + "/bin/sgpartner_to_dbir.py",
               "stdexcel": cfg["veris"].rstrip("/") + "/bin/import_stdexcel.py"
               }
    for name, script in scripts.iteritems():
        scripts[name] = importlib.import_module(script)


    # get the partner name
    source = cfg['inFile'].split("/")[-2].lower()
    source = ''.join([e for e in source if e.isalnum()])

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
    with open(cfg['inFile'], 'rU') as filehandle:
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


    # TODO: run correlated fields using script


    # TODO: verify records


    logger.info('Ending main loop.')



# do the whole config thing thing
if __name__ == '__main__':

    ## Gabe
    ## The general Apprach to config parsing (Probably not the best way)
    ## 1. create a dictionary called 'cfg' of fallback values (up at the top of the file)
    ## 2. parse the arguments (args) and turn into a dictionary if the value is not None
    ## 3. Use the config from the command line parser to read the config file and update the 'cfg' dictionary
    ## 4. Update the cfg dictionary with the arguements (args) from the command line

    # 1. TODO


    # 2. TODO


    # 3. TODO


    # 4. TODO


    main(cfg, logger)
