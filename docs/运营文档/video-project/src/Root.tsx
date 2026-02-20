import "./index.css";
import { Composition } from "remotion";
import { XiaoyaoBillPromo } from "./Composition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="XiaoyaoBillPromo"
        component={XiaoyaoBillPromo}
        durationInFrames={3600}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
