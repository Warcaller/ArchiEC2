import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import { Container } from "react-bootstrap";

import Navigation from "../Navigation";
import ShortAbout from "./ShortAbout";
import NewsCarousel from "./NewsCarousel";
import Schedule from "./Schedule";
import Footer from "../Footer";

const Home = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <>
      <NewsCarousel />
      <ShortAbout />
      <Schedule />
    </>
  );
};

export default Home;
