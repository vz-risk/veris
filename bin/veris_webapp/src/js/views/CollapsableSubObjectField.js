import React, { Component } from 'react';

import CollapsableObjectField from './CollapsableObjectField'

export default class CollapsableSubObjectField extends Component {
  render() {
    return <CollapsableObjectField classSuffix='sub' {...this.props} />
  }
}

