import React, { FunctionComponent } from "react";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";

interface ButtonLinkProps {
  to: string;
  out?: boolean;
  variant?: string;
}

const ButtonLink: FunctionComponent<ButtonLinkProps> = (props) => {
  let { to, out, variant } = props;

  if (variant === undefined) {
    variant = "secondary";
  }

  const btn = <Button variant={variant}>{props.children}</Button>;
  return out ? <a href={to}>{btn}</a> : <Link to={to}>{btn}</Link>;
};

export default ButtonLink;
