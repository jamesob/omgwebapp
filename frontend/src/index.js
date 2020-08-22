import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import { routes } from './routes';
import { BrowserRouter } from 'react-router-dom';
import './assets/styles/style';

// render the main component
ReactDOM.render(
  <BrowserRouter>
    {routes}
  </BrowserRouter>,
  document.getElementById('app')
);
