#!/usr/bin/env python3
"""
快速运行 Weather Character Skill

默认参数：
- 心情: 开心
- 地点: 常州
- 参考图: cankaotu.png
"""

from weather_character import WeatherCharacterSkill, interactive_run
import sys

def main():
    # 检查是否使用交互模式
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        result = interactive_run()
    else:
        # 默认运行（心情=开心，地点=常州）
        skill = WeatherCharacterSkill()
        
        # 支持命令行参数覆盖
        mood = sys.argv[1] if len(sys.argv) > 1 else "开心"
        location = sys.argv[2] if len(sys.argv) > 2 else "常州"
        
        result = skill.run(mood=mood, location=location)
    
    return result

if __name__ == "__main__":
    result = main()
    
    print("\n" + "=" * 60)
    if result.success:
        print("✅ 生成成功!")
        print(f"   心情: {result.mood}")
        print(f"   温度: {result.weather.temperature}°C")
        print(f"   穿搭: {result.outfit.description}")
        print(f"   图片: {result.local_path}")
        print(f"\n📤 推送消息:\n{result.message}")
    else:
        print(f"❌ 生成失败: {result.error}")
        if result.message:
            print(f"\n📤 推送消息:\n{result.message}")
    print("=" * 60)
