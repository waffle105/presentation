#!/usr/bin/env python3
"""
Weather Character Skill 测试脚本

测试内容：
1. 默认参数验证
2. 温度穿搭逻辑
3. 心情映射
4. 提示词生成
5. 参考图存在性
"""

from weather_character import WeatherCharacterSkill, Mood
import os

def test_default_parameters():
    """测试1: 默认参数"""
    print("\n" + "=" * 60)
    print("测试1: 默认参数验证")
    print("=" * 60)
    
    skill = WeatherCharacterSkill()
    
    # 检查默认心情
    assert skill.DEFAULT_MOOD == Mood.HAPPY, "默认心情应该是HAPPY"
    print(f"✅ 默认心情: {skill.DEFAULT_MOOD.value}")
    
    # 检查默认地点
    assert skill.DEFAULT_LOCATION == "常州", "默认地点应该是常州"
    print(f"✅ 默认地点: {skill.DEFAULT_LOCATION}")
    
    # 检查参考图路径
    assert "cankaotu.png" in skill.LOCAL_REFERENCE_IMAGE, "参考图应该是cankaotu.png"
    print(f"✅ 参考图路径: {skill.LOCAL_REFERENCE_IMAGE}")
    
    # 检查参考图文件存在
    assert os.path.exists(skill.LOCAL_REFERENCE_IMAGE), "参考图文件应该存在"
    print(f"✅ 参考图存在: {os.path.basename(skill.LOCAL_REFERENCE_IMAGE)}")


def test_temperature_outfit():
    """测试2: 温度穿搭逻辑"""
    print("\n" + "=" * 60)
    print("测试2: 温度穿搭逻辑")
    print("=" * 60)
    
    skill = WeatherCharacterSkill()
    
    # 测试关键温度点
    test_cases = [
        (35, "短袖", "太阳镜"),
        (25, "短袖", "无需"),
        (16, "单件卫衣", "无需外套围巾"),
        (12, "薄外套", "可选薄围巾"),
        (0, "冬季大衣", "围巾手套"),
    ]
    
    for temp, expected_top, expected_accessory in test_cases:
        outfit = skill.get_outfit_recommendation(temp)
        print(f"\n{temp}°C:")
        print(f"  上衣: {outfit.top}")
        print(f"  配饰: {outfit.accessories}")
        
        # 特别验证16°C
        if temp == 16:
            assert "single hoodie" in outfit.top.lower() or "sweatshirt" in outfit.top.lower()
            assert "NO jacket" in outfit.description
            assert "NO scarf" in outfit.description
            print("  ✅ 16°C验证通过: 单件卫衣，无需外套围巾")


def test_mood_mapping():
    """测试3: 心情映射"""
    print("\n" + "=" * 60)
    print("测试3: 心情映射")
    print("=" * 60)
    
    skill = WeatherCharacterSkill()
    
    # 测试所有心情
    for mood in Mood:
        config = skill.MOOD_CONFIG[mood]
        print(f"\n{mood.value}:")
        print(f"  表情: {config['expression'][:50]}...")
        print(f"  氛围: {config['atmosphere'][:50]}...")
        
        assert config['expression'], "表情不能为空"
        assert config['atmosphere'], "氛围不能为空"
    
    print("\n✅ 所有心情映射验证通过")


def test_prompt_generation():
    """测试4: 提示词生成"""
    print("\n" + "=" * 60)
    print("测试4: 提示词生成")
    print("=" * 60)
    
    skill = WeatherCharacterSkill()
    
    # 模拟天气和穿搭
    weather = skill.get_weather("常州")
    outfit = skill.get_outfit_recommendation(weather.temperature)
    mood = Mood.HAPPY
    
    # 生成提示词
    prompt = skill.build_prompt(weather, outfit, mood)
    
    # 验证提示词内容
    assert "CHARACTER TO PRESERVE" in prompt, "应包含角色保持指令"
    assert str(weather.temperature) in prompt, "应包含温度信息"
    assert mood.value in prompt, "应包含心情信息"
    assert outfit.top in prompt, "应包含穿搭信息"
    
    print(f"✅ 提示词长度: {len(prompt)} 字符")
    print(f"✅ 包含角色保持指令")
    print(f"✅ 包含温度: {weather.temperature}°C")
    print(f"✅ 包含心情: {mood.value}")
    print(f"✅ 包含穿搭: {outfit.top}")


def test_weather_api():
    """测试5: 天气API"""
    print("\n" + "=" * 60)
    print("测试5: 天气API")
    print("=" * 60)
    
    skill = WeatherCharacterSkill()
    
    # 获取天气
    weather = skill.get_weather("常州")
    
    print(f"温度: {weather.temperature}°C")
    print(f"天气: {weather.condition}")
    print(f"湿度: {weather.humidity}%")
    print(f"风速: {weather.wind_speed} km/h")
    print(f"风向: {weather.wind_direction}")
    print(f"体感: {weather.feels_like}°C")
    
    assert -50 <= weather.temperature <= 60, "温度应在合理范围内"
    print("\n✅ 天气API调用成功")


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("🧪 Weather Character Skill 测试套件")
    print("=" * 60)
    
    try:
        test_default_parameters()
        test_temperature_outfit()
        test_mood_mapping()
        test_prompt_generation()
        test_weather_api()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过!")
        print("=" * 60)
        
        print("\n📋 总结:")
        print("  - 默认心情: 开心 😊")
        print("  - 默认地点: 常州")
        print("  - 参考图: cankaotu.png ✅")
        print("  - 16°C穿搭: 单件卫衣，无需外套围巾 ✅")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
