# Running validation tests
Unit tests are written in nose, so you'll need to `pip install nose`. Then from the root of the repository, run `nosetests`. Python will automatically run 
the tests in the tests folder. If you want detailed output you can run `nosetests --nocapture`.

## Writing unit tests
Each unit test is a VERIS json object wrapped inside another object. Each test object has three keys, "incident" should be a VERIS json object; "should" indicates whether the incident should pass or fail validation; "message is a string that explains why the incident should or should not pass validation."
#---
http://veriscommunity.net

# JSON Notes
Learn more about the JSON schema definition at http://json-schema.org/.  We also are not enforcing the enumerations at the schema level, but instead have a separate file with the enumerations.  Those may update a bit more often then the schema itself.

# XML notes
The XML version has been archived until we can sync the XML with the JSON schema.  The JSON schema represents the latest version of VERIS.

# Index

* verisc.json - the JSON schema definition, compliant with the propoosed JSON standard
* verisc-enum.json - definition of the allowable enumerations within VERIS
