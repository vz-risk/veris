# Schema Update

1. Append version number to merged json schema and copy to assets/schema
2. Copy labels json over to assets/schema
3. In src/js/dbir-common.js

    - add imports for new schema.
    - change default version number
    - add section to schemas constant for new version

4. Add section for new version in src/js/veris_app.uiSchemas.js under each schema type. Remove any removed enumerations from ui:order, etc within each section for the version.  Add any new enumerations that may have been added so that they can be properly ordered and collapsable.

5. In assets/schema/veris_app_groom.json ensure the version number is included any any lists of moved items or the uiParsing will be inconsistant.

(Note: Steps 4 and 5 may take several iterations to get correct.  Try all combinations of schema/version in the webapp. Make sure to expand collapsed sections.)

6. Run `npm run build:full` to minify the webapp and place it in the right spot. (you may have to run `npm install webpack`)