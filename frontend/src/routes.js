import React from 'react';
import { Route, Switch } from 'react-router-dom';
import App from './components/App';
import { Home, JobView } from './components/Home';

const routes = (
  <App>
    <Switch>
      <Route exact path='/' component={Home} />
      <Route path='/jobs/:jobId' component={JobView} />
    </Switch>
  </App>
)

export { routes };
