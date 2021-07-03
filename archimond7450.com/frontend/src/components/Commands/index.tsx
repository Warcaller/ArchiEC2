import React, { useEffect } from "react";

import NormalWrapper from "../NormalWrapper";
import Header from "../Header";
import Section from "../Section";

const Commands = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <NormalWrapper>
      <Header title="Commands" />
      <Section>
        <p>
          This page contains the complete list of commands the chatbot uses.
        </p>
      </Section>
      <Section last>
        <p>TODO</p>
      </Section>
    </NormalWrapper>
  );
};

export default Commands;
