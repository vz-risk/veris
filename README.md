# *NOTE TO VERIS USERS*
We have updated VERIS to version 1.3.2.  This is primarily an update to add//modify a few enumerations, however it involves a significant change in the associated import scripts.  From here we plan to update to version 1.4 which will fix schema hierarchy issues that may affect tooling.  The primary example is making discovery_method and asset hierarchical like actor, action, and attribute.  Version 2.0 will be for major feature additions.  The primary one being considered is adding sequencing of the 4A's, timeline, and discovery method so that the sequence things happened in in the incident can be captured.

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
* convert_1.3.X_to_1.3.Y.py - convert veris 1.3.X json records to 1.3.Y
* import_stdexcel.py - script (usable as module) to convert VERIS_Standard_Excel.xlsx Reviewed data to a csv to json.
* import_veris.py - script (usable as module) to import a csv to json.  Chooses the correct import module, uses the rules module, and uses the checkValidity module.
* mergeSchema.py - Merges the schema file (e.g. verisc.json) and labels file (e.g. verisc-labels.json) to form the merged schema file (schema-merged.json)
* rules.py - script (usable as a module) to make json files valid (by adding 'unknown's) and to add rules (e.g. add asset.assets.web app if hacking.vector.web app is present)
* update_labels.py - script to update an existing labels file with a diff file.
* update_schema.py - script to update an existing schema file with a diff file.
* VERIS_Standard_Excel.xlsx - standard excel file used to produce importable data.
* vacf-rev20XX-vY_Y_Y.csv - VERIS <-> Mitre ATT&CK mapping structured as graph edges
* cis_csc_veris_map-rev20XX-vY_Y.xlsx - VERIS <-> CIS CSC mapping for both VERIS patterns and actions.
* joined_veris_json.md - Explain the joined VERIS format.

# Required packages
The following packages are required to run the associated tools
## Python
ipdb
simplejson

# Joined JSON
As the amount of VERIS json grows, it becomes unwieldly.  As such, the VERIS toolchain is being updated to allow a joined form of VERIS.  Please read more in the joined_veris_json.md file.

# VERIS Common Attack Framework  
The VERIS Common Attack Framework, (or VCAF)  serves as a bridge to ATT&CK, covering the portions of VERIS not in ATT&CK with the aim of creating a holistic framework. At its very core, VCAF is made of two components: one is the conceptual mapping between VERIS and ATT&CK, and another is the extension of ATT&CK with techniques that cover all possible Threat Actions present in VERIS. This is helpful in using ATT&CK to make strategic decisions and understanding what tactical actions to take to address a strategic challenge.  The mapping can be found as an edge list (or a join table for the more SQL minded) in `bin/vcaf-rev2020-v1_0_3.csv` in this repository.

# Center for Internet Security (CIS) Critical Security Controls (CSCs) to VERIS Mapping  
This mapping provides both pattern and control mappings for the Internet Security (CIS) Critical Security Controls (CSCs) to VERIS.  This is helpful in using VERIS to make consistent control decisions.  The mapping can be found in `bin/cis_csc_veris_map-rev2020-v1_0.xlsx` in this repository.