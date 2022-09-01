import React from 'react'
import { capWords } from '../dbir-common'

export default function CustomFieldTemplate(props) {
  const {id, classNames, label, help, required, description, errors, children, displayLabel} = props;
  return (
    <div className={classNames}>
      {displayLabel && label !== undefined && id !== 'root' && <label htmlFor={id}>{capWords(label)}{required ? "*" : null}</label>}
      {children}
      {errors}
      {id !== 'root' && description}
      {help}
    </div>
  );
}