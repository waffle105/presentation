#!/usr/bin/env python3
"""
Weather Character Skill 使用示例
"""

from weather_character import WeatherCharacterSkill

def example_default():
    """示例1: 默认参数运行（心情=开心，地点=常州）"""
    print("=" * 50)
    print("示例1: 默认参数")
    print("=" * 50)
    
    skill = WeatherCharacterSkill()
    result = skill.run()
    
    # 默认参数：
    # - mood: "开心" (DEFAULT_MOOD)
    # - location: "常州" (DEFAULT_LOCATION)
    # - 参考图: cankaotu.png
    
    print(f"心情: {result.mood}")
    print(f"温度: {result.weather.temperature}°C")
    print(f"穿搭: {result.outfit.description}")


def example_custom_mood():
    """示例2: 自定义心情"""
    print("\n" + "=" * 50)
    print("示例2: 自定义心情")
    print("=" * 50)
    
    skill = WeatherCharacterSkill()
    
    # 各种心情示例
    moods = ["开心", "兴奋", "平静", "思考", "忧郁"]
    
    for mood in moods:
        result = skill.run(mood=mood, location="上海")
        print(f"{mood}: {result.outfit.description}")


def example_custom_location():
    """示例3: 自定义地点"""
    print("\n" + "=" * 50)
    print("示例3: 自定义地点")
    print("=" * 50)
    
    skill = WeatherCharacterSkill()
    
    cities = ["北京", "上海", "广州", "成都", "哈尔滨"]
    
    for city in cities:
        result = skill.run(mood="开心", location=city)
        weather = result.weather
        print(f"{city}: {weather.temperature}°C, {weather.condition}")


def example_temperature_outfit():
    """示例4: 温度穿搭测试"""
    print("\n" + "=" * 50)
    print("示例4: 温度穿搭指南")
    print("=" * 50)
    
    skill = WeatherCharacterSkill()
    
    # 测试不同温度的穿搭建议
    test_temps = [5, 12, 16, 22, 28, 35]
    
    for temp in test_temps:
        outfit = skill.get_outfit_recommendation(temp)
        print(f"\n{temp}°C:")
        print(f"  上衣: {outfit.top}")
        print(f"  下装: {outfit.bottom}")
        print(f"  配饰: {outfit.accessories}")
        print(f"  描述: {outfit.description}")


def example_16_degrees():
    """示例5: 16°C穿搭专项测试"""
    print("\n" + "=" * 50)
    print("示例5: 16°C穿搭（单件卫衣，无需外套围巾）")
    print("=" * 50)
    
    skill = WeatherCharacterSkill()
    outfit = skill.get_outfit_recommendation(16)
    
    print(f"温度: 16°C")
    print(f"上衣: {outfit.top}")
    print(f"下装: {outfit.bottom}")
    print(f"配饰: {outfit.accessories}")
    print(f"描述: {outfit.description}")
    
    # 验证：16°C应该推荐单件卫衣，无需外套围巾
    assert "single hoodie" in outfit.top.lower() or "sweatshirt" in outfit.top.lower()
    assert "NO jacket" in outfit.description
    assert "NO scarf" in outfit.description
    print("\n✅ 验证通过: 16°C穿单件卫衣，无需外套围巾")


if __name__ == "__main__":
    # 运行所有示例
    example_default()
    example_custom_mood()
    example_custom_location()
    example_temperature_outfit()
    example_16_degrees()
    
    print("\n" + "=" * 50)
    print("✅ 所有示例运行完成!")
    print("=" * 50)
