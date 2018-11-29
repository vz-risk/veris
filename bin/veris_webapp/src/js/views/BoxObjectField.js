import React from "react";

import ObjectField from "react-jsonschema-form/lib/components/fields/ObjectField";
import { VzBoxComponent } from './vzcomponents';

import {
  orderProperties,
  retrieveSchema,
  getDefaultRegistry,
} from "react-jsonschema-form/lib/utils";

class BoxObjectField extends ObjectField {
  render() {
    const {
      uiSchema,
      formData,
      errorSchema,
      idSchema,
      name,
      required,
      disabled,
      readonly,
      onBlur,
      onFocus,
      registry = getDefaultRegistry(),
    } = this.props;
    const { definitions, fields, formContext } = registry;
    const { SchemaField, TitleField, DescriptionField } = fields;
    const schema = retrieveSchema(this.props.schema, definitions);
    const title = schema.title === undefined ? name : schema.title;
    let orderedProperties;
    try {
      const properties = Object.keys(schema.properties);
      orderedProperties = orderProperties(properties, uiSchema["ui:order"]);
    } catch (err) {
      return (
        <div>
          <p className="config-error" style={{ color: "red" }}>
            Invalid {name || "root"} object field configuration:
            <em>{err.message}</em>.
          </p>
          <pre>{JSON.stringify(schema)}</pre>
        </div>
      );
    }
    if (title !== undefined) {
      return (
        <VzBoxComponent title={title}>
          {orderedProperties.map((name, index) => {
            return (
              <SchemaField
                key={index}
                name={name}
                required={this.isRequired(name)}
                schema={schema.properties[name]}
                uiSchema={uiSchema[name]}
                errorSchema={errorSchema[name]}
                idSchema={idSchema[name]}
                formData={formData[name]}
                onChange={this.onPropertyChange(name)}
                onBlur={onBlur}
                onFocus={onFocus}
                registry={registry}
                disabled={disabled}
                readonly={readonly}
              />
            )
          })}
        </VzBoxComponent>
      );
    } else {
      return (
        <fieldset>
          {(uiSchema["ui:title"] || title) && (
            <TitleField
              id={`${idSchema.$id}__title`}
              title={uiSchema["ui:title"] || title}
              required={required}
              formContext={formContext}
            />
          )}
          {(uiSchema["ui:description"] || schema.description) && (
            <DescriptionField
              id={`${idSchema.$id}__description`}
              description={uiSchema["ui:description"] || schema.description}
              formContext={formContext}
            />
          )}
          {orderedProperties.map((name, index) => {
            return (
              <SchemaField
                key={index}
                name={name}
                required={this.isRequired(name)}
                schema={schema.properties[name]}
                uiSchema={uiSchema[name]}
                errorSchema={errorSchema[name]}
                idSchema={idSchema[name]}
                formData={formData[name]}
                onChange={this.onPropertyChange(name)}
                onBlur={onBlur}
                onFocus={onFocus}
                registry={registry}
                disabled={disabled}
                readonly={readonly}
              />
            );
          })}
        </fieldset>
      );
    }
  }
}

export default BoxObjectField;