import React from 'react'
import { compiler } from 'markdown-to-jsx'

export default function CustomDescriptionField({id, description}) {
  if (typeof description === "string") {
      return <div id={id}>{compiler(description)}</div>
  }
  return null;
};
