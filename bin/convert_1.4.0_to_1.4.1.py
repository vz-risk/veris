import json as sj
import argparse
import logging
from glob import glob
import os
from fnmatch import fnmatch
import configparser
from tqdm import tqdm
# import imp
from importlib import util
import pprint
import re

# from distutils.version import LooseVersion
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    spec = util.spec_from_file_location("veris_logger", script_dir + "/veris_logger.py")
    veris_logger = util.module_from_spec(spec)
    spec.loader.exec_module(veris_logger)
    # veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    print("Script dir: {0}.".format(script_dir))
    raise

cfg = {
    'log_level': 'warning',
    'log_file': None,
    'countryfile': './all.json'
}


def getCountryCode(countryfile):
    # country_codes = sj.loads(open(countryfile).read())
    with open(countryfile, 'r') as filehandle:
        country_codes = sj.load(filehandle)
    country_code_remap = {'Unknown': '000000'}
    for eachCountry in country_codes:
        try:
            country_code_remap[eachCountry['alpha-2']] = \
                eachCountry['region-code']
        except:
            country_code_remap[eachCountry['alpha-2']] = "000"
        try:
            country_code_remap[eachCountry['alpha-2']] += \
                eachCountry['sub-region-code']
        except:
            country_code_remap[eachCountry['alpha-2']] += "000"
    return country_code_remap


def getField(current, txt):
    tsplit = txt.split('.', 1)
    if tsplit[0] in current:
        result = current[tsplit[0]]
        if len(tsplit) > 1:
            result = getField(result, tsplit[1])
    else:
        result = None
    return result


def grepText(incident, searchFor):
    txtFields = ['summary', "notes", "victim.notes", "actor.external.notes",
                 "actor.internal.notes", "actor.partner.notes",
                 "actor.unknown.notes", "action.malware.notes",
                 "action.hacking.notes", "action.social.notes",
                 "action.misuse.notes", "action.physical.notes",
                 "action.error.notes", "action.environmental.notes",
                 "asset.notes", "attribute.confidentiality.notes",
                 "attribute.integrity.notes", "attribute.availability.notes",
                 "impact.notes", "plus.analyst_notes", "plus.pci.notes"]
    foundAny = False
    for txtField in txtFields:
        curText = getField(incident, txtField)
        if isinstance(curText, str):  # replaced basestr with str per 2to3. - GDB 181109
            if searchFor.lower() in curText:
                foundAny = True
                break
        # could be extended to look for fields in lists
    return foundAny


def main(cfg):
    veris_logger.updateLogger(cfg)

    last_version = "1.4.0"
    version = "1.4.1"

    if cfg.get('log_level', '').lower() == "debug":
        pprint.pprint(cfg)  # DEBUG

    logging.info("Converting files from {0} to {1}.".format(cfg["input"], cfg["output"]))
    for root, dirnames, filenames in tqdm(os.walk(cfg['input'])):
        logging.info("starting parsing of directory {0}.".format(root))
        # filenames = filter(lambda fname: fnmatch(fname, "*.json"), filenames)
        filenames = [fname for fname in filenames if fnmatch(fname.lower(), "*.json")]  # per 2to3. - GDB 181109
        if filenames:
            dir_ = os.path.join(cfg['output'], root[len(cfg['input']):].lstrip(
                "/"))  # if we don't strip the input, we get duplicate directories
            logging.info("Output directory is {0}.".format(dir_))
            if not os.path.isdir(dir_):
                os.makedirs(dir_)
            for fname in filenames:
                in_fname = os.path.join(root, fname)
                out_fname = os.path.join(dir_, fname)

                logging.info("Now processing %s" % in_fname)
                try:
                    # incident = sj.loads(open(in_fname).read())
                    with open(in_fname, 'r') as filehandle:
                        incident = sj.load(filehandle)
                except sj.JSONDecodeError:
                    logging.warning(
                        "ERROR: %s did not parse properly. Skipping" % in_fname)
                    continue

                if 'assets' not in incident.get('asset', {}):
                    raise KeyError("Asset missing from assets in incident {0}.".format(fname))

                # if the record is already version 1.3.6, skip it. This can happen if there are mixed records
                if incident.get('schema_version', last_version) != last_version:
                    if incident.get('schema_version', '') != version:
                        logging.warning(
                            "Incident {0} is version {1} instead of {2} and can therefore not be updated.".format(fname,
                                                                                                                  incident.get(
                                                                                                                      'schema_version',
                                                                                                                      'NONE'),
                                                                                                                  last_version))
                    continue

                # Update the schema version
                incident['schema_version'] = version

                # EXAMPLE UPDATE
                #             # Replace asset S - SCADA with S - ICS
                #             # Issue 104, Commit f8b7387
                #             # if "S - SCADA" in incident.get("asset", {}).get("assets", []):
                #                 # incident["asset"]["assets"] = [e.replace("S - SCADA", "S - ICS") for e in incident["asset"]["assets"]]
                #             incident["asset"]["assets"] = [dict(e, **{u"variety": u"S - ICS"}) if e.get(u"variety", "") ==  u"S - SCADA" else e for e in incident["asset"]["assets"]]

                # Per https://github.com/vz-risk/veris/issues/271
                # infer actor.*.motive.Secondary if malware.variety.DoS
                # Now to save the incident


                ##ISSUE 420 (lol) Update PCI standard to the new version which requires adding additional fields and moving over the fields
                # if 'pci' in incident.get("plus", {}):
                #
                #     # start the dictionary of PCI values
                #     pci_dict = {"In Place": "Yes",
                #                 "Not Applicable": "Not Assessed",
                #                 "Not In Place": "No",
                #                 "Unknown":"Not Assessed"
                #     }
                #
                #     # Need to create the new hierarchy to add the subvalues to
                #     # Do a check before we accidentally remove this field
                #     if 'requirements' not in incident.get('plus',{}).get('pci',{}):
                #         incident['plus']['pci']['requirements'] = {}
                #
                #     # loop through the values that have "req_" and iterate through those [extract out the ones that start with req
                #     # with those values you can know look up and transfer the values
                #     for y in [x for x in incident.get('plus',{}).get('pci', {}) if x.startswith('req_')]:
                #         old_value = incident.get('plus', {}).get('pci', {}).get(y)
                #         incident['plus']['pci']['requirements'][y] = {}
                #         incident['plus']['pci']['requirements'][y]['in_place'] = pci_dict.get(old_value)
                #         incident['plus']['pci'].pop(y, None)

                #Issue https://github.com/vz-risk/veris/issues/414 Discovery_notes is found in the root of the incident
                # it should really be at the root  of discovery_method, this update will make that happen
                #: do we need to ensure we capture if there's a discovery_note BUT no discovery?? seems unlikely considerng discovery_method is required
                # if incident.get("discovery_notes", {}) and incident.get('discovery_method', {}):
                #     incident['discovery_method']['discovery_notes'] = incident.get('discovery_notes')
                #     incident.pop('discovery_notes', None)



                # 486 Create a new Server asset variety for a Secrets Vault and convert N - HSM to S - Secrets Vault
                if any("N - HSM" in x.get("variety") for x in incident.get('asset', {}).get("assets", [])):

                    incident["asset"]["assets"] = [
                        dict(e, **{u"variety": u"S - Secrets vault"}) if e.get(u"variety", "") == u"N - HSM" else e for e in
                        incident["asset"]["assets"]]

                    # # Check to see if there's any additional network devices in the list
                    # network_list =["N - " in x for x in incident.get('asset',{}).get("assets",{}).get("variety",[])]
                    # #if there's NO OTHER networking devices, then we remove the Network level enumerations
                    # if not any(network_list):
                    #     assets = incident.get('asset',{}).get("variety",[])
                    #     assets.remove("Network")
                    #     incident['asset']['variety'] = assets
                    #
                    # # Now we just check to see if there's any Servers in the enumeration and if not, we addd it
                    # if "Server" not in incident.get('asset', {}).get("variety", []):
                    #     assets = incident.get('asset', {}).get("variety", [])
                    #     assets.append("Server")
                    #
                    #     incident['asset']['variety'] = assets

                # 493 Change "S - Remote Access" to an "N - Remote access" asset
                # this requires updating replacing the value and also updating the asset variety From Server to N (if it's the only networking device)
                #

                if any("S - Remote access" in x.get("variety") for x in incident.get('asset', {}).get("assets", [])):
                    #incident['asset']['assets']['variety'] = [e.replace("S - Remote Access", "N - Remote Access") for e in
                    #                                            incident['asset']['assets']['variety']]

                    incident["asset"]["assets"] = [
                        dict(e, **{u"variety": u"N - Remote access"}) if e.get(u"variety", "") == u"S - Remote access" else e for
                        e in
                        incident["asset"]["assets"]]


                    # Ok we have replaced the bottom enumeration, check to see if there's no OTHER server
                    # server_list = ["S - " in x for x in incident.get('asset', {}).get("assets", {}).get("variety", [])]
                    # if not any(server_list):
                    #     assets = incident.get('asset',{}).get("variety",[])
                    #     assets.remove("Server")
                    #     incident['asset']['variety'] = assets
                    #
                    # # add the Network if there's not one
                    # if "Network" not in incident.get('asset',{}).get("variety",[]):
                    #     assets = incident.get('asset',{}).get("variety",[])
                    #     assets.append("Network")
                    #
                    #     incident['asset']['variety'] = assets



                # 496 attribute.Confidentiality.Partner data" duplicative?
                # Let's remove "Partner data" from the schema and add the "Partner" option to "Data victim" on the ones that happened to have that "Partner data" option selected.
                # plus.attribute.confidentiality.partner_data
                # we have to figure out what we want to do partner_numberl there's a handful of cases (review the issue)
                if "Yes" in incident.get("plus",{}).get("attribute",{}).get("confidentiality",{}).get("partner_data",[]):
                    # check to see if partner is in data victim
                    if "Partner" not in incident.get("attribute",{}).get("confidentiality",{}).get("data_victim",[]):
                        victims = incident.get("attribute",{}).get("confidentiality",{}).get("data_victim",[])
                        victims.append("Partner")
                        incident['attribute']['confidentiality']['data_victim'] = victims

                    # now we need to remove this value since it's no longer in veris
                    incident['plus']['attribute'].get('confidentiality',{}).pop("partner_data")

                    # With this approach there is a edge case where there's as partner number but not partner_data
                    if incident.get("plus",{}).get("attribute",{}).get("confidentiality",{}).get("partner_number",""):
                        # temp logic until full determination, if partner_number == data_total, leave it, otherwise add it in
                        partner_number = incident.get("plus",{}).get("attribute",{}).get("confidentiality",{}).get("partner_number","")
                        data_total = incident.get('attribute',{}).get("confidentiality", {}).get("data_total","")

                        # I believe this field by defintion CAN ONLY be an integer, so we're going to force that
                        if int(partner_number) != int(data_total):
                            data_total = int(partner_number) + int(data_total)
                            incident['attribute']['confidentiality']['data_total'] = data_total

                        incident['plus']['attribute'].get('confidentiality',{}).pop("partner_number")
                    if len(incident.get("plus",{}).get("attribute",{}).get("confidentiality",{})) < 1:
                        incident['plus'].get('attribute',{}).pop('confidentiality')

                    if len(incident.get("plus",{}).get("attribute",{})) < 1:
                        incident.get('plus',{}).pop("attribute")
                        # no need to pop anything more, plus is a required field that will have data







                # 495 Use attribute.Confidentiality.Data abuse to capture the (ab)use of the data for ransom (i.e. single or double extortion)
                # We need to ensure all current Malware.Ransomware cases get the new "Data abuse" flag set before any changes we might want to do at

                if "Ransomware" in incident.get("action",{}).get("malware",{}).get("variety",[]):
                    if "Yes" in incident.get("attribute",{}).get("confidentiality",{}).get("data_disclosure",[]) \
                        or "Unknown" in incident.get("attribute",{}).get("confidentiality",{}).get("data_disclosure",[]) :

                        incident['attribute']['confidentiality']['data_abuse'] = "Yes - Data ransomed"
                    #






                logging.info("Writing new file to %s" % out_fname)
                with open(out_fname, 'w') as outfile:
                    sj.dump(incident, outfile, indent=2, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    descriptionText = "Converts VERIS 1.4.0 incidents to v1.4.1"
    helpText = "output directory to write new files. Default is to overwrite."
    parser = argparse.ArgumentParser(description=descriptionText)
    parser.add_argument("-l", "--log_level", choices=["critical", "warning", "info", "debug"],
                        help="Minimum logging level to display")
    parser.add_argument('--log_file', help='Location of log file')
    parser.add_argument("-i", "--input", required=True,
                        help="top level folder to search for incidents")
    parser.add_argument("-o", "--output",
                        help=helpText)
    # parser.add_argument('--countryfile', help='The json file holdering the country mapping.')
    parser.add_argument('--conf', help='The location of the config file', default="../user/data_flow.cfg")
    args = parser.parse_args()
    args = {k: v for k, v in vars(args).items() if v is not None}

    # logging_remap = {'warning':logging.WARNING, 'critical':logging.CRITICAL, 'info':logging.INFO, 'debug':logging.DEBUG} # defined above. - gdb 080716

    # Parse the config file
    try:
        config = configparser.ConfigParser()
        # config.readfp(open(args["conf"]))
        with open(args['conf'], 'r') as filehandle:
            config.readfp(filehandle)
        cfg_key = {
            'GENERAL': ['report', 'input', 'output', 'analysis', 'year', 'force_analyst', 'version', 'database',
                        'check'],
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
        # raise e
        pass
    # place any unique config file parsing here
    if "input" in cfg:
        cfg["input"] = [l.strip() for l in cfg["input"].split(" ,")]  # spit to list

    cfg.update(args)

    if "output" not in cfg:
        cfg["output"] = cfg["input"]

    veris_logger.updateLogger(cfg)

    # country_region = getCountryCode(cfg['countryfile'])

    # assert args.path != args.output, "Source and destination must differ"

    main(cfg)
