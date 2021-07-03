import React, { useState } from "react";
import { Nav, Navbar, NavDropdown, Image } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";

import archiImage from "../images/Archi.jpg";

const links = [
  {
    name: "Twitch",
    path: "https://www.twitch.tv/archimond7450",
    outside: true,
  },
  { name: "Divider 1", divider: true },
  { name: "Discord", path: "https://discord.gg/g5JG9Yg", outside: true },
  { name: "YouTube", path: "http://yt.vu/+archi", outside: true },
];

const logout_pages = [
  { name: "Home", path: "/", exact_path: true },
  { name: "About", path: "/about" },
  { name: "Schedule", path: "/schedule/" },
  { name: "Commands", path: "/commands/" },
  { name: "Points", path: "/points/" },
  { name: "Links", dropdown: links },
  { name: "Login", path: "/login/", exact_path: true },
];

const login_pages = [
  { name: "Home", path: "/", exact_path: true },
  { name: "About", path: "/about" },
  { name: "Schedule", path: "/schedule/" },
  { name: "Commands", path: "/commands/" },
  { name: "Points", path: "/points/" },
  { name: "Dashboard", path: "/dashboard/" },
  { name: "Logout", path: "/logout/", exact_path: true },
];

const Navigation = () => {
  const [pages, setPages] = useState(logout_pages);

  return (
    <Navbar collapseOnSelect expand="lg" variant="dark">
      <LinkContainer to="/">
        <Navbar.Brand>
          <Image
            alt=""
            src={archiImage}
            width="30"
            height="30"
            className="d-inline-block align-top"
            rounded
          />{" "}
          Archimond Gaming
        </Navbar.Brand>
      </LinkContainer>
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="mr-auto">
          {pages.map(({ name, path, exact_path, dropdown }) => {
            if (dropdown) {
              return (
                <NavDropdown
                  key={name}
                  title={name}
                  id={`collapsible-nav-dropdown-${name.toLowerCase()}`}
                >
                  {dropdown.map(({ name, path, outside, divider }) => {
                    if (divider) {
                      return <NavDropdown.Divider key={name} />;
                    } else if (typeof path === "string") {
                      return outside ? (
                        <NavDropdown.Item key={name} href={path}>
                          {name}
                        </NavDropdown.Item>
                      ) : (
                        <LinkContainer key={name} to={path}>
                          <NavDropdown.Item>{name}</NavDropdown.Item>
                        </LinkContainer>
                      );
                    }
                  })}
                </NavDropdown>
              );
            } else if (typeof path === "string") {
              return exact_path ? (
                <LinkContainer key={path} exact to={path}>
                  <Nav.Link>{name}</Nav.Link>
                </LinkContainer>
              ) : (
                <LinkContainer key={path} to={path}>
                  <Nav.Link>{name}</Nav.Link>
                </LinkContainer>
              );
            }
            throw Error("Navigation error!");
          })}
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default Navigation;
