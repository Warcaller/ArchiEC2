import React from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import Navigation from "./components/Navigation";
import Footer from "./components/Footer";
import Home from "./components/Home/";
import About from "./components/About/";
import Schedule from "./components/Schedule";
import Commands from "./components/Commands";
import Points from "./components/Points";
import Login from "./components/Login";

const App = () => {
  return (
    <>
      <BrowserRouter>
        <>
          <Navigation />
          <Switch>
            <Route exact path="/" component={Home} />
            <Route exact path="/about/" component={About} />
            <Route exact path="/schedule/" component={Schedule} />
            <Route exact path="/commands/" component={Commands} />
            <Route exact path="/points/" component={Points} />
            <Route exact path="/login/" component={Login} />
          </Switch>
          <Footer />
        </>
      </BrowserRouter>
    </>
  );
};

export default App;
