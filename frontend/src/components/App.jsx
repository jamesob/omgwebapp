import React from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';

export default class AppWrapper extends React.Component {
  render() {
    return (
      <div id="app">
        <Navbar bg="light" expand="lg">
          <Container>
            <Navbar.Brand href="/">
              changeme
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
            </Navbar.Collapse>
          </Container>
        </Navbar>

        {this.props.children}
      </div>
    );
  }
}
