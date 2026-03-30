"""
Weather Character Skill

天气角色生成技能

使用方式：
    from weather_character_skill import WeatherCharacterSkill
    
    skill = WeatherCharacterSkill()
    result = skill.run()  # 默认: 心情="开心", 地点="常州"
"""

from .weather_character import (
    WeatherCharacterSkill,
    Mood,
    WeatherInfo, 
    OutfitRecommendation,
    GenerationResult,
    interactive_run
)

__all__ = [
    'WeatherCharacterSkill',
    'Mood',
    'WeatherInfo', 
    'OutfitRecommendation',
    'GenerationResult',
    'interactive_run'
]

__version__ = '1.1.0'
__author__ = 'Weather Character Skill'

# 默认参数
DEFAULT_MOOD = "开心"
DEFAULT_LOCATION = "常州"
DEFAULT_REFERENCE_IMAGE = "cankaotu.png"
