#!/usr/bin/env python
"""
 AUTHOR: Gabriel Bassett
 DATE: 06-09-16
 DEPENDENCIES: <a list of modules requiring installation>
 

 DESCRIPTION:
 Meant to be imported.  Takes json records and adds rules for correlated enumerations.
 that may have been left out of the original source file.

 NOTES:
 <No Notes>

 ISSUES:
 <No Issues>

 TODO:
 <No TODO>

"""
# PRE-USER SETUP
import logging
#import imp
import importlib
import os
import sys
script_dir = os.path.dirname(os.path.realpath(__file__))
try:
    spec = importlib.util.spec_from_file_location("veris_logger", script_dir + "/veris_logger.py")
    veris_logger = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(veris_logger)
    # veris_logger = imp.load_source("veris_logger", script_dir + "/veris_logger.py")
except:
    logging.debug("Script dir: {0}.".format(script_dir))
    print("Script dir: {0}.".format(script_dir))
    raise
#import veris_logger

########### NOT USER EDITABLE ABOVE THIS POINT #################


# USER VARIABLES
#LOGLEVEL = logging.DEBUG
#LOG = None

########### NOT USER EDITABLE BELOW THIS POINT #################


## IMPORTS
import argparse
import configparser
import os
import json
#from datetime import datetime, date
#from distutils.version import LooseVersion
from tqdm import tqdm
from pprint import pprint, pformat
from collections import defaultdict

## SETUP
cfg = {
    'log_level': 'warning',
    'log_file': None#,
#    'schemafile': "../vcdb/veris.json",
#    'enumfile': "../vcdb/veris-enum.json",
#    'vcdb':False,
#    'version':"1.3",
#    'countryfile':'all.json',
#    'output': None,
#    'quiet': False,
#    'repositories': "",
#    'force_analyst': False,
#    'year': date.today().year
}

## FUNCTION DEFINITION

class VERISmm():
    version = 0.1
    cfg = None
    rating = {
        "a4_1": 0, 
        "incident_1": 0,
        "timeline_1": 0,
        "timeline_2": 0,
        "discovery_1": 0,
        "actor_1": 0,
        "asset_1": 0,
        "action_1": 0,
        "victim_1": 0,
        "attribute_1": 0,
        "asset_2": 0,
        "pattern": 0,
        "victim_2": 0,
        "discovery_2": 0,
        "atk_graph": 0,
        "action_2_blended": 0,
        "actor_2": 0,
        "action_2_tech": 0,
        "attribute_2": 0,
        "targeted_1": 0,
        "action_2_nontech": 0,
        "asset_3": 0,
        "quality_1": 0,
        "timeline_3": 0,
        "y2y": 0,
        "action_3": 0,
        "actor_3": 0,
        "attribute_3": 0,
        "action_3_blended": 0,
        "action_3_technical": 0,
        "actor_4": 0,
        "action_4": 0,
        "victim_3": 0,
        "impact_1": 0,
        "incident_2": 0,
        "a4_2": 0,
        "impact_2": 0,
        "actor_5": 0,
        "incident_3": 0,
        "action_5": 0,
        "controls_1": 0,
        "attribute_4": 0
    }


    def __init__(self, cfg=None):
        if cfg is not None:
            self.cfg = cfg


    def aggregate_ratings(cfg, ratings):
        agg_ratings = defaultdict(int)
        total = len(ratings)

        for rating in ratings:
            for key in ratings[rating].keys():
                try:
                    agg_ratings[key] += ratings[rating][key]
                except:
                    pprint(ratings[rating])
                    pprint(key)
                    raise

        for rating in agg_ratings:
            agg_ratings[rating] = agg_ratings[rating] / float(total)

        return agg_ratings

    def maturity(cfg, agg_ratings):
        all_pct = 1.0
        mat = {}

        # level_1
        mat[1] = bool(
            agg_ratings['a4_1'] >= all_pct and
            agg_ratings['incident_1'] >= all_pct and 
            agg_ratings['timeline_1'] >= all_pct
        )

        # level_2
        mat[2] = bool(
            mat[1] and 
            agg_ratings['timeline_2'] >= all_pct and
            agg_ratings['discovery_1'] >= all_pct and
            agg_ratings['actor_1'] >= all_pct and
            agg_ratings['asset_1'] >= all_pct and
            agg_ratings['action_1'] >= all_pct and
            agg_ratings['attribute_1'] >= all_pct and
            agg_ratings['victim_1'] >= all_pct
        )

        # level_3
        mat[3] = bool(
            mat[2] and 
            agg_ratings['asset_2'] >= all_pct and
            agg_ratings['pattern'] >= all_pct and
            agg_ratings['victim_2'] >= all_pct and
            agg_ratings['discovery_2'] >= all_pct and
            agg_ratings['atk_graph'] >= all_pct and
            agg_ratings['action_2_blended'] >= all_pct and
            agg_ratings['actor_2'] >= all_pct and
            agg_ratings['action_2_technical'] >= all_pct and
            agg_ratings['attribute_2'] >= all_pct and
            agg_ratings['target_1'] >= all_pct and
            agg_ratings['action_2_nontech'] >= all_pct
        )

        # level_4
        mat[4] = bool(
            mat[3] and 
            agg_ratings['asset_3'] >= all_pct and
            #agg_ratings['quality_1'] >= all_pct and
            agg_ratings['timeline_3'] >= all_pct and
            agg_ratings['y2y'] >= all_pct and
            agg_ratings['action_3'] >= all_pct and
            agg_ratings['actor_3'] >= all_pct and
            agg_ratings['attribute_3'] >= all_pct and
            agg_ratings['action_3_blended'] >= all_pct and
            agg_ratings['action_3_technical'] >= all_pct 
        )

        # level_5
        mat[5] = bool(
            mat[4] and 
            agg_ratings['actor_4'] >= all_pct and
            agg_ratings['action_4'] >= all_pct and
            agg_ratings['victim_3'] >= all_pct and
            agg_ratings['impact_1'] >= all_pct

        )

        # level_6
        mat[6] = bool(
            mat[5] and 
            agg_ratings['incident_2'] >= all_pct and
            agg_ratings['a4_2'] >= all_pct and
            agg_ratings['impact_2'] >= all_pct 

        )

        # level_7
        mat[7] = bool(
            mat[6] and 
            agg_ratings['actor_5'] >= all_pct and
            agg_ratings['incident_3'] >= all_pct and
            agg_ratings['action_5'] >= all_pct and
            agg_ratings['controls_1'] >= all_pct and
            agg_ratings['attribute_4'] >= all_pct
        )

        return mat

    def maturity_detail(self, agg_ratings):
        mat = {}

        # level_1
        mat[1] = {
            'a4_1': agg_ratings['a4_1'],
            'incident_1': agg_ratings['incident_1'], 
            'timeline_1': agg_ratings['timeline_1'] 
        }

        # level_2
        mat[2] = {
            'timeline_2': agg_ratings['timeline_2'],
            'discovery_1': agg_ratings['discovery_1'],
            'actor_1': agg_ratings['actor_1'],
            'asset_1': agg_ratings['asset_1'],
            'action_1': agg_ratings['action_1'],
            'attribute_1': agg_ratings['attribute_1'],
            'victim_1': agg_ratings['victim_1']
        }

        # level_3
        mat[3] = {
            'asset_2': agg_ratings['asset_2'],
            'pattern': agg_ratings['pattern'],
            'victim_2': agg_ratings['victim_2'],
            'discovery_2': agg_ratings['discovery_2'],
            'atk_graph': agg_ratings['atk_graph'],
            'action_2_blended': agg_ratings['action_2_blended'],
            'actor_2': agg_ratings['actor_2'],
            'action_2_technical': agg_ratings['action_2_technical'],
            'attribute_2': agg_ratings['attribute_2'],
            'target_1': agg_ratings['target_1'],
            'action_2_nontech': agg_ratings['action_2_nontech']
        }

        # level_4
        mat[4] = {
            'asset_3': agg_ratings['asset_3'],
            #'': agg_ratings['quality_1'],
            'timeline_3': agg_ratings['timeline_3'],
            'y2y': agg_ratings['y2y'],
            'action_3': agg_ratings['action_3'],
            'actor_3': agg_ratings['actor_3'],
            'attribute_3': agg_ratings['attribute_3'],
            'action_3_blended': agg_ratings['action_3_blended'],
            'action_3_technical': agg_ratings['action_3_technical'] 
        }

        # level_5
        mat[5] = {
            'actor_4': agg_ratings['actor_4'],
            'action_4': agg_ratings['action_4'],
            'victim_3': agg_ratings['victim_3'],
            'impact_1': agg_ratings['impact_1']

        }

        # level_6
        mat[6] = {
            'incident_2': agg_ratings['incident_2'],
            'a4_2': agg_ratings['a4_2'],
            'impact_2': agg_ratings['impact_2'] 

        }

        # level_7
        mat[7] = {
            'actor_5': agg_ratings['actor_5'],
            'incident_3': agg_ratings['incident_3'],
            'action_5': agg_ratings['action_5'],
            'controls_1': agg_ratings['controls_1'],
            'attribute_4': agg_ratings['attribute_4']
        }

        return mat


    def rate_one(self, incident):
        ### NOTES:
        ### We will assume that if a field exists, it is validatable VERIS
        ### We will not attempt to validate field values (e.g. month is >= 1, & <= 12)
        ### We will validate single-value enumerations as the existance of the field
        ### We will validate multiple-value enumerations as list length > 0 when 'Unknown' removed
        ### We will validate that string fields are not an empty string

        rating = {}


        #a4_1 
        rating['a4_1'] = bool(
            'attribute' in incident and # attribute.Unknown: all
            'action' in incident and # action.Unknown: all
            'actor' in incident and # actor.Unknown: all
            'assets' in incident.get('asset') # asset.assets.variety: Unknown
        )
        #incident_1
        rating['incident_1'] = bool(
            incident.get('incident_id', '') and # Incident_id: all
            'security_incident' in incident and # security_incident: all
            incident.get('schema_version', '') # schema_version: all
        )
        #timeline_1
        rating['timeline_1'] = bool(
            'year' in incident.get('timeline', {}).get('incident', {}) and # timeline.incident.month: all
            'month' in incident.get('timeline', {}).get('incident', {}) and # timeline.incident.year: all
            'day' in incident.get('timeline', {}).get('incident', {}) # timeline.incident.day: all
        )
        #timeline_2
        rating['timeline_2'] = bool(
            any([k != "Unknown" for k in incident.get("timeline", {}).get("compromise", {}).get("unit", [])]) and # timeline.compromise.unit: all
            any([k != "Unknown" for k in incident.get("timeline", {}).get("discovery", {}).get("unit", [])]) # timeline.discovery.unit: all
        )
        #discovery_1
        rating['discovery_1'] = bool(
            any([k != "Unknown" for k in incident.get("discovery", {}).get("internal", {}).get("variety", [])]) or # discovery_method: some
            any([k != "Unknown" for k in incident.get("discovery", {}).get("external", {}).get("variety", [])]) or  # discovery_method: some
            any([k != "Unknown" for k in incident.get("discovery", {}).get("partner", {}).get("variety", [])]) # discovery_method: some
        )
        #actor_1
        rating['actor_1'] = bool(
            any([k != "Unknown" for k in incident.get("actor", {}).get("internal", {}).get("variety", [])]) or # actor.external.variety: Unknown
            any([k != "Unknown" for k in incident.get("actor", {}).get("external", {}).get("variety", [])]) or # actor.internal.variety: Unknown
            any([k != "Unknown" for k in incident.get("actor", {}).get("partner", {}).get("variety", [])]) # actor.partner.variety: Unknown
        )
        #asset_1 
        rating['asset_1'] = bool(
            any(['variety' in k for k in incident.get('asset', {}).get('assets', [])]) # asset.assets.variety: some
        )
        #action_1
        rating['action_1'] = bool(
            len(incident.get("action", {}).get("environmental", {}).get("variety", [])) > 0 or # action.environmental.variety: Unknown
            len(incident.get("action", {}).get("error", {}).get("variety", [])) > 0 or # action.error.variety: Unknown
            len(incident.get("action", {}).get("malware", {}).get("variety", [])) > 0 or # action.malware.variety: Unknown
            len(incident.get("action", {}).get("hacking", {}).get("variety", [])) > 0 or # action.hacking.variety: Unknown
            len(incident.get("action", {}).get("social", {}).get("variety", [])) > 0 or # action.social.variety: Unknown
            len(incident.get("action", {}).get("misuse", {}).get("variety", [])) > 0 or # action.misuse.variety: Unknown
            len(incident.get("action", {}).get("physical", {}).get("variety", [])) > 0 # action.physical.variety: Unknown
        )
        #victim_1
        rating['victim_1'] = bool(
            incident.get("victim", {}).get("employee_count") != "Unknown" and # victim.employee_count: some
            incident.get('victim', {}).get('industry', '') and # victim.industry2: all
            incident.get('region', {}).get('region', '') # victim.region: all
        )
        #attribute_1
        rating['attribute_1'] = bool(
            'data_disclosure' in incident.get('attribute', {}).get('confidentiality', {'data_disclosures': 'Unknown'}) and # attribute.confidentiality.data_disclosure: all
            (
                any(['variety' in k for k in incident.get('attribute', {}).get('confidentiality', {}).get('data', [])]) or # attribute.confidentiality.data.variety: Unknown
                len(incident.get("attribute", {}).get("integrity", {}).get("variety", [])) > 0 or # attribute.integrity.variety: Unknown
                len(incident.get("attribute", {}).get("availability", {}).get("variety", [])) > 0 # attribute.availability.variety: Unknown
            )
        )
        #asset_2
        rating['asset_2'] = any([k not in ['Unknown', 'P - Unknown', 'M - Unknown', 'N - Unknown', 'S - Unknown', 'T - Unknown', 'U - Unknown', 'E - Unknown'] for k in incident.get('asset', {}).get('assets', [])]) # asset.assets.variety: all
        #pattern
        rating['pattern'] = bool(
            any([k != "Unknown" for k in incident.get("action", {}).get("error", {}).get("variety", [])]) and # action.error.variety: some
            any(['variety' in k for k in incident.get('asset', {}).get('assets', [])]) and # asset.assets.variety: some
            (
                'Web application' in incident.get('action', {}).get('hacking', {}).get('vector', []) or # action.hacking.vector: Web application
                'Direct install' in incident.get('action', {}).get('malware', {}).get('vector', []) or # action.malware.vector: Direct install
                'Payment' in [k['variety'] for k in incident.get('attribute', {}).get('confidentiality', {}).get('data', [])] or # attribute.confidentiality.data.variety: Payment
                'Espionage' in incident.get('actor', {}).get('external', {}).get('motive', []) or # actor.external.motive: Espionage
                len(incident.get("action", {}).get("malware", {}).get("variety", [])) > 0 or # action.malware.variety: all
                len(incident.get("action", {}).get("physical", {}).get("variety", [])) > 0 or # action.physical.variety: some
                len(incident.get("action", {}).get("misuse", {}).get("variety", [])) > 0 or # action.misuse.variety: all
                'DoS' in incident.get('action', {}).get('hacking', {}).get('variety', []) or # action.hacking.variety: DoS
                'State-affiliated' in incident.get('actor', {}).get('external', {}).get('variety', []) # actor.external.variety: State-affiliated
            )
        )
        #victim_2
        rating['victim_1'] = bool(
            incident.get("victim", {}).get("employee_count") != "Unknown" and # victim.employee_count: all
            incident.get('victim', {}).get('industry', '') and # victim.industry: all
            incident.get('region', {}).get('country', '') # victim.country: all
        )
        #discovery_2
        rating['discovery_2'] = bool(
            any([k != "Unknown" for k in incident.get("discovery", {}).get("internal", {}).get("variety", [])]) or # discovery_method: all
            any([k != "Unknown" for k in incident.get("discovery", {}).get("external", {}).get("variety", [])]) or  # discovery_method: all
            any([k != "Unknown" for k in incident.get("discovery", {}).get("partner", {}).get("variety", [])]) # discovery_method: all
        )
        #atk_graph
        rating['atk_graph'] =  bool(
            any([k != "Unknown" for k in incident.get("attribute", {}).get("integrity", {}).get("variety", [])]) and # attribute.integrity.variety: all
            any([k.get('variety', "Unknown") != "Unknown" for k in incident.get('attribute', {}).get('confidentiality', {}).get('data', [])]) and # attribute.confidentiality.data.variety: all
            any([k != "Unknown" for k in incident.get("action", {}).get("malware", {}).get("variety", [])]) and  # action.malware.variety: all
            any([k != "Unknown" for k in incident.get("action", {}).get("physical", {}).get("variety", [])]) and  # action.physical.variety: all
            any([k != "Unknown" for k in incident.get("action", {}).get("misuse", {}).get("variety", [])]) and  # action.misuse.variety: all
            any([k != "Unknown" for k in incident.get("action", {}).get("malware", {}).get("vector", [])]) and  # action.malware.vector: all
            any([k != "Unknown" for k in incident.get("action", {}).get("hacking", {}).get("variety", [])]) and  # action.hacking.variety: all
            any([k != "Unknown" for k in incident.get("action", {}).get("social", {}).get("variety", [])]) and  # action.social.variety: all
            any([k != "Unknown" for k in incident.get("attribute", {}).get("availability", {}).get("variety", [])])  # attribute.availability.variety: all
        )
        #action_2_blended
        rating['action-2_blended'] = bool(
            any([k != "Unknown" for k in incident.get("action", {}).get("misuse", {}).get("variety", [])]) and  # action.misuse.variety: all
            any([k != "Unknown" for k in incident.get("action", {}).get("social", {}).get("variety", [])])  # action.social.variety: all
        )
        #actor_2
        rating['actor_2'] = bool(
            any([k != "Unknown" for k in incident.get("actor", {}).get("internal", {}).get("variety", [])]) or # actor.external.variety: Unknown
            any([k != "Unknown" for k in incident.get("actor", {}).get("external", {}).get("variety", [])]) or # actor.internal.variety: Unknown
            any([k != "Unknown" for k in incident.get("actor", {}).get("partner", {}).get("variety", [])]) # actor.partner.variety: Unknown
        )
        #action_2_tech
        rating['action_2_tech'] = bool(
            any([k != "Unknown" for k in incident.get("action", {}).get("malware", {}).get("variety", [])]) and  # action.malware.variety: all
            any([k != "Unknown" for k in incident.get("action", {}).get("malware", {}).get("vector", [])]) and  # action.malware.vector: all
            any([k != "Unknown" for k in incident.get("action", {}).get("hacking", {}).get("variety", [])]) # action.malware.variety: all
        )
        #attribute_2
        rating['attribute_2'] = bool(
            'data_total' in incident.get('attribute', {}).get('confidentiality', {'data_total': 0}) and # attribute.confidentiality.data_total: all
            any([k['variety'] != "Unknown" for k in incident.get('attribute', {}).get('confidentiality', {}).get('data', [])]) and # attribute.confidentiality.data.variety: all
            len(incident.get("attribute", {}).get("integrity", {}).get("variety", [])) > 0 and # attribute.integrity.variety: all
            len(incident.get("attribute", {}).get("availability", {}).get("variety", [])) > 0 # attribute.availability.variety: all
        )
        #targeted_1
        rating['targeted_1'] = incident.get('targeted', "Unknown") != "Unknown" # targeted: all
        #action_2_nontech
        rating['action_2_nontech'] = bool(
            any([k != "Unknown" for k in incident.get("action", {}).get("error", {}).get("variety", [])]) and  # action.error.variety: all
            any([k != "Unknown" for k in incident.get("action", {}).get("physical", {}).get("vector", [])]) and  # action.physical.variety: all
            any([k != "Unknown" for k in incident.get("action", {}).get("environmental", {}).get("variety", [])]) # action.environmental.variety: all
        )
        #asset_3
        rating['asset_3'] = bool(
            any(['amount' in k for k in incident.get('asset', {}).get('assets', [])]) and # asset.assets.amount: all
            any([k != "Unknown" for k in incident.get('asset', {}).get('country', ["Unknown"])]) and # asset.country: all
            any([k != "Unknown" for k in incident.get('asset', {}).get('cloud', ["Unknown"])]) and # asset.cloud: all
            (
                any([k != "Unknown" for k in incident.get('asset', {}).get('management', ["Unknown"])]) or # asset.governance: all
                any([k != "Unknown" for k in incident.get('asset', {}).get('hosting', ["Unknown"])])!= "Unknown" or # asset.governance: all
                any([k != "Unknown" for k in incident.get('asset', {}).get('ownership', ["Unknown"])]) != "Unknown" # asset.governance: all
            )
        )
        #timeline_3
        rating['timeline_3'] = bool(
            any([k != "Unknown" for k in incident.get("timeline", {}).get("containment", {}).get("unit", [])]) and # timeline.containment.unit: all
            any([k != "Unknown" for k in incident.get("timeline", {}).get("exfiltration", {}).get("unit", [])]) and # timeline.exfiltration.unit: all
            'value' in incident.get("timeline", {}).get("compromise", {}) and # timeline.compromise.value: all
            'value' in incident.get("timeline", {}).get("exfiltration", {}) and # timeline.exfiltration.value: all
            'value' in incident.get("timeline", {}).get("discovery", {}) and # timeline.discovery.value: all

            'value' in incident.get("timeline", {}).get("containment", {}) # timeline.containment.value: all
        )
        #y2y
        rating['y2y'] = 'year' in incident.get('timeline', {}).get('incident', {}) # timeline.incident.year: all
        #action_3
        rating['action_3'] = bool(
            any([k != "Unknown" for k in incident.get("action", {}).get("physical", {}).get("vector", [])]) and  # action.physical.vector: all
            any([k != "Unknown" for k in incident.get("action", {}).get("error", {}).get("vector", [])]) # action.error.vector: all
        )
        #actor_3
        rating['actor_3'] = bool(
            (
                any([k != "Unknown" for k in incident.get('actor', {}).get('external', {}).get('country', ["Unknown"])]) or # actor.external.country: all
                any([k != "Unknown" for k in incident.get('actor', {}).get('internal', {}).get('country', ["Unknown"])]) or # actor.internal.country: all
                any([k != "Unknown" for k in incident.get('actor', {}).get('partner', {}).get('country', ["Unknown"])]) # actor.partner.country: all
            ) and (
                any([k != "Unknown" for k in incident.get('actor', {}).get('external', {}).get('variety', ["Unknown"])]) and # actor.external.variety: all
                any([k != "Unknown" for k in incident.get('actor', {}).get('internal', {}).get('variety', ["Unknown"])]) and # actor.internal.variety: all
                any([k != "Unknown" for k in incident.get('actor', {}).get('partner', {}).get('variety', ["Unknown"])]) # actor.partner.variety: all
            )
        )
        #attribute_3
        rating['attribute_3'] = bool(
            any([k != "Unknown" for k in incident.get('attribute', {}).get('confidentiality', {}).get('data_victim', ["Unknown"])]) and # attribute.confidentiality.data_victim: all
            any([k != "Unknown" for k in incident.get('attribute', {}).get('confidentiality', {}).get('state', ["Unknown"])]) and # attribute.confidentiality.state: all
            any([k != "Unknown" for k in incident.get('attribute', {}).get('availability', {}).get('duration', {}).get('unit', ["Unknown"])]) and # attribute.availability.duration.unit: all
            'value' in incident.get("attribute", {}).get("availability", {}).get("duration", {}) # attribute.availability.duration.value: all
        )
        #action_3_blended
        rating['action_3_blended'] = bool(
            any([k != "Unknown" for k in incident.get("action", {}).get("misuse", {}).get("vector", [])]) and  # action.misuse.vector: all
            any([k != "Unknown" for k in incident.get("action", {}).get("social", {}).get("vector", [])]) # action.social.vector: all
        )
        #action_3_technical
        rating['action_3_technical'] = any([k != "Unknown" for k in incident.get("action", {}).get("hacking", {}).get("vector", [])]) # action.hacking.vector: all
        #actor_4
        rating['action_4'] = bool(
            incident.get('actor', {}).get('partner', {}).get('industry', '') and # actor.partner.industry2: all & actor.partner.industry: all
                any([k != "Unknown" for k in incident.get('actor', {}).get('partner', {}).get('region', ["Unknown"])]) and # actor.partner.region: all
                any([k != "Unknown" for k in incident.get('actor', {}).get('external', {}).get('region', ["Unknown"])]) and # actor.external.region: all
                any([k != "Unknown" for k in incident.get('actor', {}).get('internal', {}).get('job_change', ["Unknown"])]) and # actor.internal.job_change: all
                incident.get('actor', {}).get('external', {}).get('name', '') # actor.external.name: all
        )
        #action_4
        rating['action_4'] = bool(
            incident.get('action', {}).get('hacking', {}).get('cve', '') and # action.hacking.cve: all
            any([k != "Unknown" for k in incident.get('action', {}).get('social', {}).get('target', ["Unknown"])]) and # action.social.target: all
            incident.get('action', {}).get('malware', {}).get('cve', '') and # action.malware.cve: all
            incident.get('action', {}).get('malware', {}).get('name', '') # action.malware.name: all
        )
        #victim_3
        rating['victim_3'] = bool(
            'locations_affected' in incident.get('victim', {}) and # victim.locations_affected: all
            incident.get('region', {}).get('state', '') and # victim.state: all
            'amount' in incident.get('victim', {}).get('revenue', {}) and # victim.revenue.amount: all
            'iso_currency_code' in incident.get('victim', {}).get('revenue', {}) and # victim.revenue.iso_currency_code: all
            'amount' in incident.get('victim', {}).get('secondary', {}) # victim.secondary.amount: all
        )
        #impact_1
        rating['impact_1'] = bool(
            incident.get('impact', {}).get('overall_rating', 'Unknown') != "Unknown" and # impact.overall_rating: all
            any([k['rating'] != "Unknown" for k in incident.get('impact', {}).get('loss', [])]) and # impact.loss.rating: all
            any([k['variety'] != "Unknown" for k in incident.get('impact', {}).get('loss', [])]) # impact.loss.variety: all
        )
        #incident_2
        rating['impact_2'] = bool(
            incident.get('notes', '') and # notes: all
            incident.get('discovery_notes', '') and # discovery_notes: all
            incident.get('campaign_id', '') and # campaign_id: all
            incident.get('reference', '') and # reference: all
            incident.get('summary', '') # summary: all
        )
        #a4_2
        rating['a4_2'] = bool(
            incident.get('attribute', {}).get('unknown', {}).get('notes', '') and # attribute.unknown.notes: all
            incident.get('action', {}).get('unknown', {}).get('notes', '') and # action.unknown.notes: all
            incident.get('actor', {}).get('unknown', {}).get('notes', '') and # actor.unknown.notes: all
            incident.get('asset', {}).get('notes', '') # asset.notes: all
        )
        #impact_2
        rating['impact_2'] = bool(
            any([k.get('max_amount', 'Unknown') != "Unknown" for k in incident.get('impact', {}).get('loss', [])]) and # impact.loss.max_amount: all
            any([k.get('min_amount', 'Unknown') != "Unknown" for k in incident.get('impact', {}).get('loss', [])]) and # impact.loss.min_amount: all
            any([k.get('amount', 'Unknown') != "Unknown" for k in incident.get('impact', {}).get('loss', [])]) and # impact.loss.amount: all
            incident.get('impact', {}).get('iso_currency_code', 'Unknown') != "Unknown" # impact.iso_currency_code: all
        )
        #actor_5
        rating['actor_5'] = bool(
            incident.get('actor', {}).get('internal', {}).get('notes', '') and # actor.internal.notes: all
            incident.get('actor', {}).get('external', {}).get('notes', '') and # actor.external.notes: all
            incident.get('actor', {}).get('partner', {}).get('notes', '') # actor.partner.notes: all
        )
        #incident_3
        rating['incident_3'] = bool(
            incident.get('victim', {}).get('notes', '') and # victim.notes: all
            incident.get('victim', {}).get('secondary', {}).get('notes', '') and # victim.secondary.notes: all
            incident.get('impact', {}).get('notes', '') # impact.notes: all
        )
        #action_5
        rating['action_5'] = bool(
            incident.get('action', {}).get('error', {}).get('notes', '') and # action.error.notes: all
            incident.get('action', {}).get('physical', {}).get('notes', '') and # action.physical.notes: all
            incident.get('action', {}).get('malware', {}).get('notes', '') and # action.malware.notes: all
            incident.get('action', {}).get('social', {}).get('notes', '') and # action.social.notes: all
            incident.get('action', {}).get('environmental', {}).get('notes', '') and # action.environmental.notes: all
            incident.get('action', {}).get('hacking', {}).get('notes', '') and # action.hacking.notes: all
            incident.get('action', {}).get('misuse', {}).get('notes', '') # action.misuse.notes: all
        )
        #controls_1
        rating['controls_1'] = bool(
            incident.get('corrective_action', '') and # corrective_action: all
            incident.get('cost_corrective_action', 'Unknown') != "Unknown" and # cost_corrective_action: all
            incident.get('control_failure', '') # control_failure: all
        )
        #attribute_4
        rating['attribute_4'] = bool(
            incident.get('attribute', {}).get('confidentiality', {}).get('notes', '') and # attribute.confidentiality.notes: all
            incident.get('attribute', {}).get('integrity', {}).get('notes', '') and # attribute.integrity.notes: all
            incident.get('attribute', {}).get('availability', {}).get('notes', '') # attribute.availability.notes: all
        )

        return rating


if __name__ == "__main__":

    ## Gabe
    ## The general Apprach to config parsing (Probably not the best way)
    ## 1. create a dictionary called 'cfg' of fallback values (up at the top of the file)
    ## 2. parse the arguments (args) and turn into a dictionary if the value is not None
    ## 3. Use the config from the command line parser to read the config file and update the 'cfg' dictionary
    ## 4. Update the cfg dictionary with the arguements (args) from the command line

    parser = argparse.ArgumentParser(description="This script takes a directory of VERIS json and scores it's maturity according to the veris maturity model. ")
    parser.add_argument("-i", "--input", required=True, help="The json file or directory")
    #parser.add_argument("-o", "--output", help="directory where json files will be written")
    #parser.add_argument("--veris", required=False, help="The location of the veris_scripts repository.")
    #parser.add_argument("-l","--log_level",choices=["critical","warning","info","debug"], help="Minimum logging level to display")
    #parser.add_argument('--log_file', help='Location of log file')
    #parser.add_argument("--dbir-private", required=False, help="The location of the dbirR repository.")
    #parser.add_argument("-s","--schemafile", help="The JSON schema file")
    #parser.add_argument("-e","--enumfile", help="The JSON file with VERIS enumerations")
    #parser.add_argument("--vcdb",help="Convert the data for use in VCDB",action="store_true")
    #parser.add_argument("--version", help="The version of veris in use")
    #parser.add_argument('--conf', help='The location of the config file', default="./_checkValidity.cfg")
    #parser.add_argument('--year', help='The DBIR year to assign tot he records.')
    #parser.add_argument('--countryfile', help='The json file holdering the country mapping.')
    # parser.add_argument('--source', help="Source_id to use for the incidents. Partner pseudonym.")
    #parser.add_argument("-f", "--force_analyst", help="Override default analyst with --analyst.", action='store_true')
    args = parser.parse_args()
    args = {k:v for k,v in vars(args).items() if v is not None}

    # Parse the config file
    try:
        config = configparser.ConfigParser()
        config.readfp(open(args["conf"]))
        cfg_key = {
            'GENERAL': ['input', 'output'], #'report', 'analysis', 'year', 'force_analyst', 'version', 'database', 'check'],
            'LOGGING': ['log_level', 'log_file'] #,
            # 'REPO': ['veris', 'dbir_private'],
            # 'VERIS': ['mergedfile', 'enumfile', 'schemafile', 'labelsfile', 'countryfile']
        }
        for section in cfg_key.keys():
            if config.has_section(section):
                for value in cfg_key[section]:
                    if value.lower() in config.options(section):
                        cfg[value] = config.get(section, value)
#        if "year" in cfg:
#            cfg["year"] = int(cfg["year"])
#        else:
#            cfg["year"] = int(datetime.now().year)
#        cfg["vcdb"] = {True:True, False:False, "false":False, "true":True}[cfg["vcdb"].lower()]
        logging.debug("config import succeeded.")
    except Exception as e:
        logging.warning("config import failed with error {0}.".format(e))
        #raise e
        pass

    cfg.update(args)
    veris_logger.updateLogger(cfg)

    logging.debug(args)

    logging.debug(cfg)

#    main(cfg)
# def main(cfg):
#    if __name__ != "__main__":
#        raise RuntimeError("Main should not be imported and run.  Instead run ''makeValid()' and 'addRules()'")

    logging.info('Beginning main loop.')
    formatter = ("- " + "/".join(cfg["input"].split("/")[-2:]))
    # Updating the format of the logging
    veris_logger.updateLogger(cfg, formatter)
    # get all files in directory and sub-directories
    if os.path.isfile(cfg['input']):
        filenames = [cfg['input']]
    elif os.path.isdir(cfg['input']):
        # http://stackoverflow.com/questions/14798220/how-can-i-search-sub-folders-using-glob-glob-module-in-python
        filenames = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(cfg['input'])
            for f in files if f.endswith(".json")]
    else:
        raise OSError("File or directory {0} does not exist.".format(cfg['input']))

    verismm = VERISmm(cfg)
    ratings = {}

    # open each json file
    # if 'output' in cfg and cfg['output'] is not None:
    #     overwrite = False
    # else:
    #    overwrite = True
    for filename in tqdm(filenames):
        with open(filename, 'r+') as filehandle:
            try:
                incident = json.load(filehandle)
            except:
                logging.warning("Unable to load {0}.".format(filename))
                continue
            logging.debug("Before parsing:\n" + pformat(incident))
            ratings[filename] = verismm.rate_one(incident)

            logging.debug("After parsing:\n" + pformat(incident))

    agg_ratings = verismm.aggregate_ratings(ratings)
    pprint(verismm.maturity(agg_ratings))
    pprint(verismm.maturity_detail(agg_ratings))

    logging.info('Ending main loop.')