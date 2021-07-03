import React, { FunctionComponent } from "react";
import { Container } from "react-bootstrap";

import HorizontalRule from "./HorizontalRule";

interface SectionProps {
  title?: string;
  last?: boolean;
}

const Section: FunctionComponent<SectionProps> = (props) => {
  const { title, last } = props;

  return (
    <>
      <Container className="padding">
        {title && (
          <Container className="text-center">
            <h2>{title}</h2>
          </Container>
        )}
        {props.children}
      </Container>
      {last || <HorizontalRule />}
    </>
  );
};

export default Section;
