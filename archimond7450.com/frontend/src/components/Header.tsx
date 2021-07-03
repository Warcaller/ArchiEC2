import React, { FunctionComponent } from "react";

import { Container } from "react-bootstrap";

import HorizontalRule from "./HorizontalRule";

interface HeaderProps {
  title: string;
}

const Header: FunctionComponent<HeaderProps> = ({ title }) => {
  return (
    <Container className="text-center">
      <h1>{title}</h1>
      <HorizontalRule main />
    </Container>
  );

  interface HeaderProps {
    title: string;
  }
};

export default Header;
