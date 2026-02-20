import { AbsoluteFill, useCurrentFrame } from "remotion";
import { ProblemScene } from "./scenes/ProblemScene";
import { SolutionScene } from "./scenes/SolutionScene";
import { DemoScene } from "./scenes/DemoScene";
import { TerminalScene } from "./scenes/TerminalScene";
import { CallToActionScene } from "./scenes/CallToActionScene";
import { PrivacyScene } from "./scenes/PrivacyScene";

import uploadScreenshot from "./screenshots/upload.png";
import overviewScreenshot from "./screenshots/overview.png";
import categoryScreenshot from "./screenshots/category.png";
import insightScreenshot from "./screenshots/insight.png";

// 场景时间轴（帧数 @ 30fps）
const SCENE1_END = 300; // 0-10s: 问题引入
const SCENE2_END = 750; // 10-25s: 解决方案
const SCENE3A_END = 1050; // 25-35s: 上传演示
const SCENE3B_END = 1350; // 35-45s: 年度总览
const SCENE3C_END = 1650; // 45-55s: 分类分析
const SCENE3D_END = 1950; // 55-65s: 消费洞察
const SCENE3E_END = 2100; // 65-70s: 隐私说明
const SCENE4_END = 2400; // 70-80s: 技术展示
const SCENE5_END = 2700; // 80-90s: 邀请试用

export const XiaoyaoBillPromo = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill>
      {/* 场景1：问题引入 (0-10s) */}
      {frame < SCENE1_END && <ProblemScene />}

      {/* 场景2：解决方案 (10-25s) */}
      {frame >= SCENE1_END && frame < SCENE2_END && <SolutionScene />}

      {/* 场景3A：上传演示 (25-35s) */}
      {frame >= SCENE2_END && frame < SCENE3A_END && (
        <DemoScene
          image={uploadScreenshot}
          title="拖拽上传"
          subtitle="自动识别支付宝/微信账单格式"
        />
      )}

      {/* 场景3B：年度总览 (35-45s) */}
      {frame >= SCENE3A_END && frame < SCENE3B_END && (
        <DemoScene
          image={overviewScreenshot}
          title="年度总览"
          subtitle="收入支出清晰可见，月度趋势一目了然"
        />
      )}

      {/* 场景3C：分类分析 (45-55s) */}
      {frame >= SCENE3B_END && frame < SCENE3C_END && (
        <DemoScene
          image={categoryScreenshot}
          title="分类分析"
          subtitle="钱花在哪一看便知"
        />
      )}

      {/* 场景3D：消费洞察 (55-65s) */}
      {frame >= SCENE3C_END && frame < SCENE3D_END && (
        <DemoScene
          image={insightScreenshot}
          title="消费洞察"
          subtitle="智能分析消费习惯，发现省钱机会"
        />
      )}

      {/* 场景3E：隐私说明 (65-70s) */}
      {frame >= SCENE3D_END && frame < SCENE3E_END && <PrivacyScene />}

      {/* 场景4：技术展示 (70-80s) */}
      {frame >= SCENE3E_END && frame < SCENE4_END && <TerminalScene />}

      {/* 场景5：邀请试用 (80-90s) */}
      {frame >= SCENE4_END && <CallToActionScene />}
    </AbsoluteFill>
  );
};
