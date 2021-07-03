import React, { useEffect } from "react";

import NormalWrapper from "../NormalWrapper";
import Header from "../Header";
import Section from "../Section";

const About = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <NormalWrapper>
      <Header title="About" />
      <Section>
        <p>
          This page contains more information about me. You can find here the
          following information.
        </p>
        <ul>
          <li>Basic information about me</li>
          <li>History of streaming</li>
          <li>Information about my current PCs</li>
          <li>My plans for the future</li>
        </ul>
      </Section>
      <Section title="Basic information">
        <p>
          My name is Miroslav Horák. I'm from the Czech Republic, currently
          working in Prague for company Artin as an external developer for
          T-Mobile. I'm 26 years old and love gaming and development and that's
          what I stream. I've been streaming for more than 4 years and I managed
          to grow a small and loyal community.
        </p>
      </Section>
      <Section title="History of streaming">
        <p>TODO</p>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Magni, totam
          voluptatum. Accusamus minus earum molestias illum optio consequatur
          voluptate quo quos. Velit dolorum non explicabo architecto dolore quo
          ipsum incidunt quod? Quae consequatur beatae voluptates molestias.
          Quibusdam delectus excepturi placeat quaerat. Vitae harum tenetur
          soluta ad veniam nihil veritatis, facere dicta excepturi nostrum quod
          et, quae libero aliquid possimus quasi.
        </p>
      </Section>
      <Section title="Information about my current PCs">
        <p>TODO</p>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Magni, totam
          voluptatum. Accusamus minus earum molestias illum optio consequatur
          voluptate quo quos. Velit dolorum non explicabo architecto dolore quo
          ipsum incidunt quod? Quae consequatur beatae voluptates molestias.
          Quibusdam delectus excepturi placeat quaerat. Vitae harum tenetur
          soluta ad veniam nihil veritatis, facere dicta excepturi nostrum quod
          et, quae libero aliquid possimus quasi.
        </p>
      </Section>
      <Section title="My plans for the future" last>
        <p>TODO</p>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Magni, totam
          voluptatum. Accusamus minus earum molestias illum optio consequatur
          voluptate quo quos. Velit dolorum non explicabo architecto dolore quo
          ipsum incidunt quod? Quae consequatur beatae voluptates molestias.
          Quibusdam delectus excepturi placeat quaerat. Vitae harum tenetur
          soluta ad veniam nihil veritatis, facere dicta excepturi nostrum quod
          et, quae libero aliquid possimus quasi.
        </p>
      </Section>
    </NormalWrapper>
  );
};

export default About;
