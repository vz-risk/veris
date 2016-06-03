# *NOTE TO VERIS USERS*
We are currently planning changes to veris.  Version 1.3.1 will add enumerations, update enumerations, and add descriptions.  The goal is to minimize the impacts on tooling.  Version 1.4 will fix schema issues that may affect tooling.  The primary example is making discovery_method and asset hierarchical like actor, action, and attribute.  Version 2.0 will be for major feature additions.  The primary one being considered is adding sequencing of the 4A's, timeline, and discovery method so that the sequence things happened in in the incident can be captured.

If you are using veris, *please* contact us at dbir [at] verizon.com to let us know hoe you use it and with what tools.  If you have suggestions on changes we can/should make, please contact us or add an issue to the repository.  We want to make sure the changes we make have minimal impact on all users and allow for easy upgrade at the user's convenience.  To that end, we have saved a v1.3 release for those who chose not to upgrade as well as a v1.3 branch.

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
