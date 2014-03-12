import simplejson
import nose
import os
from jsonschema import validate, ValidationError

schema = simplejson.loads(open('verisc.json').read())

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
      print "Validation failed and it should have. %s" % inDict['message']
      pass

def test_Schema():
  for eachTestFile in os.listdir('./tests'):
    if eachTestFile.endswith('.json'):
      test = simplejson.loads(open('./tests/'+eachTestFile).read())
      yield runTest, test
