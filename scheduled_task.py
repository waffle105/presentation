#!/usr/bin/env python3
"""
定时任务脚本 - 供 cron 调用

用途：
    由 cron 定时调用，执行天气角色生成任务
    
    执行流程：
    1. 弹出对话框让用户选择心情和城市
    2. 5分钟无响应则使用默认值
    3. 生成天气角色图片

使用：
    python scheduled_task.py              # 交互模式
    python scheduled_task.py --auto       # 自动模式（无对话框，使用默认值）
    python scheduled_task.py 开心 北京    # 指定参数
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from weather_character import WeatherCharacterSkill
from morning_dialog import show_morning_dialog


def main():
    """定时任务入口"""
    print("=" * 60)
    print(f"⏰ 天气角色定时任务")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 判断运行模式
    if len(sys.argv) > 1:
        if sys.argv[1] == "--auto":
            # 自动模式：使用默认值
            mood = "开心"
            city = "常州"
            print("\n🤖 自动模式: 使用默认设置")
        else:
            # 参数模式：使用命令行参数
            mood = sys.argv[1] if len(sys.argv) > 1 else "开心"
            city = sys.argv[2] if len(sys.argv) > 2 else "常州"
            print(f"\n📝 参数模式: 使用命令行参数")
    else:
        # 交互模式：弹出对话框
        print("\n📱 交互模式: 弹出对话框...")
        mood, city = show_morning_dialog()
    
    print(f"\n✅ 执行参数:")
    print(f"   心情: {mood}")
    print(f"   城市: {city}")
    
    # 执行任务
    skill = WeatherCharacterSkill()
    result = skill.run(mood=mood, location=city)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📋 执行结果:")
    print("-" * 60)
    
    if result.weather:
        print(f"✅ 天气获取成功")
        print(f"   温度: {result.weather.temperature}°C")
        print(f"   天气: {result.weather.condition}")
    
    if result.message:
        print(f"\n📤 推送消息:\n{result.message}")
    
    if result.local_path:
        print(f"\n✅ 角色图片: {result.local_path}")
    
    if result.error:
        print(f"\n⚠️ 错误: {result.error}")
    
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result.success else 1)
