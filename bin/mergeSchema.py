# Produces a schema file which is the combination of
# of a schema, an enumeration, and a plus section

import json
import jsonschema

defaultSchema = "../verisc.json"
defaultEnum = "../verisc-enum.json"


def buildSchema(schema, enum, plus):
    # All of the action enumerations
    for each in ['hacking', 'malware', 'social', 'error',
                 'misuse', 'physical']:
        schema['properties']['action']['properties'][each]['properties']['variety']['items']['enum'] = \
            enum['action'][each]['variety']
        schema['properties']['action']['properties'][each]['properties']['vector']['items']['enum'] = \
            enum['action'][each]['vector']
    schema['properties']['action']['properties']['environmental']['properties']['variety']['items']['enum'] = \
        enum['action']['environmental']['variety']
    schema['properties']['action']['properties']['social']['properties']['target']['items']['enum'] = \
        enum['action']['social']['target']

    # actor enumerations
    for each in ['external', 'internal', 'partner']:
        schema['properties']['actor']['properties'][each]['properties']['motive']['items']['enum'] = enum['actor'][
            'motive']
    schema['properties']['actor']['properties']['external']['properties']['variety']['items']['enum'] = \
        enum['actor']['external']['variety']
    schema['properties']['actor']['properties']['internal']['properties']['variety']['items']['enum'] = \
        enum['actor']['internal']['variety']
    schema['properties']['actor']['properties']['internal']['properties']['job_change']['items']['enum'] = \
        enum['actor']['internal']['job_change']
    schema['properties']['actor']['properties']['external']['properties']['country']['items']['enum'] = enum['country']
    schema['properties']['actor']['properties']['partner']['properties']['country']['items']['enum'] = enum['country']

    # asset properties
    schema['properties']['asset']['properties']['assets']['items']['properties']['variety']['enum'] = \
        enum['asset']['variety']
    schema['properties']['asset']['properties']['governance']['items']['enum'] = \
        enum['asset']['governance']

    # attribute properties
    schema['properties']['attribute']['properties']['availability']['properties']['variety']['items']['enum'] = \
        enum['attribute']['availability']['variety']
    schema['properties']['attribute']['properties']['availability']['properties']['duration']['properties']['unit'][
        'enum'] = enum['timeline']['unit']
    schema['properties']['attribute']['properties']['confidentiality']['properties']['data']['items']['properties'][
        'variety']['enum'] = enum['attribute']['confidentiality']['data']['variety']
    schema['properties']['attribute']['properties']['confidentiality']['properties']['data_disclosure'][
        'enum'] = enum['attribute']['confidentiality']['data_disclosure']
    schema['properties']['attribute']['properties']['confidentiality']['properties']['state']['items']['enum'] = \
        enum['attribute']['confidentiality']['state']
    schema['properties']['attribute']['properties']['integrity']['properties']['variety']['items']['enum'] = \
        enum['attribute']['integrity']['variety']

    # impact
    schema['properties']['impact']['properties']['iso_currency_code']['enum'] = enum['iso_currency_code']
    schema['properties']['impact']['properties']['loss']['items']['properties']['variety']['enum'] = \
        enum['impact']['loss']['variety']
    schema['properties']['impact']['properties']['loss']['items']['properties']['rating']['enum'] = \
        enum['impact']['loss']['rating']
    schema['properties']['impact']['properties']['overall_rating']['enum'] = \
        enum['impact']['overall_rating']

    # timeline
    for each in ['compromise', 'containment', 'discovery', 'exfiltration']:
        schema['properties']['timeline']['properties'][each]['properties']['unit']['enum'] = \
            enum['timeline']['unit']

    # victim
    schema['properties']['victim']['properties']['country']['items']['enum'] = enum['country']
    schema['properties']['victim']['properties']['employee_count']['enum'] = \
        enum['victim']['employee_count']
    schema['properties']['victim']['properties']['revenue']['properties']['iso_currency_code']['enum'] = \
        enum['iso_currency_code']

    # Randoms
    for each in ['confidence', 'cost_corrective_action', 'discovery_method', 'security_incident', 'targeted']:
        schema['properties'][each]['enum'] = enum[each]

    # Plus section
    schema['properties']['plus'] = plus

    return schema  # end of buildSchema()

if __name__ == '__main__':
  schema = json.loads(open(defaultSchema).read())
  enum = json.loads(open(defaultEnum).read())
  merged = buildSchema(schema, enum, {})
  outfile = open('../verisc-merged.json', 'w')
  outfile.write(json.dumps(merged, sort_keys=True, indent=2))
  outfile.close()
