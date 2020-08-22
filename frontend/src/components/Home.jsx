import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, Button, Badge, Table, Alert,
  Tooltip, OverlayTrigger, Card, ListGroup } from 'react-bootstrap';
import { FiHelpCircle, FiCircle, FiTrash2, FiAlertTriangle } from 'react-icons/fi';
import { useParams } from 'react-router-dom';
import BootstrapTable from 'react-bootstrap-table-next';
import _ from 'lodash';

import fetch from 'isomorphic-fetch';
import { useInput, postData, get_data } from '../util';
import moment from 'moment';


export const Home = (props) => {
  const [jobs, setJobs] = useState([]);

  const reloadJobs = () => {
    get_data('/api/jobs', setJobs);
  };

  useEffect(() => {
    reloadJobs();
    // Periodically retrieve the jobs to keep the view up to date.
    const interval = setInterval(reloadJobs, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <Container className='home'>
      <Row>
        <Card body className='mt-3 mb-3'>
          <CreateRunForm setJobs={setJobs} />
        </Card>
      </Row>

      {jobs.map((val, i) => <Row>
        <Job
          expanded={val.runs?.length > 0 && !val.completed_at}
          reloadJobs={reloadJobs} {...val} />
      </Row>)}
    </Container>
  );
};

export const JobView = (props) => {
  let { jobId } = useParams();
  const [job, setJob] = useState(null);

  useEffect(() => {
    if (jobId) get_data(`/api/jobs/${jobId}`, setJob);
  }, [jobId]);

  if (!job) {
    return <></>;
  }

  return <Container>
    <Row>
      <RunsTable job={job} />
    </Row>
  </Container>;
};

export const RunsTable = ({ job }) => {

  const statusFormatter = (cell, row) => {
    if (row.state == 'succeeded')
      return <FiCircle className="ok" />;
    else if (cell.startsWith('failed:'))
      return <RunErrorIcon id={row.id}>
      </RunErrorIcon>;

    return <div style={{display: 'flex', 'justify-content': 'center'}}>
      <FiCircle className="running" />
    </div>;
  };

  const columns = [
    { text: 'status', headerStyle: {width: "8%"}, dataField: 'state',
      formatter: statusFormatter },
  ];

  return <BootstrapTable
    className='runs-table'
    keyField="id" data={job.runs} columns={columns}
    bootstrap4 striped condensed />;
};

const CreateRunForm = ({ setJobs }) => {
  const { value:name, bind:bind_name, reset:reset_name } = useInput("");
  const { value:msg, bind:bind_msg, reset:reset_msg } = useInput("");

  const handleSubmit = (evt) => {
    evt.preventDefault();

    const postdata = {name, msg, user: 'user1'};

    postData('/api/job', postdata).then(data => get_data(`/api/jobs/`, setJobs));

    reset_msg();
    reset_name();
  }

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Row>
        <Form.Group as={Col} xs={10} controlId="formName">
          <Form.Label>
            Name
            <Help>
              The name of the person to greet
            </Help>
          </Form.Label>
          <Form.Control type="text" {...bind_name} placeholder="name" />
        </Form.Group>

        <Form.Group as={Col} xs={10} controlId="formMsg">
          <Form.Label>
            Message
          </Form.Label>
          <Form.Control type="text" {...bind_msg} placeholder="how are you?" />
        </Form.Group>
      </Form.Row>

      <Button variant="primary" type="submit">
        Schedule greeting
      </Button>
    </Form>
  );
};


const Help = (props) => {
  return <OverlayTrigger placement="bottom" delay={{ show: 100, hide: 200 }} overlay={
    <Tooltip id={`tt-${props.id}`}>{props.children}</Tooltip>
    }>
    <FiHelpCircle className='help-icon' />
  </OverlayTrigger>;
};

const Job = (props) => {
  const created_at = moment.utc(props.created_at);
  const started_at = props.started_at ? moment.utc(props.started_at) : null;
  const completed_at = props.completed_at ? moment.utc(props.completed_at) : null;

  let state;
  let status_icon;

  if (completed_at) {
    state = `completed ${completed_at.fromNow()}`;
    status_icon = <FiCircle className="ok" />;
  } else if (started_at) {
    state = `running as of ${started_at.fromNow()}`;
    status_icon = <FiCircle className="running" />;
  } else {
    state = `queued ${created_at.fromNow()}`;
    status_icon = <FiCircle className="pending" />;
  }

  return <Card width="100%" className="job">
    <Card.Header>
      <div className="status-icon">{status_icon}</div>
      {props.job_type}
      <Badge pill variant="light" className="user">by {props.user}</Badge>
    </Card.Header>

    <Card.Body>
      <div className='job-card-row'>
        <ul>
        {_.map(props.params, (v, k) => <li key={k}><b>{k}</b>: {v}</li>)}
        </ul>
      </div>
    </Card.Body>
  </Card>;
};
