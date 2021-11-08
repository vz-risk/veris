import React from 'react';
import ReactDOM from 'react-dom';

import {
  Redirect,
  Route,
  Router,
  Switch
} from 'react-router-dom';
import Engine from 'json-rules-engine-simplified';
import FileSaver from 'file-saver';
import Form from 'react-jsonschema-form';
import JSZip from 'jszip';
//import uuidv1 from 'uuid/v1';
import { v1 as uuidv1 } from 'uuid';
//import uuidv4 from 'uuid/v4';
import { v4 as uuidv4 } from 'uuid';
//import Ajv from 'ajv';
import Ajv from "ajv-draft-04"

import {
  defaultSchemaName,
  defaultSchemaVersion,
  getSchema,
  groomData,
  removeEmpty,
  ungroomData
} from '../dbir-common';
import ArrayFieldTemplate from './ArrayFieldTemplate';
import BoxObjectField from './BoxObjectField';
import CollapsableObjectField from './CollapsableObjectField';
import CollapsableSubObjectField from './CollapsableSubObjectField';
import CustomFieldTemplate from './CustomFieldTemplate';
import CustomDescriptionField from './CustomDescriptionField';
import SchemaSelect from './SchemaSelect';

import appState from '../appstate';
import meta from '../../../assets/meta.json';

const fields = {
  collapsable: CollapsableObjectField,
  collapsable2: CollapsableSubObjectField,
  ObjectField: BoxObjectField,
  DescriptionField: CustomDescriptionField
};

let ajv = new Ajv({allErrors: true, schemaId: 'id', strict: "log"});
//let ajv = new Ajv({allErrors: true, schemaId: '$id'});
//ajv.addMetaSchema(require('ajv-draft-04/src/refs/json-schema-draft-04.json'));

function clean(obj) {
  Object.keys(obj).forEach(function(key) {
    let value = obj[key];
    let type = typeof value;
    if (type === "object") {
      clean(obj[key]);
      if (!Object.keys(value).length) {
        delete obj[key];
      }
    } else if (type === "undefined") {
      delete obj[key];
    }
  });
}

class IncidentList extends React.Component {
  render() {
    let incidents = localStorage.getItem('incidents');
    if (!incidents) {
      incidents = {};
      localStorage.setItem('incidents', JSON.stringify(incidents));
    } else {
      incidents = JSON.parse(incidents);
    }
    let archived_incidents = JSON.parse(localStorage.getItem('archived_incidents') || '{}');

    const createItem = (item, key) =>
      <option key={item} value={item}>{item}</option>;

    return <div>
      <h3 className="text-brand-red">Incidents</h3>
      <form>
        <div className="formcomponents filter_content">
          <div className="col-lg-12 spacer10">
            <button className="btn btn-primary btn-radius side-button" onClick={this.props.newIncident}>New</button>
            <button className="btn btn-primary btn-radius side-button" onClick={this.props.importIncidents}>Import</button>
          </div>
          <div className="col-lg-12 spacer10">
            <div className="filterfield_edit">
              <select size="10" className="form-control customdropdown" onChange={this.props.selectIncident}>
                {Object.keys(incidents).map(createItem)}
              </select>
            </div>
            <div className="clearfix" />
          </div>
          <div className="col-lg-12">
            <button className="btn btn-primary btn-radius side-button spacer10" onClick={this.props.deleteIncident}>Delete</button>
            <button className="btn btn-primary btn-radius side-button spacer10" onClick={this.props.exportIncidents}>Export</button>
            <button className="btn btn-primary btn-radius side-button spacer10" onClick={this.props.clearIncidents}>Clear</button>
            {/* <button className="btn btn-primary btn-radius side-button spacer10" onClick={this.props.contribute}>Contribute</button> */}
          </div>
          {/* <div className="col-lg-12">
            <button className="btn btn-primary btn-radius side-button spacer10" onClick={this.props.duplicateIncident}>Duplicate</button>
            <input className="small-num" ref="duplicateAmount" type="number" min="1" defaultValue="1" /> Times
          </div> */}
          <h3 className="text-brand-red">Archived</h3>
          <div className="col-lg-12 spacer10">
            <div className="filterfield_edit">
              <select size="10" className="form-control customdropdown">
                {Object.keys(archived_incidents).map(createItem)}
              </select>
            </div>
            <div className="clearfix" />
          </div>
          <div className="col-lg-12">
            <button className="btn btn-primary btn-radius side-button spacer10" onClick={this.props.exportArchivedIncidents}>Re-export</button>
            <button className="btn btn-primary btn-radius side-button spacer10" onClick={this.props.clearArchivedIncidents}>Clear</button>
          </div>
        </div>
      </form>
    </div>
  }
}

export default class SubmissionForm extends React.Component {
  constructor(props) {
    super(props);

    if (this.props.location.search && this.props.location.search.includes('reset=1')) {
      localStorage.removeItem('lastOtherSchema');
      localStorage.removeItem('lastSchemaName');
      localStorage.removeItem('lastSchemaVersion');
    }

    this.selectedSchema = this.props.match.params.schema || localStorage.getItem('lastSchemaName') || defaultSchemaName;
    this.selectedVersion = this.props.match.params.version || localStorage.getItem('lastSchemaVersion') || defaultSchemaVersion;
    this.selectedOtherSchema = this.props.match.params.otherSchema || localStorage.getItem('lastOtherSchema');
    this.selectedIncidentId = this.props.match.params.incidentId;

    this.handleSchemaChange = this.handleSchemaChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
    this.selectIncident = this.selectIncident.bind(this);
    this.deleteIncident = this.deleteIncident.bind(this);
    this.importIncidents = this.importIncidents.bind(this);
    this.exportIncidents = this.exportIncidents.bind(this);
    this.loadIncidentData = this.loadIncidentData.bind(this);
    this.clearIncidents = this.clearIncidents.bind(this);
    this.duplicateIncident = this.duplicateIncident.bind(this);
    this.onChange = this.onChange.bind(this);
    this.exportArchivedIncidents = this.exportArchivedIncidents.bind(this);
    this.clearArchivedIncidents = this.clearArchivedIncidents.bind(this);
    this.debugDump = this.debugDump.bind(this);
    this.errors = [];

    if (this.selectedIncidentId) {
      this.loadIncidentData(this.selectedIncidentId)
    }
  }

  onChange = ({status, formData}) => {
    this.dirty = this.dirty || status === 'editing'
  };

  onSubmit(event) {
    const d = new Date();
    const rightNow = new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), d.getUTCHours(), d.getUTCMinutes(), d.getUTCSeconds(), d.getUTCMilliseconds()).toISOString();

    event.formData.plus.modified = rightNow;

    if (typeof event.formData.plus.created === 'undefined') {
      event.formData.plus.created = rightNow;
    }

    let record = event.formData;

    clean(record);

    const currentSchema = getSchema(this.selectedSchema, this.selectedVersion, this.selectedOtherSchema);
    const valid = ajv.validate(currentSchema.schema, record);
    if (!valid) {
      this.errors = ajv.errors;
      const errorNode = ReactDOM.findDOMNode(this.refs.errors);
      window.scrollTo(errorNode.offsetTop, 0);
      this.groomedData = event.formData;
      this.forceUpdate();
      return
    }
    
    console.log("Finally", event.formData);
    // Add data back in
    record = ungroomData(record, this.selectedSchema, this.selectedVersion);

    if (typeof record['schema_version'] === 'undefined') {
      //record['schema_version'] = this.selectedVersion.replace(/\./g, '_');
      record['schema_version'] = this.selectedVersion.replace(/_/g, '\.');
    }

    localStorage.setItem('incident_list_saved', false);

    const master_id = record.plus.master_id || record.master_id;

    let incidents = localStorage.getItem('incidents');
    if (!incidents) {
      incidents = {}
    } else {
      incidents = JSON.parse(incidents)
    }

    incidents[master_id] = removeEmpty(record);

    localStorage.setItem('incidents', JSON.stringify(incidents));

    const qs = this.nextIncident ? `?next=${this.nextIncident}` : '';
    this.props.history.push(`/submit/thankyou/${master_id}${qs}`)
  }

  clearIncidents(event) {
    appState.showModal({
      title: 'Clear Incidents',
      message: 'Are you sure you want to clear all of the incidents?'
    }, () => {
      localStorage.setItem('incidents', '{}');
      this.incidentList.forceUpdate()
    })
  }

  deleteIncident(event) {
    appState.showModal({
        title: 'Delete Incident',
        message: 'Are you sure you want to delete the selected incident?'
      }, () => {
        let incidents = JSON.parse(localStorage.getItem('incidents'));
        delete incidents[this.selectedIncidentId];
        localStorage.setItem('incidents', JSON.stringify(incidents));
        this.incidentList.forceUpdate()
      });
    return false
  }

  selectIncident(event) {
    // if (this.selectedIncidentId === event.target.value) {
    //   return
    // }

    const incidentId = this.selectedIncidentId = event.target.value;

    this.nextIncident = incidentId;

    let nextUrl;

    if (event.otherSchema) {
      nextUrl = `/submit/${this.selectedSchema}/${this.selectedVersion}/${this.selectedOtherSchema}/i/${this.selectedIncidentId}`
    } else {
      nextUrl = `/submit/${this.selectedSchema}/${this.selectedVersion}/i/${this.selectedIncidentId}`
    }

    if (this.dirty) {
      appState.showModal({
        title: 'Changing Incidents',
        message: 'You are changing incidents.  This will delete the in-work incident if not saved.',
        okText: 'Save then Load',
        extraText: 'Confirm'
      }, () => this.submitButton.click(),
      () => this.props.history.push(nextUrl))
    } else {
      this.props.history.push(nextUrl)
    }    
  }

  importIncidents(event) {
    let files = this.fileUpload.files;
    const incidentList =this.incidentList;
    
    for (let i = 0; i < files.length; i++) {
      let reader = new FileReader();
      reader.onload = function(incident) {
        const master_id = incident.target.fileName.substring(0, incident.target.fileName.length - 5);
        // populate the incidents object
        let incidents = JSON.parse(localStorage.getItem('incidents'));
        incidents[master_id] = JSON.parse(incident.target.result);
        localStorage.setItem('incidents', JSON.stringify(incidents));
        incidentList.forceUpdate();
      };
      reader.fileName = files[i].name;
      reader.readAsText(files[i]);
    }

    return false
  }

  duplicateIncident(event) {
    alert(this.incidentList.refs.duplicateAmount.value);
  }

  clearArchivedIncidents(event) {
    appState.showModal({
      title: 'Clear Archived Incidents',
      message: 'Are you sure you want to clear all of the archived incidents?'
    }, () => {
      localStorage.setItem('archived_incidents', '{}')
      this.incidentList.forceUpdate()
    })
  }

  exportArchivedIncidents(event) {
    let zip = new JSZip();
    let archived_incidents = JSON.parse(localStorage.getItem('archived_incidents') || '{}')
    
    for (let master_id in archived_incidents) {
      if (archived_incidents.hasOwnProperty(master_id)) {
        zip.file(`${master_id}.json`, JSON.stringify(archived_incidents[master_id], undefined, 4));
      }
    }
    zip.generateAsync({type:"blob"})
      .then(function(content) {
        FileSaver.saveAs(content, 'incidents.zip');
      });
    return false
  }

  debugDump(event) {
    let incidentsRaw = localStorage.getItem('incidents');
    const today = new Date();

    let incidentDump = document.createElement('a');
    incidentDump.href = 'data:attachment/text,' + encodeURI(incidentsRaw);
    incidentDump.target = '_blank';
    incidentDump.download = `debug_log_${today.getFullYear()}_${today.getMonth() + 1}_${today.getDate()}_${today.getHours()}_${today.getMinutes()}.log`;
    incidentDump.click();
  }

  exportIncidents(event) {
    let zip = new JSZip();
    let incidents = JSON.parse(localStorage.getItem('incidents'));
    let archived_incidents = JSON.parse(localStorage.getItem('archived_incidents') || '{}');
    archived_incidents = Object.assign(archived_incidents, incidents);
    
    if (Object.keys(incidents).length === 0) {
      alert('No incidents to export. Export cancelled.');
      return false;
    }

    for (let master_id in incidents) {
      if (incidents.hasOwnProperty(master_id)) {
        zip.file(`${master_id}.json`, JSON.stringify(incidents[master_id], undefined, 4));
      }
    }
    zip.generateAsync({type:"blob"})
      .then(function(content) {
        FileSaver.saveAs(content, 'incidents.zip');
      });

    localStorage.removeItem('incidents');
    localStorage.setItem('archived_incidents', JSON.stringify(archived_incidents));
    this.incidentList.forceUpdate();
    return false
  }

  loadIncidentData(incidentId) {
    let incidents = JSON.parse(localStorage.getItem('incidents'));
    if (typeof incidents === 'undefined') {
      return
    }

    const incident = incidents[incidentId];
    if (typeof incident === 'undefined') {
      return
    }

    this.selectedVersion = incident['schema_version'] || this.defaultSchemaVersion;

    this.groomedData = groomData(incident, this.selectedSchema, this.selectedVersion, this.selectedOtherSchema)
  }

  handleSchemaChange(event) {
    let nextUrl;
    if (event.otherSchema && this.selectedIncidentId) {
      nextUrl = `/submit/${event.schema}/${event.version}/${event.otherSchema}/i/${this.selectedIncidentId}`
    } else if (event.otherSchema) {
      nextUrl = `/submit/${event.schema}/${event.version}/${event.otherSchema}`
    } else if (this.selectedIncidentId) {
      nextUrl = `/submit/${event.schema}/${event.version}/i/${this.selectedIncidentId}`
    } else {
      nextUrl = `/submit/${event.schema}/${event.version}`
    }

    localStorage.setItem('lastSchemaName', event.schema);
    localStorage.setItem('lastSchemaVersion', event.version);
    if (typeof event.otherSchema === 'undefined') {
      localStorage.removeItem('lastOtherSchema')
    } else {
      localStorage.setItem('lastOtherSchema', event.otherSchema)
    }

    const form = this;
    const setParams = () => {
      form.selectedSchema = event.schema;
      form.selectedVersion = event.version;
      form.selectedOtherSchema = event.otherSchema
    };

    if (this.dirty) {
      appState.showModal({
          title: 'Changing Schema',
          message: 'You are changing schemas.  This will delete the in-work incident if not saved.',
          okText: 'Save then New',
          extraText: 'Confirm'
        }, () => this.submitButton.click() && setParams() && this.props.history.push(nextUrl),
        () => setParams() && this.props.history.push(nextUrl))
    } else {
      setParams();
      this.props.history.push(nextUrl)
    }
  }

  render() {
    if (this.selectedIncidentId) {
      this.loadIncidentData(this.selectedIncidentId)
    }

    const schema = this.selectedSchema;
    const version = this.selectedVersion;
    const otherSchema = this.selectedOtherSchema;
    const errors = this.errors;

    const currentSchema = getSchema(schema, version, otherSchema);
    const formData = this.groomedData ? this.groomedData : {
          "incident_id": uuidv1(), 
          "master_id": uuidv4()
        };

    this.groomedData = undefined;
    this.dirty = false;


    const createError = (item, index) => 
      <p key={`schema_error${index}`}>{item.dataPath}.{item.params[Object.keys(item.params)[0]]}: {item.message}</p>;

    return (
      <div id="gcontent">
        <div className="col-md-2 col-sm-3 border-right leftmenuitems">
          <div className="section-divider-bottom">
            <SchemaSelect onClick={this.handleSchemaChange}
                schema={schema}
                version={version} />
          </div>

          <div className="section-divider-bottom">
            <IncidentList
                ref={(incidentList) => { this.incidentList = incidentList }}
                selectIncident={this.selectIncident}
                newIncident={() => this.props.history.push(`/submit/${schema}/${version}`)}
                deleteIncident={this.deleteIncident}
                importIncidents={(e) => {this.fileUpload.click(); e.preventDefault() }}
                clearIncidents={this.clearIncidents}
                exportIncidents={this.exportIncidents}
                clearArchivedIncidents={this.clearArchivedIncidents}
                exportArchivedIncidents={this.exportArchivedIncidents}
                duplicateIncident={this.duplicateIncident}
                schema={schema}
                version={version} />
          </div>
       

          <input
              ref={(input) => { this.fileUpload = input }}
              onChange={this.importIncidents}
              type="file" style={{display: 'none'}} multiple={true} />

          <div className="section-divider-bottom">
            <h3>Alpha Build: {meta.build}</h3>
            {/*<button className="btn btn-primary btn-radius side-button spacer10" onClick={this.debugDump}>Debug Dump</button>*/}
          </div>
       
        </div>

        <div className="col-md-10 col-sm-9 right-content">

          <div ref="errors">
            {errors.length > 0 ? (<pre>
                {errors.map(createError)}
              </pre>) : undefined}
          </div>

          {currentSchema.schema ? (
            <Form schema={currentSchema.schema}
                uiSchema={currentSchema.uischema}
                onSubmit={this.onSubmit}
                onChange={this.onChange}
                fields={fields} 
                formData={formData}
                noValidate={true}
                noHtml5Validate={true}
                FieldTemplate={CustomFieldTemplate}
                ArrayFieldTemplate={ArrayFieldTemplate}>
            <button ref={(submitButton) => { this.submitButton = submitButton }}
                type="submit"
                className="btn btn-primary btn-radius spacer10">Save</button>
            </Form>
          ): (
            <h1>Something strange is afoot with the selected schema</h1>
          )}
        </div>

        <div className="clearfix" />
      </div>  
    )
  }
}
