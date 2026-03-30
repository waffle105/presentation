#!/usr/bin/env python3
"""
定时任务管理器

每天早上 7:30 自动执行：
1. 弹出对话框让用户选择心情和城市
2. 5分钟无响应则使用默认值
3. 生成天气角色图片

使用方法：
---------
方式1: 后台服务运行（推荐）
    python scheduler.py

方式2: cron 定时任务
    30 7 * * * cd /path/to/skill && python scheduled_task.py --interactive

方式3: 无对话框自动运行
    python scheduled_task.py --auto
"""

import schedule
import time
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from weather_character import WeatherCharacterSkill
from morning_dialog import show_morning_dialog, show_morning_dialog_auto


def job_morning_task():
    """
    早晨任务
    
    1. 弹出对话框（GUI 或命令行）
    2. 等待用户选择（5分钟超时）
    3. 执行生成任务
    """
    print("\n" + "=" * 60)
    print(f"⏰ 执行定时任务: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # 1. 弹出对话框，让用户选择
        print("\n📱 等待用户选择...")
        mood, city = show_morning_dialog()
        
        print(f"\n✅ 用户选择:")
        print(f"   心情: {mood}")
        print(f"   城市: {city}")
        
        # 2. 执行生成任务
        skill = WeatherCharacterSkill()
        result = skill.run(mood=mood, location=city)
        
        if result.success:
            print("\n✅ 任务完成!")
            print(f"   图片: {result.local_path}")
            print(f"   温度: {result.weather.temperature}°C")
            print(f"\n📤 推送消息:\n{result.message}")
        else:
            print(f"\n⚠️ 任务部分完成: {result.error}")
            if result.message:
                print(f"\n📤 推送消息:\n{result.message}")
            
    except Exception as e:
        print(f"\n❌ 任务失败: {e}")


def job_morning_task_auto():
    """
    早晨任务（自动模式，无对话框）
    """
    print("\n" + "=" * 60)
    print(f"⏰ 执行定时任务（自动模式）: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        mood, city = show_morning_dialog_auto()
        
        skill = WeatherCharacterSkill()
        result = skill.run(mood=mood, location=city)
        
        if result.success:
            print("\n✅ 任务完成!")
        else:
            print(f"\n⚠️ 任务部分完成: {result.error}")
            
    except Exception as e:
        print(f"\n❌ 任务失败: {e}")


def run_scheduler():
    """运行定时调度器"""
    print("=" * 60)
    print("🗓️ 天气角色定时任务管理器")
    print("=" * 60)
    print("\n📋 定时任务列表:")
    print("   • 每天 07:30 - 弹出对话框 → 生成天气角色")
    print("\n💡 提示:")
    print("   - 对话框弹出后5分钟无响应将使用默认设置")
    print("   - 默认心情: 开心")
    print("   - 默认城市: 常州")
    print("\n按 Ctrl+C 停止运行\n")
    
    # 设置定时任务
    schedule.every().day.at("07:30").do(job_morning_task)
    
    # 显示下次执行时间
    next_run = schedule.next_run()
    print(f"⏰ 下次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行循环
    while True:
        schedule.run_pending()
        time.sleep(60)


def run_once():
    """立即执行一次（测试用）"""
    print("=" * 60)
    print("🧪 测试模式 - 立即执行一次")
    print("=" * 60)
    
    job_morning_task()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="天气角色定时任务管理器")
    parser.add_argument("--test", action="store_true", help="立即执行一次（测试模式）")
    parser.add_argument("--auto", action="store_true", help="自动模式（无对话框）")
    parser.add_argument("--time", type=str, default="07:30", help="设置执行时间（格式: HH:MM）")
    
    args = parser.parse_args()
    
    if args.test:
        run_once()
    else:
        run_scheduler()
