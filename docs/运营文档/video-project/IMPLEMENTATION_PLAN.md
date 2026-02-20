# 小遥账单助手 - Remotion 视频实施计划

> 视频时长：90秒 (2700帧 @ 30fps)
> 分辨率：1920x1080
> 创建日期：2026-02-20

---

## 项目概述

本视频使用 Remotion 4.0.417 + React 19 + TypeScript + Tailwind v4 制作。

**核心特点**：
- 使用现有截图，无需录制新视频
- 配音驱动（非背景音乐）
- 5个场景，90秒时长
- 代码复用性高

---

## 场景规划

| 场景 | 时长 | 帧数 | 内容 | 素材 |
|------|------|------|------|------|
| 场景1：问题引入 | 0-10s | 0-300 | 黑底白字逐行淡入 | 无 |
| 场景2：解决方案 | 10-25s | 300-750 | Logo放大 + 品牌标语 | Logo |
| 场景3A：上传演示 | 25-35s | 750-1050 | 上传页截图展示 | 08-上传账单.png |
| 场景3B：年度总览 | 35-45s | 1050-1350 | 年度总览截图 | 02-年度总览.png |
| 场景3C：分类分析 | 45-55s | 1350-1650 | 分类分析截图 | 04-分类分析.png |
| 场景3D：消费洞察 | 55-65s | 1650-1950 | 消费洞察截图 | 06-消费洞察-01.png |
| 场景3E：数据清除 | 65-70s | 1950-2100 | 隐私说明页面 | 文字卡片 |
| 场景4：技术展示 | 70-80s | 2100-2400 | 终端打字效果 | 无 |
| 场景5：邀请试用 | 80-90s | 2400-2700 | Logo + GitHub | Logo |

---

## 配音脚本（可直接录制）

### 场景1：问题引入（0-10秒）

```
想要分析自己的消费账单，但不敢用第三方工具？
因为担心数据上传、隐私泄露...
```

### 场景2：解决方案（10-25秒）

```
所以我开发了这个工具——小遥账单助手。
一个完全本地化的账单分析工具。
数据不上传服务器，支持支付宝和微信账单。
```

### 场景3：产品演示（25-70秒）

```
拖拽上传，自动识别格式。
支付宝 CSV、微信 CSV/XLSX 都支持。

年度总览一目了然，收入支出清晰可见。

分类占比分析，钱花在哪一看便知。

智能分析消费习惯，发现省钱机会。

所有数据都在本地处理，随时手动清除，隐私无忧。
```

### 场景4：技术展示（70-80秒）

```
前端使用 Vue 3 加 ECharts，
后端使用 Flask 加 Pandas。
一行 Docker 命令即可启动。
```

### 场景5：邀请试用（80-90秒）

```
项目已在 GitHub 开源，完全免费使用。
如果你也在寻找一个隐私安全的账单分析方案，
欢迎试用并给个Star支持。
```

---

## 资源准备

### 截图资源（已存在）

这些截图来自 `docs/产品文档/产品截图/`：

```
public/screenshots/
├── logo.png                 # 产品 Logo
├── 08-上传账单.png          # 上传页面
├── 02-年度总览.png          # 年度总览
├── 04-分类分析.png          # 分类分析
├── 06-消费洞察-01.png       # 消费洞察
└── 宣传海报图.png           # 宣传海报
```

### 配置脚本

将截图复制到项目 public 目录：

```bash
# Windows
mkdir docs\运营文档\video-project\public\screenshots
copy docs\产品文档\产品截图\Logo.png docs\运营文档\video-project\public\screenshots\logo.png
copy docs\产品文档\产品截图\08-上传账单.png docs\运营文档\video-project\public\screenshots\
copy docs\产品文档\产品截图\02-年度总览.png docs\运营文档\video-project\public\screenshots\
copy docs\产品文档\产品截图\04-分类分析.png docs\运营文档\video-project\public\screenshots\
copy docs\产品文档\产品截图\06-消费洞察-01.png docs\运营文档\video-project\public\screenshots\
```

### 配音文件

录制后放置在：

```
public/audio/
└── voiceover.mp3  # 90秒配音文件
```

---

## 组件结构

```
src/
├── Root.tsx              # 根组件，定义所有 Composition
├── Composition.tsx       # 主视频 Composition
├── scenes/
│   ├── ProblemScene.tsx          # 场景1：问题引入
│   ├── SolutionScene.tsx         # 场景2：解决方案
│   ├── DemoScene.tsx             # 场景3：产品演示（带截图）
│   ├── TerminalScene.tsx         # 场景4：技术展示
│   └── CallToActionScene.tsx     # 场景5：邀请试用
├── components/
│   ├── FadeText.tsx              # 淡入文字组件
│   ├── Logo.tsx                  # Logo 组件
│   ├── ScreenshotDisplay.tsx     # 截图展示组件
│   └── Terminal.tsx              # 终端组件
└── utils/
    └── timing.ts                 # 时间工具函数
```

---

## 核心组件实现

### 1. Root.tsx - 配置所有场景

```tsx
import { Composition } from "remotion";
import { XiaoyaoBillVideo } from "./Composition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="XiaoyaoBillPromo"
        component={XiaoyaoBillVideo}
        durationInFrames={2700}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          // 场景时间轴（帧数）
          scene1End: 300,      // 0-10s
          scene2End: 750,      // 10-25s
          scene3aEnd: 1050,    // 25-35s
          scene3bEnd: 1350,    // 35-45s
          scene3cEnd: 1650,    // 45-55s
          scene3dEnd: 1950,    // 55-65s
          scene3eEnd: 2100,    // 65-70s
          scene4End: 2400,     // 70-80s
          scene5End: 2700,     // 80-90s
        }}
      />
    </>
  );
};
```

### 2. ProblemScene.tsx - 问题引入

```tsx
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const ProblemScene = ({ endFrame }: { endFrame: number }) => {
  const frame = useCurrentFrame();

  // 文字逐行淡入
  const line1Opacity = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: 'clamp' });
  const line2Opacity = interpolate(frame, [60, 120], [0, 1], { extrapolateRight: 'clamp' });
  const line3Opacity = interpolate(frame, [120, 180], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#000', justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ fontSize: 48, color: '#fff', textAlign: 'center', lineHeight: 1.8 }}>
        <div style={{ opacity: line1Opacity }}>想要分析自己的消费账单</div>
        <div style={{ opacity: line2Opacity }}>但不敢用第三方工具？</div>
        <div style={{ opacity: line3Opacity, color: '#ff6b6b' }}>因为担心数据上传、隐私泄露...</div>
      </div>
    </AbsoluteFill>
  );
};
```

### 3. SolutionScene.tsx - 解决方案

```tsx
import { AbsoluteFill, interpolate, useCurrentFrame, spring } from "remotion";
import logo from "../screenshots/logo.png";

export const SolutionScene = ({ startFrame, endFrame }: { startFrame: number; endFrame: number }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  // Logo 弹簧放大动画
  const scale = spring({
    frame: localFrame,
    fps: 30,
    config: { damping: 100, stiffness: 100 },
  });

  // 文字淡入
  const textOpacity = interpolate(localFrame, [30, 60], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#f0f9ff', justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ transform: `scale(${scale})`, textAlign: 'center' }}>
        <img src={logo} style={{ width: 200, height: 200, marginBottom: 40 }} />
        <h1 style={{ fontSize: 72, fontWeight: 'bold', color: '#1e40af' }}>小遥账单助手</h1>
        <div style={{ opacity: textOpacity, fontSize: 36, color: '#64748b', marginTop: 20 }}>
          隐私优先 · 完全本地化 · 数据零泄露
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

### 4. DemoScene.tsx - 截图展示

```tsx
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

interface DemoSceneProps {
  startFrame: number;
  endFrame: number;
  image: string;
  title: string;
  subtitle: string;
}

export const DemoScene = ({ startFrame, endFrame, image, title, subtitle }: DemoSceneProps) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;
  const duration = endFrame - startFrame;

  // 截图缩放进入
  const scale = interpolate(localFrame, [0, 30], [0.8, 1], { extrapolateRight: 'clamp' });

  // 标题淡入
  const titleOpacity = interpolate(localFrame, [20, 50], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0f172a', justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ transform: `scale(${scale})`, textAlign: 'center' }}>
        <img
          src={image}
          style={{
            width: 1400,
            height: 700,
            borderRadius: 12,
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
          }}
        />
        <div style={{ marginTop: 40, opacity: titleOpacity }}>
          <h2 style={{ fontSize: 48, color: '#fff' }}>{title}</h2>
          <p style={{ fontSize: 28, color: '#94a3b8', marginTop: 10 }}>{subtitle}</p>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

### 5. TerminalScene.tsx - 终端打字效果

```tsx
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";

export const TerminalScene = ({ startFrame, endFrame }: { startFrame: number; endFrame: number }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  const lines = [
    "$ docker-compose up -d",
    "Starting xiaoyaobill... done",
    "",
    "访问 http://localhost:8888",
    "✓ 应用已启动"
  ];

  // 计算当前显示的行数
  const currentLine = Math.floor(localFrame / 30);

  return (
    <AbsoluteFill style={{ backgroundColor: '#1e1e1e', justifyContent: 'center', alignItems: 'center' }}>
      <div style={{
        backgroundColor: '#2d2d2d',
        padding: 40,
        borderRadius: 8,
        fontFamily: 'monospace',
        fontSize: 28,
        color: '#f8f8f2',
        width: 1000,
      }}>
        {lines.slice(0, currentLine + 1).map((line, i) => (
          <div key={i} style={{ marginBottom: 10 }}>
            {line.startsWith('$') ? <span style={{ color: '#61afef' }}>{line}</span> : line}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

### 6. CallToActionScene.tsx - 邀请试用

```tsx
import { AbsoluteFill, useCurrentFrame, spring, interpolate } from "remotion";
import logo from "../screenshots/logo.png";

export const CallToActionScene = ({ startFrame }: { startFrame: number }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  // Logo 放大
  const scale = spring({
    frame: localFrame,
    fps: 30,
    config: { damping: 100 },
  });

  // 文字淡入
  const textOpacity = interpolate(localFrame, [30, 60], [0, 1]);
  const linkOpacity = interpolate(localFrame, [90, 120], [0, 1]);

  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      justifyContent: 'center',
      alignItems: 'center'
    }}>
      <div style={{ transform: `scale(${scale})`, textAlign: 'center' }}>
        <img src={logo} style={{ width: 180, height: 180, marginBottom: 30 }} />
        <h1 style={{ fontSize: 64, color: '#fff', marginBottom: 20 }}>小遥账单助手</h1>
        <p style={{ fontSize: 32, color: '#e0e7ff', opacity: textOpacity }}>已开源 · 欢迎Star</p>
        <div style={{ opacity: linkOpacity, marginTop: 40, fontSize: 28, color: '#fff' }}>
          github.com/dtsola/xiaoyaoprivatebill
        </div>
      </div>
    </AbsoluteFit>
  );
};
```

---

## 主 Composition

```tsx
// Composition.tsx
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { ProblemScene } from "./scenes/ProblemScene";
import { SolutionScene } from "./scenes/SolutionScene";
import { DemoScene } from "./scenes/DemoScene";
import { TerminalScene } from "./scenes/TerminalScene";
import { CallToActionScene } from "./scenes/CallToActionScene";

import uploadScreenshot from "../screenshots/08-上传账单.png";
import overviewScreenshot from "../screenshots/02-年度总览.png";
import categoryScreenshot from "../screenshots/04-分类分析.png";
import insightScreenshot from "../screenshots/06-消费洞察-01.png";

export const XiaoyaoBillVideo = ({
  scene1End,
  scene2End,
  scene3aEnd,
  scene3bEnd,
  scene3cEnd,
  scene3dEnd,
  scene3eEnd,
  scene4End,
  scene5End,
}: {
  scene1End: number;
  scene2End: number;
  scene3aEnd: number;
  scene3bEnd: number;
  scene3cEnd: number;
  scene3dEnd: number;
  scene3eEnd: number;
  scene4End: number;
  scene5End: number;
}) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill>
      {/* 场景1：问题引入 */}
      {frame < scene1End && <ProblemScene endFrame={scene1End} />}

      {/* 场景2：解决方案 */}
      {frame >= scene1End && frame < scene2End && (
        <SolutionScene startFrame={scene1End} endFrame={scene2End} />
      )}

      {/* 场景3A：上传演示 */}
      {frame >= scene2End && frame < scene3aEnd && (
        <DemoScene
          startFrame={scene2End}
          endFrame={scene3aEnd}
          image={uploadScreenshot}
          title="拖拽上传"
          subtitle="自动识别支付宝/微信账单格式"
        />
      )}

      {/* 场景3B：年度总览 */}
      {frame >= scene3aEnd && frame < scene3bEnd && (
        <DemoScene
          startFrame={scene3aEnd}
          endFrame={scene3bEnd}
          image={overviewScreenshot}
          title="年度总览"
          subtitle="收入支出清晰可见，月度趋势一目了然"
        />
      )}

      {/* 场景3C：分类分析 */}
      {frame >= scene3bEnd && frame < scene3cEnd && (
        <DemoScene
          startFrame={scene3bEnd}
          endFrame={scene3cEnd}
          image={categoryScreenshot}
          title="分类分析"
          subtitle="钱花在哪一看便知"
        />
      )}

      {/* 场景3D：消费洞察 */}
      {frame >= scene3cEnd && frame < scene3dEnd && (
        <DemoScene
          startFrame={scene3cEnd}
          endFrame={scene3dEnd}
          image={insightScreenshot}
          title="消费洞察"
          subtitle="智能分析消费习惯，发现省钱机会"
        />
      )}

      {/* 场景3E：数据清除 */}
      {frame >= scene3dEnd && frame < scene3eEnd && (
        <DemoScene
          startFrame={scene3dEnd}
          endFrame={scene3eEnd}
          image={""}  // 使用文字卡片替代
          title="隐私无忧"
          subtitle="所有数据本地处理，随时手动清除"
        />
      )}

      {/* 场景4：技术展示 */}
      {frame >= scene3eEnd && frame < scene4End && (
        <TerminalScene startFrame={scene3eEnd} endFrame={scene4End} />
      )}

      {/* 场景5：邀请试用 */}
      {frame >= scene4End && (
        <CallToActionScene startFrame={scene4End} />
      )}
    </AbsoluteFill>
  );
};
```

---

## 开发步骤

### 第1步：准备资源

```bash
# 创建 public 目录
mkdir -p public/screenshots public/audio

# 复制截图文件
# (手动复制或使用上面提供的命令)
```

### 第2步：安装依赖

```bash
cd docs/运营文档/video-project
npm install
```

### 第3步：创建组件文件

按上面的组件结构创建文件：
```
src/scenes/ProblemScene.tsx
src/scenes/SolutionScene.tsx
src/scenes/DemoScene.tsx
src/scenes/TerminalScene.tsx
src/scenes/CallToActionScene.tsx
```

### 第4步：启动开发服务器

```bash
npm run dev
```

访问 http://localhost:4321 查看 Remotion Studio

### 第5步：预览和调整

在 Remotion Studio 中：
1. 预览各场景动画效果
2. 调整时间轴
3. 修改样式和动画参数

### 第6步：添加配音

将录制好的 `voiceover.mp3` 放入 `public/audio/`，然后在 Composition 中添加音频：

```tsx
import { Audio } from "remotion";
import voiceover from "../audio/voiceover.mp3";

// 在 AbsoluteFill 内添加
<Audio src={voiceover} />
```

### 第7步：渲染视频

```bash
# 渲染为 MP4
npx remotion render XiaoyaoBillPromo out/video.mp4

# 或使用 WebGL 渲染（更快）
npx remotion render XiaoyaoBillPromo out/video.mp4 --gl=angle
```

---

## 技术要点

### Remotion 最佳实践

1. **使用 interpolate 进行平滑动画**
```tsx
const opacity = interpolate(frame, [0, 30], [0, 1]);
```

2. **使用 spring 制作弹性效果**
```tsx
const scale = spring({ frame, fps: 30, config: { damping: 100 } });
```

3. **截图适配显示**
```tsx
<img
  src={image}
  style={{ width: 1400, height: 700, objectFit: 'contain' }}
/>
```

4. **时间管理**
- 每个场景都有明确的 startFrame 和 endFrame
- 使用 localFrame 计算相对时间

### Tailwind CSS 使用

```tsx
<div className="flex items-center justify-center bg-gradient-to-br from-purple-600 to-blue-600">
```

确保已配置 `@remotion/tailwind-v4`。

---

## 输出规格

| 参数 | 值 |
|------|-----|
| 格式 | MP4 (H.264) |
| 分辨率 | 1920x1080 |
| 帧率 | 30fps |
| 时长 | 90秒 |
| 音频 | AAC, 128kbps |

---

## 后续优化

1. **添加转场效果** - 场景间添加淡入淡出或滑动转场
2. **字幕叠加** - 添加同步字幕
3. **进度指示** - 添加场景切换指示器
4. **响应式版本** - 制作竖屏版本（1080x1920）用于短视频平台

---

**文档维护**: dtsola
**创建日期**: 2026-02-20
**最后更新**: 2026-02-20
