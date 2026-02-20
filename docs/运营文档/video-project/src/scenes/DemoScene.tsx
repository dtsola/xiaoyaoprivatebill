import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

interface DemoSceneProps {
  image: string;
  title: string;
  subtitle: string;
}

export const DemoScene = ({ image, title, subtitle }: DemoSceneProps) => {
  const frame = useCurrentFrame();

  // 截图缩放进入
  const scale = interpolate(frame, [0, 30], [0.8, 1], { extrapolateRight: "clamp" });

  // 标题淡入
  const titleOpacity = interpolate(frame, [20, 50], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#f0f9ff", justifyContent: "center", alignItems: "center" }}>
      <div style={{ transform: `scale(${scale})`, textAlign: "center" }}>
        <img
          src={image}
          style={{
            width: 1400,
            height: 700,
            borderRadius: 12,
            boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.15)",
          }}
        />
        <div style={{ marginTop: 40, opacity: titleOpacity }}>
          <h2 style={{ fontSize: 48, color: "#1e40af", margin: 0 }}>{title}</h2>
          <p style={{ fontSize: 28, color: "#64748b", marginTop: 10 }}>{subtitle}</p>
        </div>
      </div>
    </AbsoluteFill>
  );
};
