import { AbsoluteFill, useCurrentFrame } from "remotion";

export const TerminalScene = () => {
  const frame = useCurrentFrame();

  const lines = [
    "$ docker-compose up -d",
    "Starting xiaoyaobill... done",
    "",
    "访问 http://localhost:8888",
    "✓ 应用已启动",
  ];

  // 计算当前显示的行数
  const currentLine = Math.floor(frame / 45);

  return (
    <AbsoluteFill style={{ backgroundColor: "#f0f9ff", justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          backgroundColor: "#1e1e1e",
          padding: 40,
          borderRadius: 12,
          fontFamily: "monospace",
          fontSize: 28,
          color: "#f8f8f2",
          width: 1000,
          boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        }}
      >
        {lines.slice(0, currentLine + 1).map((line, i) => (
          <div key={i} style={{ marginBottom: 10 }}>
            {line.startsWith("$") ? <span style={{ color: "#61afef" }}>{line}</span> : line}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
