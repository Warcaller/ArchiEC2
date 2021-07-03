import React from "react";
import { Container, Row, Col, Image } from "react-bootstrap";

import Section from "./Section";
import ButtonLink from "../ButtonLink";

import archiSmileImage from "../../images/archi-civil-smile_256x256.png";

const ShortAbout = () => {
  return (
    <Section imageClass="bg02">
      <Container>
        <Row className="justify-content-center no-margin">
          <Col xs={12} lg="auto" className="text-center">
            <Image alt="Archi" src={archiSmileImage} roundedCircle />
          </Col>
          <Col xs={12} lg="auto" className="text-center text-lg-left">
            <h1>Shortly about me</h1>
            <p>
              My name is Miroslav Horák. I'm from the Czech Republic.
              <br />
              I am a Twitch streamer with a very small community.
              <br />
              I usually stream from Prague but occasionally I stream from my
              worse PC at home.
              <br />
              Since February 2021 I've been streaming also to Youtube.
              <br />
              I tried to stream to Facebook for a while as well but decided it
              isn't worth it.
              <br />
              I used to mainly stream Warcraft III but nowadays I stream more
              variety.
              <br />
              On Twitch i use my own chatbot. It's still work in progress.
              <br />
            </p>
            <ButtonLink to="/about/">More info</ButtonLink>
          </Col>
        </Row>
      </Container>
    </Section>
  );
};

export default ShortAbout;
