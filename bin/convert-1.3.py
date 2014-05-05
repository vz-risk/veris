import simplejson as sj
import argparse
import logging
from glob import glob
import os

def getCountryCode():
    country_codes = sj.loads(open('all.json').read())
    country_code_remap = {'Unknown':'000000'}
    for eachCountry in country_codes:
        try:
            country_code_remap[eachCountry['alpha-2']] = eachCountry['region-code']
        except:
            country_code_remap[eachCountry['alpha-2']] = "000"
        try:
            country_code_remap[eachCountry['alpha-2']] += eachCountry['sub-region-code']
        except:
            country_code_remap[eachCountry['alpha-2']] += "000"
    return country_code_remap

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Converts VERIS 1.2 incidents to v1.3")
    parser.add_argument("-l", "--logging", choices=["critical", "warning", "info"],
                        help="Minimum logging level to display", default="warning")
    parser.add_argument("-p", "--path", nargs='+', help="list of paths to search for incidents")
    parser.add_argument("-o", "--output", help="output file to write new files. Default is to overwrite.")
    args = parser.parse_args()
    logging_remap = {'warning': logging.WARNING, 'critical': logging.CRITICAL, 'info': logging.INFO}
    logging.basicConfig(level=logging_remap[args.logging])
    data_paths = [x + '/*.json' for x in args.path]
    country_region = getCountryCode()

    for eachDir in data_paths:
        for eachFile in glob(eachDir):
          logging.info("Now processing %s" % eachFile)
          try:
              incident = sj.loads(open(eachFile).read())
          except sj.scanner.JSONDecodeError:
              logging.warning("ERROR: %s did not parse properly. Skipping" % eachFile)
              continue

          # Update the schema version
          incident['schema_version'] = "1.3.0"

          # Make the external actor country a list
          if type(incident.get('actor',{}).get('external',{}).get('country',[])) != type(list()):
            logging.info("\tChanging actor.external.country to list.")
            incident['actor']['external']['country'] = [incident['actor']['external']['country']]

          # Make the partner actor country a list
          if type(incident.get('actor',{}).get('partner',{}).get('country',[])) != type(list()):
            logging.info("\tChanging actor.partner.country to list.")
            incident['actor']['partner']['country'] = [incident['actor']['external']['country']]

          # Make the victim country a list
          if type(incident.get('victim',{}).get('country',[])) != type(list()):
            logging.info("\tChanging victim.country to list.")
            incident['victim']['country'] = [incident['victim']['country']]

          # Make the asset country a list
          if type(incident.get('asset',{}).get('country',[])) != type(list()):
            logging.info("\tChanging asset.country to list.")
            incident['asset']['country'] = [incident['asset']['country']]

          # Create region codes
          logging.info("\tWriting region codes")
          if 'country' in incident['actor'].get('external',{}):
            incident['actor']['external']['region'] = []
            for each in incident['actor']['external']['country']:
              incident['actor']['external']['region'].append(country_region[each])
          if 'country' in incident['actor'].get('partner',{}):
            incident['actor']['partner']['region'] = []
            for each in incident['actor']['partner']['country']:
              incident['actor']['partner']['region'].append(country_region[each])
          if 'country' in incident['victim']:
            incident['victim']['region'] = []
            for each in incident['victim']['country']:
              incident['victim']['region'].append(country_region[each])
          if 'region' in incident['actor'].get('external',{}):
            incident['actor']['external']['region'] = list(set(incident['actor']['external']['region']))
          if 'region' in incident['actor'].get('partner',{}):
            incident['actor']['partner']['region'] = list(set(incident['actor']['partner']['region']))
          if 'region' in incident['victim']:
            incident['victim']['region'] = list(set(incident['victim']['region']))

          # Build a whole new physical section
          if 'physical' in incident['action']:
            logging.info("\tbuilding a new physical section")
            new_physical = {'variety':[],'vector':[]}
            new_physical['vector'] = incident['action']['physical']['location']
            new_physical['variety'] = incident['action']['physical']['variety']
            for each in incident['action']['physical']['vector']:
              if each in ["Bypassed controls","Disabled controls"]:
                new_physical['variety'].append(each)
            incident['action']['physical'] = new_physical

          # management, hosting, ownership, accessibility
          logging.info("\tFixing the asset management, hosting, ownership, and accessibility")
          incident['asset']['governance'] = []
          if 'Victim' in incident['asset'].get('ownership',[]):
            incident['asset']['governance'].append("Personally owned")
          if 'Partner' in incident['asset'].get('ownership',[]):
            incident['asset']['governance'].append("3rd party owned")
          if 'External' in incident['asset'].get('management',[]):
            incident['asset']['governance'].append("3rd party managed")
          for h in ['External shared', 'External dedicated', 'External']:
            if h in incident['asset'].get('hosting',[]):
                incident['asset']['governance'].append("3rd party hosted")
          incident['asset']['governance'] = list(set(incident['asset']['governance']))
          if len(incident['asset']['governance']) == 0:
            incident['asset'].pop('governance')
          if 'Isolated' in incident['asset'].get('accessibility',[]):
            incident['asset']['governance'].append("Internally isolated")
          if 'management' in incident['asset']:
            incident['asset'].pop('management')
          if 'hosting' in incident['asset']:
            incident['asset'].pop('hosting')
          if 'ownership' in incident['asset']:
            incident['asset'].pop('ownership')
          if 'accessibility' in incident['asset']:
            incident['asset'].pop('accessibility')

          # Fix the discovery_method
          logging.info("\tFixing the discovery_method")
          if incident['discovery_method'] == 'Int - reported by user':
            incident['discovery_method'] = 'Int - reported by employee'
          if incident['discovery_method'] == 'Int - IT audit':
            incident['discovery_method'] = 'Int - IT review'

          # Rename embezzlement to posession abuse
          logging.info("\tRenaming embezzlement to posession abuse")
          if 'Embezzlement' in incident['action'].get('misuse',{}).get('variety',[]):
            pos = incident['action']['misuse']['variety'].index('Embezzlement')
            incident['action']['misuse']['variety'][pos] = "Possession abuse"

          # Rename misappropriation to Repurpose
          logging.info("\tRenaming misappropriation to repurpose")
          if 'Misappropriation' in incident['attribute'].get('integrity',{}).get('variety',[]):
            pos = incident['attribute']['integrity']['variety'].index('Misappropriation')
            incident['attribute']['integrity']['variety'][pos] = "Repurpose"

          # Rename related_incidents
          if incident.get('related_incidents',"") != "":
            incident['campaign_id'] = incident['related_incidents']
          if "related_incidents" in incident:
            incident.pop('related_incidents')

          #Now save the finished incident
          if args.output:
            outfile = open(os.path.join(args.output,os.path.basename(eachFile)),'w')
          else:
            outfile = open(eachFile,'w')
          outfile.write(sj.dumps(incident,indent=2,sort_keys=True))
          outfile.close()
