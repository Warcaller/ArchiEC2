import { useState } from "react";
import { Carousel } from "react-bootstrap";

import Section from "./Section";

const news = [
  {
    imageClass: "bg03",
    caption: "Website up again",
    text:
      "After movement to AWS and some rewrite the website is working again!",
  },
  {
    imageClass: "bg03",
    caption: "Website being worked on",
    text:
      "The core part of the website is working but Archi is still working on it.",
  },
  {
    imageClass: "bg03",
    caption: "Streaming from home",
    text:
      "Until the end of February Archi has to stay home. Streams will probably be lower quality until Archi returns to Prague.",
  },
  {
    imageClass: "bg03",
    caption: "Old chatbot running",
    text:
      "Right now Archi has to use an old version of his chatbot. Overlay won't work as well as some commands and loyalty points.",
  },
];

const NewsCarousel = () => {
  return (
    <Carousel>
      {news.map(({ imageClass, caption, text }) => {
        return (
          <Carousel.Item interval={50 * caption.length + 75 * text.length}>
            <Section height={250} key={caption} imageClass={imageClass}>
              <Carousel.Caption>
                <h1>{caption}</h1>
                <p>{text}</p>
              </Carousel.Caption>
            </Section>
          </Carousel.Item>
        );
      })}
    </Carousel>
  );
};

export default NewsCarousel;
