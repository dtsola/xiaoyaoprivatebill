# 小遥账单助手 - 视频项目

> 使用 Remotion 制作的 120 秒产品宣传视频

---

## 当前状态

视频已完成开发，包含以下场景（120秒）：

| 场景 | 时间 | 内容 |
|------|------|------|
| 问题引入 | 0-10s | 黑底白字 |
| 解决方案 | 10-25s | Logo + 品牌标语 |
| 上传账单 | 25-33s | 截图展示 |
| 功能首页 | 33-41s | 截图展示 |
| 年度总览 | 41-49s | 截图展示 |
| 月度分析 | 49-57s | 截图展示 |
| 分类分析 | 57-65s | 截图展示 |
| 时间分析 | 65-73s | 截图展示 |
| 消费洞察1 | 73-81s | 截图展示 |
| 消费洞察2 | 81-89s | 截图展示 |
| 消费洞察3 | 89-97s | 截图展示 |
| 交易记录 | 97-105s | 截图展示 |
| 隐私说明 | 105-115s | 文字卡片 |
| 邀请试用 | 115-120s | Logo + GitHub |

---

## 添加配音

### 1. 录制配音

参考 [VOICEOVER_SCRIPT.md](VOICEOVER_SCRIPT.md) 获取完整配音脚本。

推荐录音软件：
- **Windows**: Audacity 或 系统录音机
- **Mac**: GarageBand 或 QuickTime Player
- **手机**: 语音备忘录

录音要求：
- 格式：MP3
- 比特率：128kbps
- 采样率：44.1kHz
- 声道：单声道
- 时长：约 120 秒

### 2. 放置配音文件

将录制的 `voiceover.mp3` 放入 `public/audio/` 目录：

```bash
# Windows
copy path\to\voiceover.mp3 public\audio\voiceover.mp3
```

---

## 预览视频

```bash
npm run dev
```

访问 http://localhost:4321

---

## 渲染视频

### 无配音版本

```bash
npx remotion render XiaoyaoBillPromo out/video.mp4
```

### 带配音版本

```bash
npx remotion render XiaoyaoBillPromo out/video.mp4 --audio=public/audio/voiceover.mp3
```

### 使用 WebGL 加速

```bash
npx remotion render XiaoyaoBillPromo out/video.mp4 --audio=public/audio/voiceover.mp3 --gl=angle
```

---

## 视频参数

| 参数 | 值 |
|------|-----|
| 分辨率 | 1920x1080 |
| 帧率 | 30fps |
| 时长 | 120秒 (3600帧) |
| 格式 | MP4 (H.264) |

---

## 项目结构

```
src/
├── Root.tsx              # Composition 配置
├── Composition.tsx       # 主视频组件
├── scenes/               # 场景组件
│   ├── ProblemScene.tsx          # 问题引入
│   ├── SolutionScene.tsx         # 解决方案
│   ├── DemoScene.tsx             # 截图展示
│   ├── PrivacyScene.tsx          # 隐私说明
│   └── CallToActionScene.tsx     # 邀请试用
└── screenshots/          # 截图资源
    ├── logo.png
    ├── upload.png
    ├── home.png
    ├── overview.png
    ├── monthly.png
    ├── category.png
    ├── time.png
    ├── insight.png
    ├── insight2.png
    ├── insight3.png
    └── records.png
```

---

## 相关文档

- [配音脚本](VOICEOVER_SCRIPT.md) - 完整配音文本
- [实施计划](IMPLEMENTATION_PLAN.md) - 技术实现方案
- [应用发布宣传视频脚本](../应用发布宣传视频脚本.md) - B站发布信息

---

## 发布到 B站

1. 渲染视频（带配音）
2. 上传到 B站
3. 使用标题：「我开发了一个隐私优先的账单分析工具，再也不用担心账单数据泄露」

视频标签：
```
开源项目,隐私保护,账单分析,Python,Vue,前端开发,后端开发,Docker,数据分析,个人财务
```

---

**Made with Remotion ❤️**
