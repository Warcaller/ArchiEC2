import React, { useEffect } from "react";

import NormalWrapper from "../NormalWrapper";
import Header from "../Header";
import Section from "../Section";

const Login = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <NormalWrapper>
      <Header title="Login" />
      <Section last>
        <p>TODO</p>
      </Section>
    </NormalWrapper>
  );
};

export default Login;
