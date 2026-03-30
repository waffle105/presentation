#!/usr/bin/env python3
"""
Weather Character Skill 使用指南

快速上手:
---------
1. 导入技能:
   from weather_character_skill import WeatherCharacterSkill
   
2. 创建实例:
   skill = WeatherCharacterSkill()

3. 运行（默认参数）:
   result = skill.run()
   
4. 检查结果:
   if result.success:
       print(f"图片保存到: {result.local_path}")
"""

from weather_character import WeatherCharacterSkill

print("=" * 60)
print("🌤️ Weather Character Skill 使用指南")
print("=" * 60)

print("\n【基础用法】")
print("-" * 60)

print("""
# 方式1: 默认运行（心情=开心，地点=常州）
skill = WeatherCharacterSkill()
result = skill.run()

# 方式2: 指定心情
result = skill.run(mood="兴奋")

# 方式3: 指定心情和地点
result = skill.run(mood="平静", location="北京")

# 方式4: 完整参数
result = skill.run(
    mood="思考",
    location="上海",
    output_filename="my_character.png"
)
""")

print("\n【可用心情】")
print("-" * 60)
print("  开心  😊  - 明朗微笑，阳光明媚")
print("  平静  😌  - 柔和目光，宁静温和")
print("  兴奋  🤩  - 开怀大笑，活力四射")
print("  忧郁  😢  - 微微低落，阴天朦胧")
print("  思考  🤔  - 凝视远方，深沉氛围")

print("\n【温度穿搭示例】")
print("-" * 60)

skill = WeatherCharacterSkill()
test_temps = [35, 25, 16, 12, 0]

for temp in test_temps:
    outfit = skill.get_outfit_recommendation(temp)
    print(f"  {temp}°C: {outfit.description}")

print("\n【角色一致性】")
print("-" * 60)
print("  每次生成都参考 cankaotu.png")
print("  保持: 发型发色、眼睛眼镜、脸型体型、画风渲染")
print("  只改: 服装、表情、背景")

print("\n【命令行使用】")
print("-" * 60)
print("  cd skills/weather-character-skill")
print("  python run.py                    # 默认: 开心，常州")
print("  python run.py 兴奋 北京          # 自定义")
print("  python run.py --interactive      # 交互模式")

print("\n【测试】")
print("-" * 60)
print("  python test_skill.py             # 运行测试套件")
print("  python examples.py               # 运行示例代码")

print("\n" + "=" * 60)
print("✅ 默认参数: 心情='开心' | 地点='常州' | 参考图='cankaotu.png'")
print("=" * 60)
