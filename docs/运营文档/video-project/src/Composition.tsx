import { AbsoluteFill, useCurrentFrame } from "remotion";
import { ProblemScene } from "./scenes/ProblemScene";
import { SolutionScene } from "./scenes/SolutionScene";
import { DemoScene } from "./scenes/DemoScene";
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

// 场景时间轴（帧数 @ 30fps，总时长 120秒 = 3600帧）
const SCENE1_END = 300; // 0-10s: 问题引入
const SCENE2_END = 750; // 10-25s: 解决方案
const SCENE3A_END = 990; // 25-33s: 上传账单
const SCENE3B_END = 1230; // 33-41s: 首页
const SCENE3C_END = 1470; // 41-49s: 年度总览
const SCENE3D_END = 1710; // 49-57s: 月度分析
const SCENE3E_END = 1950; // 57-65s: 分类分析
const SCENE3F_END = 2190; // 65-73s: 时间分析
const SCENE3G_END = 2430; // 73-81s: 消费洞察1
const SCENE3H_END = 2670; // 81-89s: 消费洞察2
const SCENE3I_END = 2910; // 89-97s: 消费洞察3
const SCENE3J_END = 3150; // 97-105s: 交易记录
const SCENE4_END = 3450; // 105-115s: 隐私说明
const SCENE5_END = 3600; // 115-120s: 邀请试用

export const XiaoyaoBillPromo = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill>
      {/* 场景1：问题引入 (0-10s) */}
      {frame < SCENE1_END && <ProblemScene />}

      {/* 场景2：解决方案 (10-25s) */}
      {frame >= SCENE1_END && frame < SCENE2_END && <SolutionScene />}

      {/* 场景3A：上传账单 (25-33s) */}
      {frame >= SCENE2_END && frame < SCENE3A_END && (
        <DemoScene
          image={uploadScreenshot}
          title="拖拽上传"
          subtitle="自动识别支付宝/微信账单格式"
        />
      )}

      {/* 场景3B：首页 (33-41s) */}
      {frame >= SCENE3A_END && frame < SCENE3B_END && (
        <DemoScene
          image={homeScreenshot}
          title="全能账单分析工具"
          subtitle="支持支付宝和微信账单，4大功能卡片"
        />
      )}

      {/* 场景3C：年度总览 (41-49s) */}
      {frame >= SCENE3B_END && frame < SCENE3C_END && (
        <DemoScene
          image={overviewScreenshot}
          title="年度总览"
          subtitle="收入支出清晰可见，月度趋势一目了然"
        />
      )}

      {/* 场景3D：月度分析 (49-57s) */}
      {frame >= SCENE3C_END && frame < SCENE3D_END && (
        <DemoScene
          image={monthlyScreenshot}
          title="月度分析"
          subtitle="月度收支趋势，环比同比分析"
        />
      )}

      {/* 场景3E：分类分析 (57-65s) */}
      {frame >= SCENE3D_END && frame < SCENE3E_END && (
        <DemoScene
          image={categoryScreenshot}
          title="分类分析"
          subtitle="钱花在哪一看便知"
        />
      )}

      {/* 场景3F：时间分析 (65-73s) */}
      {frame >= SCENE3E_END && frame < SCENE3F_END && (
        <DemoScene
          image={timeScreenshot}
          title="时间分析"
          subtitle="消费时间分布，发现消费规律"
        />
      )}

      {/* 场景3G：消费洞察1 (73-81s) */}
      {frame >= SCENE3F_END && frame < SCENE3G_END && (
        <DemoScene
          image={insight1Screenshot}
          title="消费洞察"
          subtitle="高频商户分析"
        />
      )}

      {/* 场景3H：消费洞察2 (81-89s) */}
      {frame >= SCENE3G_END && frame < SCENE3H_END && (
        <DemoScene
          image={insight2Screenshot}
          title="消费洞察"
          subtitle="大额消费提醒"
        />
      )}

      {/* 场景3I：消费洞察3 (89-97s) */}
      {frame >= SCENE3H_END && frame < SCENE3I_END && (
        <DemoScene
          image={insight3Screenshot}
          title="消费洞察"
          subtitle="消费建议与优化"
        />
      )}

      {/* 场景3J：交易记录 (97-105s) */}
      {frame >= SCENE3I_END && frame < SCENE3J_END && (
        <DemoScene
          image={recordsScreenshot}
          title="交易记录"
          subtitle="完整交易明细，支持多维度筛选"
        />
      )}

      {/* 场景4：隐私说明 (105-115s) */}
      {frame >= SCENE3J_END && frame < SCENE4_END && <PrivacyScene />}

      {/* 场景5：邀请试用 (115-120s) */}
      {frame >= SCENE4_END && <CallToActionScene />}
    </AbsoluteFill>
  );
};