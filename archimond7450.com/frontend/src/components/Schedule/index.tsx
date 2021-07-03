import React, { useEffect } from "react";

import NormalWrapper from "../NormalWrapper";
import Header from "../Header";
import Section from "../Section";
import AccurateSchedule from "./AccurateSchedule";

const Schedule = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <NormalWrapper>
      <Header title="Schedule" />
      <Section>
        <p>
          This page contains the accurate schedule. If the schedule fails to
          load or looks out of date, please contact me on Discord.
        </p>
      </Section>
      <Section last>
        <AccurateSchedule />
      </Section>
    </NormalWrapper>
  );
};

export default Schedule;
