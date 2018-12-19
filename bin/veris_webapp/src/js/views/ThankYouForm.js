import React from 'react'

import { VzBoxComponent, VzLinkButton } from './vzcomponents'
import queryString from 'query-string'

export default function ThankYouForm(props) {
  const params = queryString.parse(props.location.search);

  let nextUrl;

  if ('next' in params) {
    nextUrl = `/submit/${params['next']}`
  } else {
    nextUrl = `/submit/${localStorage.getItem('lastSchema')}/${localStorage.getItem('lastVersion')}`
  }

  return <VzBoxComponent title="Thank You">
      <div>
        <pre>
          {JSON.stringify(JSON.parse(localStorage.getItem('incidents'))[props.match.params.incidentId])}
        </pre>
        <VzLinkButton to={nextUrl}>Return</VzLinkButton>
      </div>
    </VzBoxComponent>
      
} 
