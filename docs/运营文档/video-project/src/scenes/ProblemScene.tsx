import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const ProblemScene = () => {
  const frame = useCurrentFrame();

  // 文字逐行淡入
  const line1Opacity = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: "clamp" });
  const line2Opacity = interpolate(frame, [60, 120], [0, 1], { extrapolateRight: "clamp" });
  const line3Opacity = interpolate(frame, [120, 180], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000", justifyContent: "center", alignItems: "center" }}>
      <div style={{ fontSize: 48, color: "#fff", textAlign: "center", lineHeight: 1.8 }}>
        <div style={{ opacity: line1Opacity }}>想要分析自己的消费账单</div>
        <div style={{ opacity: line2Opacity }}>但不敢用第三方工具？</div>
        <div style={{ opacity: line3Opacity, color: "#ff6b6b" }}>因为担心数据上传、隐私泄露...</div>
      </div>
    </AbsoluteFill>
  );
};
