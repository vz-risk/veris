import React from "react"

import ObjectField from "react-jsonschema-form/lib/components/fields/ObjectField"
import { VzCollapsible } from './vzcomponents'
import { capWords } from '../dbir-common'

import {
  orderProperties,
  retrieveSchema,
  getDefaultRegistry,
} from "react-jsonschema-form/lib/utils"

export default class CollapsableObjectField extends ObjectField {
  render() {
    const {
      uiSchema,
      formData,
      errorSchema,
      idSchema,
      name,
      disabled,
      readonly,
      onBlur,
      onFocus,
      registry = getDefaultRegistry(),
      classSuffix = '',
    } = this.props;
    const { definitions, fields } = registry;
    const { SchemaField } = fields;
    const schema = retrieveSchema(this.props.schema, definitions);
    const title = schema.title === undefined ? name : schema.title;
    let orderedProperties;
    try {
      const properties = Object.keys(schema.properties);
      orderedProperties = orderProperties(properties, uiSchema["ui:order"])
    } catch (err) {
      return (
        <div>
          <p className="config-error" style={{ color: "red" }}>
            Invalid {name || "root"} object field configuration:
            <em>{err.message}</em>.
          </p>
          <pre>{JSON.stringify(schema)}</pre>
        </div>
      )
    }
    return (
      <VzCollapsible trigger={capWords(uiSchema["ui:title"] || title)}
              className={`expandcollapse${classSuffix}`}
              openedClassName={`expandcollapse${classSuffix}`}
              triggerClassName={`expandcollapse${classSuffix}-topic`}
              triggerOpenedClassName={`expandcollapse${classSuffix}-topic`}
              contentOuterClassName={`expandcollapse${classSuffix}_content`}
              contentInnerClassName={`expandcollapse${classSuffix}_content_expanddiv1`}>
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
      </VzCollapsible>
    )
  }
}
