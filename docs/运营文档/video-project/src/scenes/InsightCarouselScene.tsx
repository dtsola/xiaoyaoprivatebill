import { interpolate } from "remotion";

interface InsightCarouselProps {
  images: [string, string, string]; // 3张截图
  relativeFrame: number; // 场景内的相对帧数
}

export const InsightCarouselScene = ({ images, relativeFrame }: InsightCarouselProps) => {
  // 使用相对帧数
  const frame = Math.max(0, relativeFrame);

  // 8秒场景 (240帧)，每张图显示约2.67秒 (80帧)
  const imageIndex = Math.floor(frame / 80);
  const progressInCycle = (frame % 80) / 80;

  const scale = interpolate(progressInCycle, [0, 0.2, 0.8, 1], [0.9, 1, 1, 0.9]);
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={{
      flex: 1,
      background: "#f0f9ff",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
    }}>
      <h2 style={{
        fontSize: 64,
        fontWeight: "bold",
        color: "#1e40af",
        marginBottom: 40,
        opacity: titleOpacity,
      }}>
        消费洞察
      </h2>

      {/* 当前截图 */}
      <div style={{
        transform: `scale(${scale})`,
      }}>
        <img
          src={images[Math.min(imageIndex, 2)]}
          style={{
            width: 1400,
            height: 700,
            borderRadius: 20,
            boxShadow: "0 20px 60px rgba(0,0,0,0.15)",
            objectFit: "contain",
          }}
        />
      </div>

      {/* 进度指示器 */}
      <div style={{ marginTop: 30, display: "flex", gap: 12 }}>
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            style={{
              width: i === imageIndex ? 32 : 12,
              height: 12,
              borderRadius: 6,
              background: i === imageIndex ? "#3b82f6" : "#cbd5e1",
              transition: "all 0.3s",
            }}
          />
        ))}
      </div>

      {/* 副标题 */}
      <div style={{
        fontSize: 32,
        color: "#64748b",
        marginTop: 30,
      }}>
        {imageIndex === 0 && "高频商户分析"}
        {imageIndex === 1 && "大额消费提醒"}
        {imageIndex === 2 && "消费建议与优化"}
      </div>
    </div>
  );
};
