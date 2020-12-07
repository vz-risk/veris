import React from 'react'

import veriscLabels from '../../assets/schema/verisc-labels.json'
import vcdbLabels from '../../assets/schema/vcdb-labels.json'
import dbirLabels from '../../assets/schema/dbir-labels.json'
import groomSchemaDef from '../../assets/schema/veris_app_groom.json'

import verisHelp from './help.js' //  '../../assets/schema/help.json'

import verisc1_3_1 from '../../assets/schema/verisc-merged1_3_1.json'
import verisc1_3_2 from '../../assets/schema/verisc-merged1_3_2.json'
import verisc1_3_3 from '../../assets/schema/verisc-merged1_3_3.json'
import verisc1_3_4 from '../../assets/schema/verisc-merged1_3_4.json'
import verisc1_3_5 from '../../assets/schema/verisc-merged1_3_5.json'
import verisc2 from '../../assets/schema/verisc-merged2.json'
import vcdb1_3_1 from '../../assets/schema/vcdb-merged1_3_1.json'
import vcdb1_3_2 from '../../assets/schema/vcdb-merged1_3_2.json'
import vcdb1_3_3 from '../../assets/schema/vcdb-merged1_3_3.json'
import vcdb1_3_4 from '../../assets/schema/vcdb-merged1_3_4.json'
import vcdb1_3_5 from '../../assets/schema/vcdb-merged1_3_5.json'
import dbir1_3_1 from '../../assets/schema/dbir-merged1_3_1.json'
import dbir1_3_2 from '../../assets/schema/dbir-merged1_3_2.json'
import dbir1_3_3 from '../../assets/schema/dbir-merged1_3_3.json'
import dbir1_3_4 from '../../assets/schema/dbir-merged1_3_4.json'
import dbir1_3_5 from '../../assets/schema/dbir-merged1_3_5.json'

import uiSchemas from './veris_app.uiSchemas'

export const defaultSchemaName = 'partner';
export const defaultSchemaVersion = '1.3.5';

const schemas = {
    partner: {
      name: 'Partner',
      versions: {
        '1.3.1': {
          schema: processSchema(dbir1_3_1, 'partner', '1.3.1', dbirLabels),
          rawschema: dbir1_3_1,
          uischema: uiSchemas['partner']['1.3.1']
        },
        '1.3.2': {
          schema: processSchema(dbir1_3_2, 'partner', '1.3.2', dbirLabels),
          rawschema: dbir1_3_2,
          uischema: uiSchemas['partner']['1.3.2']
        },
        '1.3.3': {
          schema: processSchema(dbir1_3_3, 'partner', '1.3.3', dbirLabels),
          rawschema: dbir1_3_3,
          uischema: uiSchemas['partner']['1.3.3']
        },
        '1.3.4': {
          schema: processSchema(dbir1_3_4, 'partner', '1.3.4', dbirLabels),
          rawschema: dbir1_3_4,
          uischema: uiSchemas['partner']['1.3.4']
        },
        '1.3.5': {
          schema: processSchema(dbir1_3_5, 'partner', '1.3.5', dbirLabels),
          rawschema: dbir1_3_5,
          uischema: uiSchemas['partner']['1.3.5']
        },
        // '1.4': {
        //   schema: undefined,
        //   rawschema: undefined,
        //   uischema: add_help(uiSchemas['partner']['1.4'])
        // },
        '2.0': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['partner']['2.0']
        }
      },
      allowOther: false
    },
    verisc: {
      name: 'VERISC',
      versions: {
        '1.3.1': {
          schema: processSchema(verisc1_3_1, 'verisc', '1.3.1', veriscLabels),
          rawschema: verisc1_3_1,
          uischema: uiSchemas['verisc']['1.3.1']
        },
        '1.3.2': {
          schema: processSchema(verisc1_3_2, 'verisc', '1.3.2', veriscLabels),
          rawschema: verisc1_3_2,
          uischema: uiSchemas['verisc']['1.3.2']
        },
        '1.3.3': {
          schema: processSchema(verisc1_3_3, 'verisc', '1.3.3', veriscLabels),
          rawschema: verisc1_3_3,
          uischema: uiSchemas['verisc']['1.3.3']
        },
        '1.3.4': {
          schema: processSchema(verisc1_3_4, 'verisc', '1.3.4', veriscLabels),
          rawschema: verisc1_3_4,
          uischema: uiSchemas['verisc']['1.3.4']
        },
        '1.3.5': {
          schema: processSchema(verisc1_3_5, 'verisc', '1.3.5', veriscLabels),
          rawschema: verisc1_3_5,
          uischema: uiSchemas['verisc']['1.3.5']
        },
        // '1.4': {
        //   schema: processSchema(verisc1_4, 'verisc', '1.4', veriscLabels),
        //   rawschema: verisc1_4,
        //   uischema: add_help(uiSchemas['verisc']['1.4'])
        // },
        '2.0': {
          rawschema: verisc2,
          schema: processSchema(verisc2, 'verisc', '2.0', veriscLabels),
          uischema: uiSchemas['verisc']['2.0']
        }
      },
      allowOther: false
    }, 
    dbir: {
      name: 'DBIR',
      versions: {
        '1.3.1': {
          schema: processSchema(dbir1_3_1, 'dbir', '1.3.1', dbirLabels),
          rawschema: dbir1_3_1,
          uischema: uiSchemas['dbir']['1.3.1']
        },
        '1.3.2': {
          schema: processSchema(dbir1_3_2, 'dbir', '1.3.2', dbirLabels),
          rawschema: dbir1_3_2,
          uischema: uiSchemas['dbir']['1.3.2']
        },
        '1.3.3': {
          schema: processSchema(dbir1_3_3, 'dbir', '1.3.3', dbirLabels),
          rawschema: dbir1_3_3,
          uischema: uiSchemas['dbir']['1.3.3']
        },
        '1.3.4': {
          schema: processSchema(dbir1_3_4, 'dbir', '1.3.4', dbirLabels),
          rawschema: dbir1_3_4,
          uischema: uiSchemas['dbir']['1.3.4']
        },
        '1.3.5': {
          schema: processSchema(dbir1_3_5, 'dbir', '1.3.5', dbirLabels),
          rawschema: dbir1_3_5,
          uischema: uiSchemas['dbir']['1.3.5']
        },
        // '1.4': {
        //   schema: undefined,
        //   rawschema: undefined,
        //   uischema: add_help(uiSchemas['dbir']['1.4'])
        // },
        '2.0': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['dbir']['2.0']
        }
      },
      allowOther: false
    },
    vzir: {
      name: 'VZIR (Other)',
      versions: {
        '1.3.1': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['vzir']['1.3.1']
        },
        '1.3.2': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['vzir']['1.3.2']
        },
        '1.3.3': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['vzir']['1.3.3']
        },
        '1.3.4': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['vzir']['1.3.4']
        },
        '1.3.5': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['vzir']['1.3.5']
        },
        // '1.4': {
        //   schema: undefined,
        //   rawschema: undefined,
        //   uischema: add_help(uiSchemas['vzir']['1.4'])
        // },
        '2.0': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['vzir']['2.0']
        }
      },
      allowOther: true
    },
    vcdb: {
      name: 'VCDB',
      versions: {
        '1.3.1': {
          schema: processSchema(vcdb1_3_1, 'vcdb', '1.3.1', vcdbLabels),
          rawschema: vcdb1_3_1,
          uischema: uiSchemas['vcdb']['1.3.1']
        },
        '1.3.2': {
          schema: processSchema(vcdb1_3_2, 'vcdb', '1.3.2', vcdbLabels),
          rawschema: vcdb1_3_2,
          uischema: uiSchemas['vcdb']['1.3.2']
        },
        '1.3.3': {
          schema: processSchema(vcdb1_3_3, 'vcdb', '1.3.3', vcdbLabels),
          rawschema: vcdb1_3_3,
          uischema: uiSchemas['vcdb']['1.3.3']
        },
        '1.3.4': {
          schema: processSchema(vcdb1_3_4, 'vcdb', '1.3.4', vcdbLabels),
          rawschema: vcdb1_3_4,
          uischema: uiSchemas['vcdb']['1.3.4']
        },
        '1.3.5': {
          schema: processSchema(vcdb1_3_5, 'vcdb', '1.3.5', vcdbLabels),
          rawschema: vcdb1_3_5,
          uischema: uiSchemas['vcdb']['1.3.5']
        }
      },
      allowOther: false
    },
    other: {
      name: 'Other',
      versions: {
        '1.3.1': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['other']['1.3.1']
        },
        '1.3.2': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['other']['1.3.2']
        },
        '1.3.3': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['other']['1.3.3']
        },
        '1.3.4': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['other']['1.3.4']
        },
        '1.3.5': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['other']['1.3.5']
        },
        // '1.4': {
        //   schema: undefined,
        //   rawschema: undefined,
        //   uischema: add_help(uiSchemas['other']['1.4'])
        // },
        '2.0': {
          schema: undefined,
          rawschema: undefined,
          uischema: uiSchemas['other']['2.0']
        }
      },
      allowOther: true
    }
  };

function deepCopy(oldObj) {
    let newObj = oldObj;
    if (oldObj && typeof oldObj === 'object') {
        newObj = Object.prototype.toString.call(oldObj) === "[object Array]" ? [] : {};
        for (let i in oldObj) {
            newObj[i] = deepCopy(oldObj[i]);
        }
    }
    return newObj;
}

export function getSchemaNames() {
  return Object.keys(schemas).map((i) => {
    return {name: schemas[i].name, value: i}
  })
}

export function getSchemaVersions(schemaName) {
  if (schemas[schemaName].versions != null) {
    return Object.keys(schemas[schemaName].versions).map((i) => {
      return {name: i, value: i}
    })
  } else {
    return []
  }
}

export function getSchema(schemaName, version, otherSchema) {
  version = version.replace(/_/g, '.');
  let schema = schemas[schemaName].versions[version];

  if (otherSchema != null) {
    let rawschema = JSON.parse(localStorage.getItem('otherSchema'))[otherSchema];
    schema.schema = groomSchema(rawschema, schemaName, version)
  }

  return schema
}

export function getOtherSchemas() {
  let otherSchemas = localStorage.getItem('otherSchema') ? JSON.parse(localStorage.getItem('otherSchema')) : {};

  return Object.keys(otherSchemas).map((i) => {
      return {name: i, value: i}
  })
}

export function allowOther(schemaName) {
  return schemas[schemaName].allowOther
}

export function removeEmpty(obj) {
  Object.keys(obj).forEach(function(key) {
    if (obj[key] && typeof obj[key] === 'object') {
      removeEmpty(obj[key]);
      if (Object.keys(obj[key]).length === 0) {
        delete obj[key]
      }
    }
    else if (obj[key] == null) delete obj[key]
  });
  return obj
}

function processSchema(schema, schemaName, version, labels) {
  schema = groomSchema(schema, schemaName, version);
  if (labels != null) {
    schema = mergeLabels(schema, labels)
  }

  return schema
}

function mergeLabels(schema, labels) {
  for (let key in labels) {
    //if (key == "data") {console.log(schema)}
    if (typeof labels[key] === 'object') {
      if ('properties' in schema && key in schema.properties) {
          schema.properties[key] = mergeLabels(schema.properties[key], labels[key])
      } else if ('items' in schema && 'properties' in schema.items && key in schema.items.properties) {
        schema.items.properties[key] = mergeLabels(schema.items.properties[key], labels[key])
      }
    } else {
      if ('items' in schema && 'enum' in schema.items) {
        [schema.items.enum, schema.items.enumNames] = processEnums(schema.items, labels)
      } else if ('enum' in schema) {
        [schema.enum, schema.enumNames] = processEnums(schema, labels)
      }
    }
  }

  return schema
}

function sortWithIndices(toSort) {
  for (let i = 0; i < toSort.length; i++) {
    toSort[i] = [toSort[i], i];
  }
  toSort.sort(function(left, right) {
    return left[0] < right[0] ? -1 : 1;
  });
  toSort.sortIndices = [];
  for (let j = 0; j < toSort.length; j++) {
    toSort.sortIndices.push(toSort[j][1]);
    toSort[j] = toSort[j][0];
  }
  return toSort;
}

function processEnums(schema, labels) {
  let [enums, enumNames] = [schema.enum, buildEnumNames(schema.enum, labels)];
  let sortEnum = [];

  let sorted = sortWithIndices(enumNames);

  for (let i=0; i<sorted.sortIndices.length; i++) {
    sortEnum.push(enums[sorted.sortIndices[i]])
  }

  return [sortEnum, enumNames]
}

function buildEnumNames(schemaEnum, labels) {
  let enumNames = [];

  for (let i = 0; i < schemaEnum.length; i++) {
    enumNames.push(schemaEnum[i] in labels ? 
                   schemaEnum[i] !== labels[schemaEnum[i]] ? `${schemaEnum[i]}: ${labels[schemaEnum[i]]}` : schemaEnum[i] :
                   schemaEnum[i])
  }

  return enumNames
}

export function capWords(value) {
  return value.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase())
}

function schemaMatchesRule(schemaName, version, rule) {
  if ('all' in rule.schemas) {
    return true
  } else if (schemaName in rule.schemas) {
    return rule.schemas[schemaName].includes('all') ||
      rule.schemas[schemaName].includes(version)
  }

  return false
}

export function groomData(obj, schemaName, version) {
  return groomObject(obj, schemaName, version, true)
}

export function groomSchema(obj, schemaName, version) {
  return groomObject(obj, schemaName, version, false)
}

export function ungroomData(obj, schemaName, version) {
  return ungroomObject(obj, schemaName, version, true)
}

export function ungroomSchema(obj, schemaName, version) {
  return ungroomObject(obj, schemaName, version, false)
}

function groomObject(obj, schemaName, version, isData) {
  console.log(schemaName);
  console.log(version);
  console.log("");
  version = version.replace(/_/g, '.');
  let acc = deepCopy(obj);
  for (let i=0; i<groomSchemaDef.rules.length; i++) {
    let rule = groomSchemaDef.rules[i];

    if((version == "1.3.4") && (schemaName == "partner")) { // && (rule['field'].includes("source_id"))) {
      console.log("debug")
    }

    if (!schemaMatchesRule(schemaName, version, rule)) {
      continue
    }

    try {
      let field = getField(acc, rule.field, isData)
        
      if ((field !== undefined) && ('year_change' in rule) && ('default' in field)) {
        const d = new Date();
        if (d.getUTCMonth() < 6) {
          field.default = d.getUTCFullYear()
        } else {
          field.default = d.getUTCFullYear() + 1
        }
      }

      if ('move' in rule) {
        setField(acc, rule.move, field, isData);
        removeField(acc, rule.field, isData)
      } else if ('hide' in rule) {
        removeField(acc, rule.field, isData)
      } else if ('property' in rule && 'value' in rule) {
        setFieldProperty(acc, rule.field, rule.property, rule.value, isData)
      } else if ('value' in rule) {
        setField(acc, rule.field, rule.value, isData)
      }
    }
    catch (err) {
      console.log(`Error processing rule ${rule.field} on obj`, err)
    }

  }

  return acc;
}

function ungroomObject(obj, schemaName, version, isData) {
  version = version.replace(/_/g, '.');
  let acc = deepCopy(obj);
  for (let i=0; i<groomSchemaDef.rules.length; i++) {
    let rule = groomSchemaDef.rules[i];

    if (!schemaMatchesRule(schemaName, version, rule)) {
      continue
    }

    if ('move' in rule) {
      setField(acc, rule.field, getField(obj, rule.move, isData), isData);
      removeField(acc, rule.move, isData)
    } 
  }

  return acc;
}

function getField(obj, _keys, isData) {
  if (typeof obj === 'undefined') {
    return
  }
  
  let keys = _keys.slice();
  if (typeof keys.shift === 'undefined') {
    keys = [keys]
  }
  
  let key = keys.shift();
  if (key !== undefined)  {
    let result;
    if (isData) {
      result = getField(obj[key], keys, isData)
    } else {
      result = 'properties' in obj ? getField(obj.properties[key], keys, isData) : undefined
    }
    return result
  } 

  return obj
}

function setField(obj, _keys, value, isData) {
  if (typeof obj === 'undefined') {
    return
  }

  let keys = _keys.slice();
  if (typeof keys.shift === 'undefined') {
    keys = [keys]
  }

  let key = keys.shift();
  if (keys.length !== 0)  {
    if (isData) {
      if (!(key in obj)) {
        obj[key] = {}
      }
      setField(obj[key], keys, value, isData)
    } else {
      if (!(key in obj.properties)) {
        obj.properties[key] = { properties: {} }
      }
      setField(obj.properties[key], keys, value, isData)
    }
  } else {
    isData ? obj[key] = value : obj.properties[key] = value
  } 
}

function removeField(obj, _keys, isData) {
  if (typeof obj === 'undefined') {
    return
  }

  let keys = _keys.slice();
  if (typeof keys.shift === 'undefined') {
    keys = [keys]
  }

  let key = keys.shift();
  if (keys.length !== 0)  {
    isData ? removeField(obj[key], keys, isData) : removeField(obj.properties[key], keys, isData)
  } else {
    if (isData) {
      delete obj[key]
    } else {
      delete obj.properties[key];
      if (typeof obj.required !== 'undefined') {
        let index = obj.required.indexOf(key);
        obj.required.splice(index, 1);
        if (obj.required.length === 0) {
          delete obj['required'];
        }
      } 
    } 
  } 
}

function setFieldProperty(obj, _keys, property, value, isData) {
  if (typeof obj === 'undefined') {
    return
  }

  let keys = _keys.slice();
  if (typeof keys.shift === 'undefined') {
    keys = [keys]
  }

  let key = keys.shift();
  if (keys.length !== 0)  {
    isData ? setFieldProperty(obj[key], keys, value): setFieldProperty(obj.properties[key], keys, value)
  } else {
    isData ? obj[key][property] = value : obj.properties[key][property] = value
  } 
}

export function loadOtherSchema(fileDetails, file) {
  let schema = JSON.parse(file.target.result);
  
  let otherSchema = localStorage.getItem('otherSchema') ? JSON.parse(localStorage.getItem('otherSchema')) : {};
  otherSchema[fileDetails.name] = schema;

  localStorage.setItem('otherSchema', JSON.stringify(otherSchema))
}

function add_help(uiSchema) {
  for (let key in verisHelp) {
    let dest = key.split('.');
    dest.push('ui:help');
    setField(uiSchema, dest, verisHelp[key], true)
  }
  return uiSchema
}