import React, { FunctionComponent } from "react";

import { Container } from "react-bootstrap";

interface NormalWrapperProps {
  backgroundColor?: string;
  textColor?: string;
}

const supportedColors = [
  "primary",
  "secondary",
  "success",
  "danger",
  "warning",
  "info",
  "light",
  "dark",
  "white",
];

const NormalWrapper: FunctionComponent<NormalWrapperProps> = (props) => {
  let { backgroundColor, textColor } = props;

  if (
    (backgroundColor && supportedColors.indexOf(backgroundColor) === -1) ||
    backgroundColor === undefined
  ) {
    backgroundColor = "dark";
  }

  if (
    (textColor && supportedColors.indexOf(textColor) === -1) ||
    textColor === undefined
  ) {
    textColor = "light";
  }

  return (
    <Container
      fluid
      className={`bg-${backgroundColor} text-${textColor} padding`}
    >
      {props.children}
    </Container>
  );
};

export default NormalWrapper;
