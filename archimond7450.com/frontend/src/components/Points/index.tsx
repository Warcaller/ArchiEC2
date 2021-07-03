import React, { useEffect } from "react";

import NormalWrapper from "../NormalWrapper";
import Header from "../Header";
import Section from "../Section";

const Points = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <NormalWrapper>
      <Header title="Points" />
      <Section>
        <p>
          This page contains information about all points you can earn on my
          streams. There is also a leaderboard of top 10 viewers with each
          points.
        </p>
      </Section>
      <Section last>
        <p>TODO</p>
      </Section>
    </NormalWrapper>
  );
};

export default Points;
