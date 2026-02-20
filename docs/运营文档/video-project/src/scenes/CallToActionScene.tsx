import { AbsoluteFill, useCurrentFrame, spring, interpolate } from "remotion";
import logo from "../screenshots/logo.png";

export const CallToActionScene = () => {
  const frame = useCurrentFrame();

  // Logo 放大
  const scale = spring({
    frame,
    fps: 30,
    config: { damping: 100 },
  });

  // 文字淡入
  const textOpacity = interpolate(frame, [30, 60], [0, 1]);
  const linkOpacity = interpolate(frame, [90, 120], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ transform: `scale(${scale})`, textAlign: "center" }}>
        <img
          src={logo}
          style={{
            width: 180,
            height: 180,
            margin: "0 auto 30px",
            borderRadius: 36,
            backgroundColor: "rgba(255, 255, 255, 0.2)",
            backdropFilter: "blur(10px)",
          }}
        />
        <h1 style={{ fontSize: 64, color: "#fff", marginBottom: 20, margin: 0 }}>小遥账单助手</h1>
        <p style={{ fontSize: 32, color: "#e0e7ff", opacity: textOpacity, marginTop: 10, marginBottom: 0 }}>
          已开源 · 欢迎Star
        </p>
        <div style={{ opacity: linkOpacity, marginTop: 40, fontSize: 28, color: "#fff" }}>
          https://github.com/dtsola/xiaoyaoprivatebill
        </div>
        <div style={{ opacity: linkOpacity, marginTop: 20, fontSize: 24, color: "#fbbf24" }}>
          ⭐ 欢迎Star支持
        </div>
      </div>
    </AbsoluteFill>
  );
};
