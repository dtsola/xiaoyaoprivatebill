#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并小遥账单助手视频配音文件
"""

import os
import subprocess

# 音频文件列表（按顺序）- 优化后的时间轴
AUDIO_FILES = [
    ("scene1_problem.mp3", 0),        # 0s
    ("scene2_solution.mp3", 9),        # 9s
    ("scene3a_upload.mp3", 22),       # 22s
    ("scene3b_home.mp3", 31),        # 31s
    ("scene3c_overview.mp3", 39),     # 39s
    ("scene3d_monthly.mp3", 45),     # 45s
    ("scene3e_category.mp3", 51),     # 51s
    ("scene3f_time.mp3", 57),        # 57s
    ("scene3ghi_insight.mp3", 62),    # 62s
    ("scene3j_records.mp3", 70),     # 70s
    ("scene4_privacy.mp3", 74),     # 74s
    ("scene5_cta.mp3", 80),        # 80s
]

# 输出文件
OUTPUT_FILE = "voiceover.mp3"
AUDIO_DIR = "public/audio"
OUTPUT_PATH = os.path.join(AUDIO_DIR, OUTPUT_FILE)


def merge_audio_with_pydub():
    """使用 pydub 合并音频"""
    try:
        from pydub import AudioSegment
    except ImportError:
        print("安装 pydub...")
        subprocess.run(["pip", "install", "pydub"], check=True)
        from pydub import AudioSegment

    print("=" * 60)
    print("小遥账单助手 - 配音文件合并")
    print("=" * 60)
    print("正在使用 pydub 合并音频...")
    print("-" * 60)

    # 创建一个 90 秒的静音音频作为基础
    total_duration = 90  # 秒
    combined = AudioSegment.silent(duration=total_duration * 1000)

    for filename, delay_seconds in AUDIO_FILES:
        input_path = os.path.join(AUDIO_DIR, filename)
        delay_ms = delay_seconds * 1000

        print(f"  处理: {filename} (延迟 {delay_seconds}s)")

        # 加载音频
        audio = AudioSegment.from_mp3(input_path)

        # 在指定位置插入音频
        combined = combined.overlay(audio, position=delay_ms)

    # 确保输出目录存在
    os.makedirs(AUDIO_DIR, exist_ok=True)

    # 导出合并后的音频
    combined.export(OUTPUT_PATH, format="mp3", bitrate="128k")

    print("-" * 60)
    print(f"完成! 音频已保存到: {OUTPUT_PATH}")
    print(f"总时长: {len(combined) / 1000} 秒")
    print(f"文件大小: {os.path.getsize(OUTPUT_PATH) / 1024:.1f} KB")
    print("=" * 60)
    return True


def main():
    """主函数"""
    # 确保在正确的目录
    if os.path.exists("src/Composition.tsx"):
        # 在 video-project 目录
        pass

    # 尝试使用 pydub 合并音频
    merge_audio_with_pydub()


if __name__ == "__main__":
    main()
