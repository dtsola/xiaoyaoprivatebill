import { AbsoluteFill, interpolate, useCurrentFrame, spring } from "remotion";
import logo from "../screenshots/logo.png";

export const SolutionScene = () => {
  const frame = useCurrentFrame();

  // Logo 弹簧放大动画
  const scale = spring({
    frame,
    fps: 30,
    config: { damping: 100, stiffness: 100 },
  });

  // 文字淡入
  const textOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#f0f9ff", justifyContent: "center", alignItems: "center" }}>
      <div style={{ transform: `scale(${scale})`, textAlign: "center" }}>
        <img
          src={logo}
          style={{
            width: 200,
            height: 200,
            margin: "0 auto 40px",
            borderRadius: 40,
          }}
        />
        <h1 style={{ fontSize: 72, fontWeight: "bold", color: "#1e40af", margin: 0 }}>小遥账单助手</h1>
        <div style={{ opacity: textOpacity, fontSize: 36, color: "#64748b", marginTop: 20 }}>
          隐私优先 · 完全本地化 · 数据零泄露
        </div>
      </div>
    </AbsoluteFill>
  );
};
