import React from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import ButtonLink from "../ButtonLink";

import Section from "./Section";

const Schedule = () => {
  return (
    <Section imageClass="bg07">
      <Container>
        <Row className="justify-content-center">
          <Col xs={12} className="text-center">
            <h1>Regular schedule</h1>
            <p>
              I usually stream every day. Depending on where I am there are two
              possible schedules I generally stick to.
              <br />
              Please remember that I sometimes might not stream because of
              various reasons (job, work on websites or chatbot, vacation, etc.)
            </p>
          </Col>
        </Row>
        <p>&nbsp;</p>
        <Row className="justify-content-center">
          <Col xs={12} className="text-center">
            <h2>At home</h2>
            <p>
              Mon: 20:00 - 23:00
              <br />
              Tue: 20:00 - 23:00
              <br />
              Wed: 20:00 - 23:00
              <br />
              Thu: 20:00 - 23:00
              <br />
              Fri: 19:30 - 23:30
              <br />
              Sat: 19:30 - 23:30
              <br />
              Sun: 19:30 - 23:30
              <br />
              &nbsp;
            </p>
          </Col>
          <Col xs={12} className="text-center">
            <h2>In Prague</h2>
          </Col>
          <Col xs={12} md="auto" className="text-center text-lg-left">
            <h3>Odd week</h3>
            <p>
              Mon: 18:00 - 23:00
              <br />
              Tue: 18:00 - 23:30
              <br />
              Wed: 17:30 - 00:00
              <br />
              Thu: 18:00 - 23:30
              <br />
              Fri: 18:00 - 00:00
              <br />
              Sat: 16:00 - 00:00
              <br />
              Sun: NO STREAM
              <br />
              &nbsp;
            </p>
          </Col>
          <Col xs={12} md="auto" className="text-center text-lg-left">
            <h3>Even week</h3>
            <p>
              Mon: NO STREAM
              <br />
              Tue: 18:00 - 23:30
              <br />
              Wed: 19:00 - 00:00
              <br />
              Thu: 17:00 - 23:30
              <br />
              Fri: 18:00 - 00:00
              <br />
              Sat: 18:00 - 00:00
              <br />
              Sun: 17:30 - 23:30
              <br />
              &nbsp;
            </p>
          </Col>
          <Col xs={12} className="text-center">
            <ButtonLink to="/schedule/">More info</ButtonLink>
          </Col>
        </Row>
      </Container>
    </Section>
  );
};

export default Schedule;
