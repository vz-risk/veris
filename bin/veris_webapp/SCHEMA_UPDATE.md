# Schema Update

1. Append version number to merged json schema and copy to assets/schema
2. Copy labels json over to assets/schema
3. In src/js/dbir-common.js

    - add imports for new schema.
    - change default version number
    - add section to schemas constant for new version

4. Add section for new version in src/js/veris_app.uiSchemas.js 

5. Run `npm run build:dist` to minify the webapp and place it in the right spot.