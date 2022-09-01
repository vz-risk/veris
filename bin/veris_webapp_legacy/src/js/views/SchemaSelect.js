import React from 'react'
import {
  defaultSchemaName,
  defaultSchemaVersion,
  getSchemaVersions,
  loadOtherSchema,
  getSchemaNames,
  getOtherSchemas,
  allowOther
} from '../dbir-common'

export default class SchemaSelect extends React.Component {
  constructor(props) {
    super(props);

    const selectedSchema = props.schema ? props.schema : defaultSchemaName
    const selectedVersion = props.version ? props.version : defaultSchemaVersion

    const otherSchemas = getOtherSchemas();

    this.state = {
      schema: selectedSchema,
      version: selectedVersion,
      versionOptions: getSchemaVersions(selectedSchema),
      otherSchema: otherSchemas.length > 0 ? otherSchemas[0].value : undefined,
      otherSchemas: otherSchemas
    };

    this.handleSchemaChange = this.handleSchemaChange.bind(this);
    this.handleVersionChange = this.handleVersionChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.loadOtherSchema = this.loadOtherSchema.bind(this);
    this.handleOtherSchemaChange = this.handleOtherSchemaChange.bind(this);
    this.handleLoadClick = this.handleLoadClick.bind(this);
  }

  handleSchemaChange(event) {
    this.fillVersions(event.target.value);
  }

  fillVersions(schemaName) {
    const versions = getSchemaVersions(schemaName);
    const defaultVersion = defaultSchemaVersion;

    this.setState({
      versionOptions: versions,
      schema: schemaName,
      version: defaultVersion
    });
  }

  handleVersionChange(event) {
    this.setState({version: event.target.value})
  }

  handleOtherSchemaChange(event) {
    this.setState({otherSchema: event.target.value})
  }

  handleSubmit(event) {
    event.preventDefault();

    if (typeof this.props.onClick !== "undefined") {
      this.props.onClick({ schema: this.state.schema, version: this.state.version, otherSchema: allowOther(this.state.schema) ? this.state.otherSchema : undefined})
    }
  }

  loadOtherSchema(event) {
    const parent = this;

    let files = this.otherSchemaUpload.files;
    let reader = new FileReader();
    let fileDetails = files[0];
    reader.onload = function(file) {
      // populate the other schema
      loadOtherSchema(fileDetails, file);
      let otherSchemas = getOtherSchemas();

      parent.setState({
        otherSchema: otherSchemas.length > 0 ? otherSchemas[0].value : undefined,
        otherSchemas: getOtherSchemas()
      })
    };
    // call reader
    reader.readAsText(fileDetails)
  }

  clearOtherSchema(event) {
    localStorage.setItem('otherSchema', '{}');
    this.setState({otherSchemas: getOtherSchemas()})
  }

  handleLoadClick(event) {
    this.otherSchemaUpload.click()
  }

  render() {
    const createItem = (item, key) => 
      <option key={key} value={item.value}>{item.name}</option>

    return (
      <div>
        <h3 className="text-brand-red">Schema</h3>
        <form>
          <div className="formcomponents filter_content">
            <input
              ref={(input) => { this.otherSchemaUpload = input }}
              onChange={this.loadOtherSchema}
              type="file" style={{display: 'none'}} multiple={false} />
            <div className="col-lg-12 spacer10">
              <div className="filterfield_edit">
                <select value={this.state.schema} onChange={this.handleSchemaChange} className="form-control customdropdown">
                  {getSchemaNames().map(createItem)}
                </select>
              </div>
              <div className="clearfix" />
            </div>
            <div className="col-lg-12 spacer10">
              <div className="filterfield_edit">
                <select value={this.state.version.replace(/_/g, '.')} onChange={this.handleVersionChange} className="form-control customdropdown">
                  {this.state.versionOptions.map(createItem)}
                </select>
              </div>
              <div className="clearfix" />
            </div>
            <div className="col-lg-12 spacer10">
              <div className="filterfield_edit">
                <select value={this.state.otherSchema} onChange={this.handleOtherSchemaChange} className="form-control customdropdown"
                    disabled={!allowOther(this.state.schema)}>
                  {this.state.otherSchemas.map(createItem)}
                </select>
              </div>
              <div className="clearfix" />
            </div>
            <div className="col-lg-12 spacer10">
              <button className="btn btn-primary btn-radius side-button" onClick={this.handleSubmit}>Apply</button>
            </div>
            <div className="col-lg-6 spacer10">
              <button className="btn btn-primary btn-radius side-button" onClick={this.handleLoadClick}>Load</button>
            </div>
            <div className="col-lg-6 spacer10">
              <button className="btn btn-primary btn-radius side-button" onClick={this.clearOtherSchema}>Clear Other</button>
            </div>
          </div>
        </form>
      </div>
    )
  }
}
