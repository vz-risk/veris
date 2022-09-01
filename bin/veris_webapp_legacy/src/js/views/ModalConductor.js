import React from 'react';
import { observer } from 'mobx-react'

import { VzModal } from './vzcomponents.js'

@observer
export default class ModalConductor extends React.Component {
  render() {
    if (!this.props.appState.currentModal) {
      return null
    }

    return <VzModal
      isOpen={true}
      onOk={this.props.appState.currentModal.callback}
      onExtra={this.props.appState.currentModal.extraCallback}
      hideModal={() => this.props.appState.currentModal = null}
      {...this.props.appState.currentModal.props} />
  }
}