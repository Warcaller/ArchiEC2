import React from "react";
import { Link } from "react-router-dom";
import { Navbar, Nav } from "react-bootstrap";

const Footer = () => {
  return (
    <Navbar collapseOnSelect variant="dark">
      <Navbar.Collapse className="justify-content-center">
        <Navbar.Text>
          &copy; 2018 - 2021 Miroslav Horák. All rights reserved.
        </Navbar.Text>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default Footer;
