# Joined JSON

As the number of JSON records increases, it becomes unwieldly to regularly read them off of disk.  At 750,000+ in the DBIR, in some cases this incurs significant performance penalties.  To help make it less wieldly, we are updating the tooling to support a second file format.

The traditional file format (a single json string incident in a single json file) will continue to be supported.  Additionally, a single json string per file within a zip archive will also be supported.  However, importing these are slow in verisr::json2veris() with anything over 5,000 incident files in the zip file becoming unwieldly.

As such, json files within zip files will be checked to see if they begin with an array (a first character after white space of "[").  If it does, the file will be assumed to be an array of VERIS incidents and parsed accordingly.  **This currently _only_ applies in JSON within zipped files.**  These files can currently be created using the `/bin/vcdb_to_joined.py` script within the `https://github.com/vz-risk/vcdb` repository, however the functionality will likely be moved to the veris repository as we progress.

Scripts supporting the joined JSON format:
* verisr/json2veris() - YES as of 2.3.2007
* checkValidity.py - Planned
* convert_1.3.3_to_1.3.4.py - Planned
* other conversion scripts - Not planned
* import_stdexcel1_3_4.py - Yes
* other import_stdexcel scripts - Not planned
* import_veris.py - Not planned, no longer used
* into-mongo.py - Not planned
* json2csv.py - Not planned. Import into R and export csv
* mergeSchema.py - Not necessary
* repeat_veris.py - Not planned
* rules.py - Planned
* update_labels.py - Not necessary
* update_schema.py - Not necessary
* veris_logger.py - Not necessary
* verismm.py - Not necessary