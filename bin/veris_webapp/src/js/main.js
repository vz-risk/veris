import React from 'react'
import ReactDOM from 'react-dom'
import { 
  Route,
  Router,
  Switch
} from 'react-router-dom'
import { createHashHistory } from 'history'

import ModalConductor from './views/ModalConductor'
import SubmissionForm from './views/SubmissionForm'
import ThankYouForm from './views/ThankYouForm'

import appState from './appstate'

const history = createHashHistory();

const App = () => (
  <div>
    <Switch>
      <Route path='/submit/thankyou/:incidentId' component={ThankYouForm} />
      <Route path='/submit/:schema/:version/i/:incidentId' component={SubmissionForm} />
      <Route path='/submit/:schema/:version/:otherSchema/i/:incidentId' component={SubmissionForm} />
      <Route path='/submit/:schema/:version/:otherSchema' component={SubmissionForm} />
      <Route path='/' component={SubmissionForm} />
    </Switch>
  </div>
);

window.onload = function() {
  ReactDOM.render((
    <div>
      <Router history={history}>
        <App />
      </Router>
      <ModalConductor appState={appState} />
    </div>
  ), document.getElementById('app'))
};
