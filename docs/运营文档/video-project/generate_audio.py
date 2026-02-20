#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Edge TTS 生成小遥账单助手视频配音
"""

import asyncio
import edge_tts
import os

# 配音文本配置
VOICE_TEXTS = {
    "scene1_problem.mp3": "想要分析自己的消费账单，但不敢用第三方工具？因为担心数据上传、隐私泄露。",
    "scene2_solution.mp3": "所以我开发了这个工具——小遥账单助手。一个完全本地化的账单分析工具。数据不上传服务器，支持支付宝和微信账单。",
    "scene3a_upload.mp3": "拖拽上传，自动识别格式。支付宝 CSV、微信 CSV/XLSX 都支持。",
    "scene3b_home.mp3": "全能账单分析工具，支持支付宝和微信账单，4大功能卡片。",
    "scene3c_overview.mp3": "年度总览一目了然，收入支出清晰可见。",
    "scene3d_monthly.mp3": "月度收支趋势，环比同比分析。",
    "scene3e_category.mp3": "分类占比分析，钱花在哪一看便知。",
    "scene3f_time.mp3": "消费时间分布，发现消费规律。",
    "scene3ghi_insight.mp3": "高频商户分析，大额消费提醒。消费建议与优化，发现省钱机会。",
    "scene3j_records.mp3": "完整交易明细，支持多维度筛选。",
    "scene4_privacy.mp3": "所有数据都在本地处理，随时手动清除，隐私无忧。",
    "scene5_cta.mp3": "项目已在 GitHub 开源，完全免费使用。欢迎试用并给个Star支持。",
}

# 使用中文女声（自然度较高）
# 可选声音:
# - zh-CN-XiaoxiaoNeural (女声，自然)
# - zh-CN-YunxiNeural (男声，自然)
# - zh-CN-XiaoyiNeural (女声，温柔)
VOICE = "zh-CN-XiaoxiaoNeural"

# 语速 (0.5 ~ 2.0，默认为1.0)
RATE = "+0%"

# 音调/音高 (-50% ~ 100%，默认为0%，使用 Hz 格式)
PITCH = "+0Hz"

# 音量 (默认为0，范围-100~100，0为默认音量，增加正值增加音量)
VOLUME = "+0%"


async def generate_audio(filename, text, output_dir="public/audio"):
    """生成单个音频文件"""
    output_path = os.path.join(output_dir, filename)

    print(f"正在生成: {filename}")
    print(f"  文本: {text}")

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE,
        pitch=PITCH,
        volume=VOLUME
    )

    await communicate.save(output_path)
    print(f"  完成: {output_path}")


async def main():
    """生成所有配音文件"""
    print("=" * 60)
    print("小遥账单助手 - Edge TTS 配音生成")
    print("=" * 60)
    print(f"语音: {VOICE}")
    print(f"语速: {RATE}")
    print(f"音调: {PITCH}")
    print("-" * 60)

    # 确保输出目录存在
    os.makedirs("public/audio", exist_ok=True)

    # 逐个生成音频文件
    tasks = []
    for filename, text in VOICE_TEXTS.items():
        task = generate_audio(filename, text)
        tasks.append(task)

    await asyncio.gather(*tasks)

    print("-" * 60)
    print(f"✅ 所有配音文件已生成到 public/audio/")
    print(f"共生成 {len(VOICE_TEXTS)} 个音频文件")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
