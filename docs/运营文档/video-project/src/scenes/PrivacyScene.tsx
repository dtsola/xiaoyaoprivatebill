import { AbsoluteFill, interpolate, useCurrentFrame, spring } from "remotion";

export const PrivacyScene = () => {
  const frame = useCurrentFrame();

  // 图标弹簧动画
  const scale = spring({
    frame,
    fps: 30,
    config: { damping: 100 },
  });

  // 文字淡入
  const titleOpacity = interpolate(frame, [20, 50], [0, 1], { extrapolateRight: "clamp" });
  const subtitleOpacity = interpolate(frame, [50, 80], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#f0f9ff", justifyContent: "center", alignItems: "center" }}>
      <div style={{ transform: `scale(${scale})`, textAlign: "center" }}>
        <div
          style={{
            fontSize: 120,
            marginBottom: 30,
          }}
        >
          🔒
        </div>
        <h2 style={{ fontSize: 56, color: "#1e40af", margin: 0, opacity: titleOpacity }}>隐私无忧</h2>
        <p
          style={{
            fontSize: 32,
            color: "#64748b",
            marginTop: 20,
            opacity: subtitleOpacity,
            maxWidth: 800,
            lineHeight: 1.6,
          }}
        >
          所有数据本地处理，随时手动清除
        </p>
      </div>
    </AbsoluteFill>
  );
};
