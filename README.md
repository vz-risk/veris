# *NOTE TO VERIS USERS*
We have updated VERIS to version 1.3.1.  This is primarily an update to add//modify a few enumerations, however it involves a significant change in the associated import scripts.  From here we plan to update to version 1.4 which will fix schema hierarchy issues that may affect tooling.  The primary example is making discovery_method and asset hierarchical like actor, action, and attribute.  Version 2.0 will be for major feature additions.  The primary one being considered is adding sequencing of the 4A's, timeline, and discovery method so that the sequence things happened in in the incident can be captured.

If you are using veris, *please* contact us at dbir [at] verizon.com to let us know how you use it and with what tools.  If you have suggestions on changes we can/should make, please contact us or add an issue to the repository.  We want to make sure the changes we make have minimal impact on all users and allow for easy upgrade at the user's convenience.  To that end, we have saved a v1.3 release for those who chose not to upgrade as well as a v1.3 branch.

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

* verisc.json - the JSON schema definition, compliant with the propoosed JSON standard. Merged with versc-labels.json to produce verisc-enum.json, verisc-merged.json, and keynames-real.txt
* verisc-labels.json - A list of enumerations with descriptions. Merged with versc.json to produce verisc-enum.json, verisc-merged.json, and keynames-real.txt
* verisc-enum.json - definition of the allowable enumerations within VERIS
* verisc-merged.json - The complete schema used for converting reviewed CSVs to json.
* bin/all.json - a json file of country codes used for converting CSVs to json.
* bin/build_standard_excel.py - script to read a merged schema file and produce the VERIS_Standard_Excel.xlsx file
* checkValidity.py - script (usable as module) to validate a json record against a schema file as well as aditional rules.
* convert-1.3.py - convert veris 1.2 json records to 1.3
* convert_1.3_to_1.3.1.py - convert veris 1.3 json records to 1.3.1
* import_stdexcel.py - script (usable as module) to convert VERIS_Standard_Excel.xlsx Reviewed data to a csv to json.
* import_veris.py - script (usable as module) to import a csv to json.  Chooses the correct import module, uses the rules module, and uses the checkValidity module.
* mergeSchema.py - Merges the schema file (e.g. verisc.json) and labels file (e.g. verisc-labels.json) to form the merged schema file (schema-merged.json)
* rules.py - script (usable as a module) to make json files valid (by adding 'unknown's) and to add rules (e.g. add asset.assets.web app if hacking.vector.web app is present)
* update_labels.py - script to update an existing labels file with a diff file.
* update_schema.py - script to update an existing schema file with a diff file.
* VERIS_Standard_Excel.xlsx - standard excel file used to produce importable data.

# Required packages
The following packages are required to run the associated tools
## Python
ipdb
simplejson
