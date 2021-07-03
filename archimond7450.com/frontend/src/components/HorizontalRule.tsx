import React, { FunctionComponent } from "react";

interface HorizontalRuleProps {
  main?: boolean;
}

const HorizontalRule: FunctionComponent<HorizontalRuleProps> = ({
  main = false,
}) => {
  return <hr className={`horizontalRule${main ? "Main" : "Content"}`} />;
};

export default HorizontalRule;
