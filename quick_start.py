#!/usr/bin/env python3
"""
快速使用指南 - 天气角色生成技能

这是一个交互式演示脚本，帮助你快速了解如何使用这个技能。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from weather_character import WeatherCharacterSkill

def main():
    print("=" * 70)
    print("🌤️ 天气角色生成技能 - 快速使用指南")
    print("=" * 70)
    
    print("\n【1. 基础使用】")
    print("-" * 70)
    print("""
from weather_character import WeatherCharacterSkill

skill = WeatherCharacterSkill()
result = skill.run()  # 默认: 心情=开心, 地点=常州
""")
    
    print("\n【2. 自定义参数】")
    print("-" * 70)
    print("""
# 指定心情和地点
result = skill.run(
    mood="兴奋",      # 心情：开心/平静/兴奋/忧郁/思考
    location="北京"    # 地点：任意城市
)
""")
    
    print("\n【3. 定时任务】")
    print("-" * 70)
    print("""
# 启动定时调度器（每天 7:30 执行）
python scheduler.py

# 测试模式（立即执行一次）
python scheduler.py --test

# 使用 cron（推荐生产环境）
# crontab -e
# 添加: 30 7 * * * cd /path/to/skill && python scheduled_task.py
""")
    
    print("\n【4. 命令行使用】")
    print("-" * 70)
    print("""
# 默认运行
python weather_character.py

# 交互模式
python weather_character.py --interactive

# 启动定时任务
python scheduler.py
""")
    
    print("\n【5. 现在演示一下？】")
    print("-" * 70)
    
    choice = input("是否立即演示？（y/n，默认 y）: ").strip().lower()
    
    if choice in ("", "y", "yes"):
        print("\n🚀 正在执行演示...\n")
        
        skill = WeatherCharacterSkill()
        
        # 获取天气并生成消息（不生成图片，节省时间）
        print("📍 获取常州天气...")
        weather = skill.get_weather("常州")
        
        print(f"   温度: {weather.temperature}°C")
        print(f"   天气: {weather.condition}")
        print(f"   湿度: {weather.humidity}%")
        
        # 生成推送消息
        message = weather.to_message()
        print(f"\n📤 推送消息:\n{message}")
    
    print("\n" + "=" * 70)
    print("✅ 使用指南演示完成！")
    print("=" * 70)
    
    print("\n📚 更多信息请查看 README.md 和 SKILL.md")


if __name__ == "__main__":
    main()
