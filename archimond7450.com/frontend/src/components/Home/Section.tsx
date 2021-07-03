import { FunctionComponent } from "react";

interface HomeSectionProps {
  imageClass: string;
  height?: number;
}

const HomeSection: FunctionComponent<HomeSectionProps> = (props) => {
  const { imageClass, height } = props;
  return (
    <section
      style={{ height: height || "auto" }}
      className={`text-white image padding ${imageClass}`}
    >
      {props.children}
    </section>
  );
};

export default HomeSection;
