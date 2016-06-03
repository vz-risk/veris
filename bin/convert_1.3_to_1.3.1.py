import json as sj
import argparse
import logging
from glob import glob
import os
from fnmatch import fnmatch


def getCountryCode():
    country_codes = sj.loads(open('all.json').read())
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
        if isinstance(curText, basestring):
          if searchFor.lower() in curText:
              foundAny = True
              break
        # could be extended to look for fields in lists
    return foundAny

if __name__ == '__main__':
    descriptionText = "Converts VERIS 1.3 incidents to v1.3.1"
    helpText = "output file to write new files. Default is to overwrite."
    parser = argparse.ArgumentParser(description=descriptionText)
    parser.add_argument("-l", "--logging", choices=["critical",
                                                    "warning", "info"],
                        help="Minimum logging level to display",
                        default="warning")
    parser.add_argument("-p", "--path", required=True,
                        help="top level folder to search for incidents")
    parser.add_argument("-o", "--output", required=True,
                        help=helpText)
    args = parser.parse_args()
    logging_remap = {'warning': logging.WARNING, 'critical': logging.CRITICAL,
                     'info': logging.INFO}
    logging.basicConfig(level=logging_remap[args.logging])
    country_region = getCountryCode()

    assert args.path != args.output, "Source and destination must differ"
    for dirpath, dirnames, filenames in os.walk(args.path):
      filenames = filter(lambda fname: fnmatch(fname, "*.json"), filenames)
      if filenames:
        dir_ = os.path.join(args.output, dirpath[1:])
        os.makedirs(dir_)
        for fname in filenames:
          in_fname = os.path.join(dirpath,fname)
          out_fname = os.path.join(dir_, fname)

          logging.info("Now processing %s" % in_fname)
          try:
              incident = sj.loads(open(in_fname).read())
          except sj.scanner.JSONDecodeError:
              logging.warning(
                  "ERROR: %s did not parse properly. Skipping" % in_fname)
              continue

          # Update the schema version
          incident['schema_version'] = "1.3.1"

          # Fix other/unknown in asset.variety
          # Issue 110, Commit 366f810 (branch v1_3_1)
          for enum in [
            ("M - Other", "M - Unknown"),
            ("N - Other", "N - Unknown"),
            ("P - Other", "P - Unknown"),
            ("S - Other", "S - Unknown"),
            ("T - Other", "T - Unknown"),
            ("U - Other", "U - Unknown")
          ]:
            if enum[0] in incident.get("asset", {}).get("assets", []):
              incident["asset"]["assets"] = [enum.replace(e[0], e[1])  for e in incident["asset"]["assets"]]

          # Now to save the incident
          logging.info("Writing new file to %s" % out_fname)
          outfile = open(out_fname, 'w')
          outfile.write(sj.dumps(incident, sort_keys=True, indent=2))
          outfile.close()
