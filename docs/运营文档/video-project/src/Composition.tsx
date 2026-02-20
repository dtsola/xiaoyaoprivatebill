import { AbsoluteFill, useCurrentFrame, staticFile } from "remotion";
import { Audio } from "@remotion/media";
import { ProblemScene } from "./scenes/ProblemScene";
import { SolutionScene } from "./scenes/SolutionScene";
import { DemoScene } from "./scenes/DemoScene";
import { InsightCarouselScene } from "./scenes/InsightCarouselScene";
import { CallToActionScene } from "./scenes/CallToActionScene";
import { PrivacyScene } from "./scenes/PrivacyScene";

import uploadScreenshot from "./screenshots/upload.png";
import homeScreenshot from "./screenshots/home.png";
import overviewScreenshot from "./screenshots/overview.png";
import monthlyScreenshot from "./screenshots/monthly.png";
import categoryScreenshot from "./screenshots/category.png";
import timeScreenshot from "./screenshots/time.png";
import insight1Screenshot from "./screenshots/insight.png";
import insight2Screenshot from "./screenshots/insight2.png";
import insight3Screenshot from "./screenshots/insight3.png";
import recordsScreenshot from "./screenshots/records.png";

// 配音文件
const voiceover = staticFile("audio/voiceover.mp3");

// 场景时间轴（帧数 @ 30fps，总时长 90秒 = 2700帧）
// 基于实际配音时长优化，每个场景增加1-2秒过渡
const SCENE1_END = 270;   // 0-9s: 问题引入 (配音 8s)
const SCENE2_END = 660;   // 9-22s: 解决方案 (配音 11.7s)
const SCENE3A_END = 930;  // 22-31s: 上传账单 (配音 8.5s)
const SCENE3B_END = 1170; // 31-39s: 首页 (配音 6.3s)
const SCENE3C_END = 1350; // 39-45s: 年度总览 (配音 4.2s)
const SCENE3D_END = 1530; // 45-51s: 月度分析 (配音 3.5s)
const SCENE3E_END = 1710; // 51-57s: 分类分析 (配音 3.8s)
const SCENE3F_END = 1860; // 57-62s: 时间分析 (配音 3.5s)
const SCENE3G_END = 2100; // 62-70s: 消费洞察 (配音 7.1s)
const SCENE3H_END = 2220; // 70-74s: 交易记录 (配音 3.6s)
const SCENE4_END = 2400;  // 74-80s: 隐私说明 (配音 5.3s)
const SCENE5_END = 2700;  // 80-90s: 邀请试用 (配音 6.8s)

export const XiaoyaoBillPromo = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill>
      {/* 配音 */}
      <Audio src={voiceover} />

      {/* 场景1：问题引入 (0-9s) */}
      {frame < SCENE1_END && <ProblemScene />}

      {/* 场景2：解决方案 (9-22s) */}
      {frame >= SCENE1_END && frame < SCENE2_END && <SolutionScene />}

      {/* 场景3A：上传账单 (22-31s) */}
      {frame >= SCENE2_END && frame < SCENE3A_END && (
        <DemoScene
          image={uploadScreenshot}
          title="拖拽上传"
          subtitle="自动识别支付宝/微信账单格式"
        />
      )}

      {/* 场景3B：首页 (31-39s) */}
      {frame >= SCENE3A_END && frame < SCENE3B_END && (
        <DemoScene
          image={homeScreenshot}
          title="全能账单分析工具"
          subtitle="支持支付宝和微信账单，4大功能卡片"
        />
      )}

      {/* 场景3C：年度总览 (39-45s) */}
      {frame >= SCENE3B_END && frame < SCENE3C_END && (
        <DemoScene
          image={overviewScreenshot}
          title="年度总览"
          subtitle="收入支出清晰可见，月度趋势一目了然"
        />
      )}

      {/* 场景3D：月度分析 (45-51s) */}
      {frame >= SCENE3C_END && frame < SCENE3D_END && (
        <DemoScene
          image={monthlyScreenshot}
          title="月度分析"
          subtitle="月度收支趋势，环比同比分析"
        />
      )}

      {/* 场景3E：分类分析 (51-57s) */}
      {frame >= SCENE3D_END && frame < SCENE3E_END && (
        <DemoScene
          image={categoryScreenshot}
          title="分类分析"
          subtitle="钱花在哪一看便知"
        />
      )}

      {/* 场景3F：时间分析 (57-62s) */}
      {frame >= SCENE3E_END && frame < SCENE3F_END && (
        <DemoScene
          image={timeScreenshot}
          title="时间分析"
          subtitle="消费时间分布，发现消费规律"
        />
      )}

      {/* 场景3G：消费洞察轮播 (62-70s) - 3张截图轮播 */}
      {frame >= SCENE3F_END && frame < SCENE3G_END && (
        <InsightCarouselScene
          images={[insight1Screenshot, insight2Screenshot, insight3Screenshot]}
          relativeFrame={frame - SCENE3F_END}
        />
      )}

      {/* 场景3H：交易记录 (70-74s) */}
      {frame >= SCENE3G_END && frame < SCENE3H_END && (
        <DemoScene
          image={recordsScreenshot}
          title="交易记录"
          subtitle="完整交易明细，支持多维度筛选"
        />
      )}

      {/* 场景4：隐私说明 (74-80s) */}
      {frame >= SCENE3H_END && frame < SCENE4_END && <PrivacyScene />}

      {/* 场景5：邀请试用 (80-90s) */}
      {frame >= SCENE4_END && <CallToActionScene />}
    </AbsoluteFill>
  );
};
