import { observable } from 'mobx'

class AppState {
  @observable currentModal = null

  @observable showModal(props, callback, extraCallback) {
    this.currentModal = {
      props: props,
      callback: callback,
      extraCallback: extraCallback
    }
  }
}

var appState = new AppState

export default appState