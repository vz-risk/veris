import simplejson
import nose
import os
from jsonschema import validate, ValidationError

schema = simplejson.loads(open('verisc.json').read())
enum = simplejson.loads(open('verisc-enum.json').read())

# All of the action enumerations
for each in ['hacking','malware','social','error','misuse','physical']:
    schema['properties']['action']['properties'][each]['properties']['variety']['items']['enum'] = enum['action'][each]['variety']
    schema['properties']['action']['properties'][each]['properties']['vector']['items']['enum'] = enum['action'][each]['vector']
schema['properties']['action']['properties']['environmental']['properties']['variety']['items']['enum'] = enum['action']['environmental']['variety']
schema['properties']['action']['properties']['physical']['properties']['location']['items']['enum'] = enum['action']['physical']['location']
schema['properties']['action']['properties']['social']['properties']['target']['items']['enum'] = enum['action']['social']['target']

# actor enumerations
for each in ['external','internal','partner']:
    schema['properties']['actor']['properties'][each]['properties']['motive']['items']['enum'] = enum['actor']['motive']
schema['properties']['actor']['properties']['external']['properties']['variety']['items']['enum'] = enum['actor']['external']['variety']
schema['properties']['actor']['properties']['internal']['properties']['variety']['items']['enum'] = enum['actor']['internal']['variety']
schema['properties']['actor']['properties']['external']['properties']['country']['items']['enum'] = enum['country']
schema['properties']['actor']['properties']['partner']['properties']['country']['items']['enum'] = enum['country']

# asset properties
schema['properties']['asset']['properties']['assets']['items']['properties']['variety']['pattern'] = '|'.join(enum['asset']['variety'])
for each in ['accessibility','cloud','hosting','management','ownership']:
    schema['properties']['asset']['properties'][each]['pattern'] = '|'.join(enum['asset'][each])

# attribute properties
schema['properties']['attribute']['properties']['availability']['properties']['variety']['items']['enum'] = enum['attribute']['availability']['variety']
schema['properties']['attribute']['properties']['availability']['properties']['duration']['properties']['unit']['pattern'] = '|'.join(enum['timeline']['unit'])
schema['properties']['attribute']['properties']['confidentiality']['properties']['data']['items']['properties']['variety']['pattern'] = '|'.join(enum['attribute']['confidentiality']['data']['variety'])
schema['properties']['attribute']['properties']['confidentiality']['properties']['data_disclosure']['pattern'] = '|'.join(enum['attribute']['confidentiality']['data_disclosure'])
schema['properties']['attribute']['properties']['confidentiality']['properties']['state']['items']['enum'] = enum['attribute']['confidentiality']['state']
schema['properties']['attribute']['properties']['integrity']['properties']['variety']['items']['enum'] = enum['attribute']['integrity']['variety']

# impact
schema['properties']['impact']['properties']['iso_currency_code']['patter'] = '|'.join(enum['iso_currency_code'])
schema['properties']['impact']['properties']['loss']['items']['properties']['variety']['pattern'] = '|'.join(enum['impact']['loss']['variety'])
schema['properties']['impact']['properties']['loss']['items']['properties']['rating']['pattern'] = '|'.join(enum['impact']['loss']['rating'])
schema['properties']['impact']['properties']['overall_rating']['patter'] = '|'.join(enum['impact']['overall_rating'])

# timeline
for each in ['compromise','containment','discovery','exfiltration']:
    schema['properties']['timeline']['properties'][each]['properties']['unit']['pattern'] = '|'.join(enum['timeline']['unit'])
    
# victim
schema['properties']['victim']['properties']['country']['pattern'] = '|'.join(enum['country'])
schema['properties']['victim']['properties']['employee_count']['pattern'] = '|'.join(enum['victim']['employee_count'])
schema['properties']['victim']['properties']['revenue']['properties']['iso_currency_code']['pattern'] = '|'.join(enum['iso_currency_code'])

# Randoms
for each in ['confidence','cost_corrective_action','discovery_method','security_incident','targeted']:
    schema['properties'][each]['pattern'] = '|'.join(enum[each])

def runTest(inDict):
  try:
    validate(inDict['incident'],schema)
    if inDict['should'] == "pass":
      print "Validation passed properly. %s" % inDict['message']
      pass
    else:
      # Validation passed but it should have failed. Explain.
      print "validation passed but it should have failed. %s" % inDict['message']
      assert False
  except ValidationError as e:
    if inDict['should'] == "pass":
      # Validation failed but it should have passed. Explain yourself
      offendingPath = '.'.join(str(x) for x in e.path)
      print "Validation failed but should have passed %s" % inDict['message']
      print "\t %s %s" % (offendingPath,e.message)
      assert False
    else:
      print "Validation failed and it should have. %s %s" % (inDict['message'],e.message)
      pass

def test_Schema():
  for eachTestFile in os.listdir('./tests'):
    if eachTestFile.endswith('.json'):
      test = simplejson.loads(open('./tests/'+eachTestFile).read())
      yield runTest, test
