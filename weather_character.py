#!/usr/bin/env python3
"""
Weather Character Skill - 天气角色生成技能

根据用户心情、所在地天气和参考风格，生成角色一致的人物图片。

核心设计原则：
- 心情决定表情
- 天气决定天气氛围
- 城市决定场景特色
- 三者独立结合

使用方式：
    from weather_character import WeatherCharacterSkill
    
    skill = WeatherCharacterSkill()
    result = skill.run()
"""

import requests
import os
import base64
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

# ============================================
# 数据模型
# ============================================

class Mood(Enum):
    """心情类型"""
    HAPPY = "开心"
    CALM = "平静"
    EXCITED = "兴奋"
    MELANCHOLY = "忧郁"
    THOUGHTFUL = "思考"


class WeatherType(Enum):
    """天气类型"""
    SUNNY = "晴天"
    CLOUDY = "多云"
    RAINY = "雨天"
    SNOWY = "雪天"
    FOGGY = "雾天"
    STORMY = "暴风雨"
    CLEAR = "晴朗"
    OVERCAST = "阴天"


@dataclass
class WeatherInfo:
    """天气信息"""
    temperature: int
    condition: str
    humidity: int
    wind_speed: int
    wind_direction: str
    feels_like: int
    city: str = ""
    
    def to_message(self) -> str:
        """转换为推送消息文本"""
        now = datetime.now()
        date_str = now.strftime("%Y年%m月%d日")
        weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
        
        outfit = self.get_outfit_suggestion()
        
        message = f"""早上好！今天是{date_str}，{weekday}。

📍 {self.city}
🌡️ 气温：{self.temperature}°C（体感 {self.feels_like}°C）
☁️ 天气：{self.condition}
💧 湿度：{self.humidity}%
🌬️ 风力：{self.wind_direction}风 {self.wind_speed}km/h

👕 {outfit}

祝您今天心情愉快！😊"""
        return message
    
    def get_outfit_suggestion(self) -> str:
        """获取穿搭建议"""
        temp = self.temperature
        
        if temp >= 30:
            return "天气炎热，建议穿短袖短裤，注意防晒防暑。"
        elif temp >= 25:
            return "天气温暖，短袖衬衫配休闲裤，舒适出行。"
        elif temp >= 20:
            return "天气舒适，长袖T恤配牛仔裤刚刚好。"
        elif temp >= 15:
            return "气温适中，穿件单薄的卫衣或运动衫即可，无需外套围巾。"
        elif temp >= 10:
            return "气温稍凉，建议薄外套配薄毛衣，可带条薄围巾备用。"
        elif temp >= 5:
            return "天气偏冷，暖外套加毛衣，出门记得围巾保暖。"
        else:
            return "天气寒冷，穿上冬季大衣，围巾手套帽子一个都别少。"
    
    def get_weather_type(self) -> WeatherType:
        """根据天气状况判断天气类型"""
        condition_lower = self.condition.lower()
        
        rainy_keywords = ['rain', 'drizzle', 'shower', 'thunder', 'storm', '雨', '阵雨', '雷']
        for kw in rainy_keywords:
            if kw in condition_lower:
                return WeatherType.RAINY
        
        snowy_keywords = ['snow', 'blizzard', 'sleet', '雪', '暴风雪']
        for kw in snowy_keywords:
            if kw in condition_lower:
                return WeatherType.SNOWY
        
        foggy_keywords = ['fog', 'mist', 'haze', '雾', '霾']
        for kw in foggy_keywords:
            if kw in condition_lower:
                return WeatherType.FOGGY
        
        overcast_keywords = ['overcast', '阴', '阴天']
        for kw in overcast_keywords:
            if kw in condition_lower:
                return WeatherType.OVERCAST
        
        cloudy_keywords = ['cloudy', '多云']
        for kw in cloudy_keywords:
            if kw in condition_lower:
                return WeatherType.CLOUDY
        
        sunny_keywords = ['sunny', 'clear', '晴', '晴朗']
        for kw in sunny_keywords:
            if kw in condition_lower:
                return WeatherType.SUNNY
        
        return WeatherType.CLOUDY


@dataclass
class OutfitRecommendation:
    """穿搭建议"""
    top: str
    bottom: str
    accessories: str
    description: str


@dataclass
class GenerationResult:
    """生成结果"""
    success: bool
    image_url: Optional[str] = None
    local_path: Optional[str] = None
    weather: Optional[WeatherInfo] = None
    outfit: Optional[OutfitRecommendation] = None
    mood: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None


# ============================================
# 城市场景配置
# ============================================

CITY_SCENES = {
    # 江苏
    "常州": {
        "landmarks": "Changzhou Dinosaur Park, Tianning Temple, modern city skyline",
        "description": "Changzhou city scene with dinosaur park elements or Tianning Temple pagoda in the background, modern Chinese city atmosphere",
        "style": "modern Chinese city with traditional elements"
    },
    "南京": {
        "landmarks": "Nanjing City Wall, Confucius Temple, Qinhuai River, Purple Mountain",
        "description": "Nanjing historic city scene with ancient city wall or Qinhuai River, traditional Chinese architecture",
        "style": "historic Chinese city with classical architecture"
    },
    "苏州": {
        "landmarks": "classical gardens, canals, traditional bridges, Humble Administrator's Garden",
        "description": "Suzhou classical garden scene with traditional pavilions, stone bridges over canals, elegant Chinese landscape",
        "style": "classical Chinese garden and water town"
    },
    "无锡": {
        "landmarks": "Taihu Lake, Lingshan Grand Buddha, Yuantouzhu",
        "description": "Wuxi scenic scene with Taihu Lake view or Lingshan Buddha, beautiful Jiangnan water scenery",
        "style": "scenic Jiangnan water region"
    },
    
    # 一线城市
    "北京": {
        "landmarks": "Forbidden City, Great Wall, Temple of Heaven, traditional hutongs",
        "description": "Beijing historic scene with Forbidden City red walls, traditional hutong alleyways, or Great Wall in distance",
        "style": "imperial Chinese capital with traditional architecture"
    },
    "上海": {
        "landmarks": "the Bund, Oriental Pearl Tower, Shanghai Tower, Huangpu River",
        "description": "Shanghai modern skyline scene with the Bund's colonial buildings or Pudong skyscrapers across Huangpu River",
        "style": "modern international metropolis skyline"
    },
    "广州": {
        "landmarks": "Canton Tower, Shamian Island, traditional Lingnan architecture",
        "description": "Guangzhou city scene with Canton Tower or traditional Lingnan style buildings, subtropical city atmosphere",
        "style": "modern Lingnan city with subtropical vibe"
    },
    "深圳": {
        "landmarks": "Ping An Finance Center, modern skyscrapers, Shenzhen Bay",
        "description": "Shenzhen modern tech city scene with futuristic skyline and green parks, innovative city atmosphere",
        "style": "modern tech metropolis"
    },
    
    # 其他城市
    "杭州": {
        "landmarks": "West Lake, Leifeng Pagoda, Broken Bridge, willow trees",
        "description": "Hangzhou scenic scene with beautiful West Lake, traditional pagodas, weeping willows by the water",
        "style": "romantic Chinese landscape with lake and gardens"
    },
    "成都": {
        "landmarks": "giant pandas, Wide and Narrow Alleys, Jinli ancient street",
        "description": "Chengdu relaxed city scene with panda elements or traditional Sichuan architecture, leisurely atmosphere",
        "style": "relaxed Sichuan city with panda theme"
    },
    "西安": {
        "landmarks": "Terracotta Warriors, Ancient City Wall, Big Wild Goose Pagoda",
        "description": "Xi'an ancient capital scene with historic city wall or traditional Tang dynasty architecture",
        "style": "ancient Chinese capital with historic grandeur"
    },
    "重庆": {
        "landmarks": "mountain city terrain, Yangtze River, Jiefangbei, Hongya Cave",
        "description": "Chongqing mountain city scene with dramatic hillside buildings, river views, unique 3D cityscape",
        "style": "dramatic mountain city with layered architecture"
    },
    "武汉": {
        "landmarks": "Yellow Crane Tower, Yangtze River Bridge, East Lake",
        "description": "Wuhan city scene with iconic Yellow Crane Tower or Yangtze River bridge, central China metropolis",
        "style": "central Chinese city with historic landmarks"
    },
    "长沙": {
        "landmarks": "Orange Isle, Yuelu Academy, IFS Tower",
        "description": "Changsha city scene with Orange Isle statue or modern downtown, vibrant entertainment city",
        "style": "vibrant entertainment city"
    },
    "天津": {
        "landmarks": "Tianjin Eye, Italian Style Town, Ancient Culture Street",
        "description": "Tianjin city scene with giant Ferris wheel or blend of Western and Chinese architecture",
        "style": "blend of Western and Chinese colonial style"
    },
    "青岛": {
        "landmarks": "beach, red-roofed German architecture, Zhan Qiao pier",
        "description": "Qingdao coastal city scene with beaches, red-roofed colonial buildings, ocean view",
        "style": "coastal city with European colonial charm"
    },
    "厦门": {
        "landmarks": "Gulangyu Island, Nanputuo Temple, beachfront",
        "description": "Xiamen seaside scene with Gulangyu colonial architecture or beautiful beach, subtropical island vibe",
        "style": "tropical seaside city"
    },
    "大连": {
        "landmarks": "Xinghai Square, seaside promenade, Russian architecture",
        "description": "Dalian coastal city scene with seaside squares, beaches, and unique architecture",
        "style": "northern coastal city"
    },
    "哈尔滨": {
        "landmarks": "Saint Sophia Cathedral, Ice and Snow World, Central Street",
        "description": "Harbin winter scene with Russian-style architecture or ice festival elements, snowy atmosphere",
        "style": "winter city with Russian influence"
    },
    "昆明": {
        "landmarks": "Dianchi Lake, Western Hills, flower gardens",
        "description": "Kunming spring city scene with beautiful flowers, lake views, eternal spring atmosphere",
        "style": "eternal spring city with flowers"
    },
    "三亚": {
        "landmarks": "tropical beach, palm trees, blue ocean",
        "description": "Sanya tropical paradise scene with pristine beaches, palm trees, crystal clear water",
        "style": "tropical beach paradise"
    },
    "拉萨": {
        "landmarks": "Potala Palace, Jokhang Temple, blue sky",
        "description": "Lhasa sacred city scene with magnificent Potala Palace against pure blue sky, Tibetan atmosphere",
        "style": "sacred Tibetan city with Buddhist architecture"
    },
    "桂林": {
        "landmarks": "karst mountains, Li River, traditional villages",
        "description": "Guilin scenic landscape with dramatic karst peaks, Li River, traditional Chinese landscape painting style",
        "style": "iconic Chinese landscape painting scenery"
    },
    "丽江": {
        "landmarks": "ancient town, Snow Mountain, traditional Naxi architecture",
        "description": "Lijiang ancient town scene with cobblestone streets, traditional wooden buildings, mountain backdrop",
        "style": "ancient town with ethnic minority culture"
    },
    "香港": {
        "landmarks": "Victoria Harbour, Peak Tower, dense skyscrapers",
        "description": "Hong Kong iconic harbor scene with stunning skyline, Victoria Peak, dense urban landscape",
        "style": "dense international harbor city"
    },
    "澳门": {
        "landmarks": "Ruins of St. Paul's, casino resorts, Portuguese architecture",
        "description": "Macau scene with historic Portuguese buildings or modern casino skyline, East-West blend",
        "style": "blend of Portuguese and Chinese heritage"
    },
    "台北": {
        "landmarks": "Taipei 101, traditional temples, night markets",
        "description": "Taipei city scene with iconic Taipei 101 tower or traditional temples, modern Asian city",
        "style": "modern Asian city with traditional elements"
    },
}

# 默认通用场景
DEFAULT_SCENE = {
    "landmarks": "modern city buildings, streets, urban landscape",
    "description": "modern city scene with typical urban environment",
    "style": "contemporary city atmosphere"
}


# ============================================
# 核心技能类
# ============================================

class WeatherCharacterSkill:
    """
    天气角色生成技能
    
    设计原则：
    - 心情 → 表情
    - 天气 → 天气氛围（光线、降水等）
    - 城市 → 场景特色（地标、风格）
    """
    
    DEFAULT_MOOD = Mood.HAPPY
    DEFAULT_LOCATION = "常州"
    LOCAL_REFERENCE_IMAGE = os.path.join(os.path.dirname(__file__), "cankaotu.png")
    
    CHARACTER_FEATURES = """
CHARACTER TO PRESERVE EXACTLY (from reference image):
- Same face, same head shape, same body proportions
- Same hair style and exact same hair color gradient
- Same eyes shape and color, same glasses
- Same art style and rendering quality
- Keep 100% identical character identity
"""
    
    # 心情 → 表情
    MOOD_EXPRESSION = {
        Mood.HAPPY: "bright cheerful smile, eyes curved happily, joyful expression",
        Mood.CALM: "peaceful relaxed face, soft gentle gaze, serene expression",
        Mood.EXCITED: "big bright smile, excited sparkling eyes, energetic pose",
        Mood.MELANCHOLY: "slightly downcast eyes, faint melancholic look, thoughtful expression",
        Mood.THOUGHTFUL: "distant contemplative gaze, slight tilt of head, deep in thought"
    }
    
    # 天气 → 天气氛围
    WEATHER_ATMOSPHERE = {
        WeatherType.SUNNY: {
            "sky": "bright blue sky with white fluffy clouds",
            "lighting": "warm golden sunlight, bright natural lighting",
            "weather_elements": "sunny day with clear visibility"
        },
        WeatherType.CLOUDY: {
            "sky": "partly cloudy sky with soft white clouds",
            "lighting": "soft diffused sunlight through clouds",
            "weather_elements": "pleasant partly cloudy day"
        },
        WeatherType.OVERCAST: {
            "sky": "grey overcast sky with thick clouds",
            "lighting": "soft muted light, diffused through clouds",
            "weather_elements": "dim overcast day"
        },
        WeatherType.RAINY: {
            "sky": "grey rainy sky with dark clouds",
            "lighting": "soft dim light through rain clouds, cool ambient lighting",
            "weather_elements": "falling raindrops, wet surfaces, puddles on ground"
        },
        WeatherType.SNOWY: {
            "sky": "white-grey winter sky",
            "lighting": "soft white reflected light from snow",
            "weather_elements": "falling snowflakes, snow-covered ground, winter atmosphere"
        },
        WeatherType.FOGGY: {
            "sky": "foggy misty sky with limited visibility",
            "lighting": "soft diffused light through fog, ethereal lighting",
            "weather_elements": "dense fog, misty atmosphere, mysterious mood"
        },
        WeatherType.STORMY: {
            "sky": "dramatic dark stormy sky",
            "lighting": "dramatic contrast lighting, dark and moody",
            "weather_elements": "strong winds, heavy rain or approaching storm"
        },
        WeatherType.CLEAR: {
            "sky": "clear pleasant sky",
            "lighting": "natural balanced lighting",
            "weather_elements": "pleasant clear weather"
        }
    }
    
    # 温度穿搭
    TEMPERATURE_OUTFITS = {
        (30, 50): OutfitRecommendation(
            top="short-sleeve T-shirt or tank top",
            bottom="shorts or light skirt",
            accessories="sunglasses, sun hat",
            description="light summer outfit"
        ),
        (25, 30): OutfitRecommendation(
            top="short-sleeve shirt or thin top",
            bottom="light pants or shorts",
            accessories="optional hat",
            description="warm weather outfit"
        ),
        (20, 25): OutfitRecommendation(
            top="long-sleeve T-shirt or thin shirt",
            bottom="casual pants or jeans",
            accessories="none needed",
            description="comfortable outfit"
        ),
        (15, 20): OutfitRecommendation(
            top="single hoodie or sweatshirt",
            bottom="jeans or casual pants",
            accessories="none needed",
            description="single hoodie - NO jacket, NO scarf"
        ),
        (10, 15): OutfitRecommendation(
            top="light jacket over thin sweater",
            bottom="pants or jeans",
            accessories="optional light scarf",
            description="light jacket over inner layer"
        ),
        (5, 10): OutfitRecommendation(
            top="warm jacket over sweater",
            bottom="warm pants",
            accessories="scarf recommended",
            description="warm layered outfit"
        ),
        (-30, 5): OutfitRecommendation(
            top="winter coat over thick sweater",
            bottom="thick warm pants",
            accessories="scarf, gloves, beanie hat",
            description="warm winter outfit"
        )
    }
    
    def __init__(self):
        self.weather_info: Optional[WeatherInfo] = None
        self.outfit: Optional[OutfitRecommendation] = None
        self._reference_image_url: Optional[str] = None
        
    def _get_reference_image_url(self) -> str:
        if self._reference_image_url:
            return self._reference_image_url
            
        if os.path.exists(self.LOCAL_REFERENCE_IMAGE):
            with open(self.LOCAL_REFERENCE_IMAGE, "rb") as f:
                img_data = f.read()
            b64_data = base64.b64encode(img_data).decode('utf-8')
            data_uri = f"data:image/png;base64,{b64_data}"
            self._reference_image_url = data_uri
            return data_uri
        else:
            raise FileNotFoundError(f"参考图片不存在: {self.LOCAL_REFERENCE_IMAGE}")
    
    def get_weather(self, location: str = "常州") -> WeatherInfo:
        try:
            url = f"https://wttr.in/{location}?format=j1"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            current = data['current_condition'][0]
            
            return WeatherInfo(
                temperature=int(current['temp_C']),
                condition=current['weatherDesc'][0]['value'],
                humidity=int(current['humidity']),
                wind_speed=int(current['windspeedKmph']),
                wind_direction=current['winddir16Point'],
                feels_like=int(current['FeelsLikeC']),
                city=location
            )
        except Exception as e:
            print(f"⚠️ 获取天气失败: {e}")
            return WeatherInfo(
                temperature=20,
                condition="晴",
                humidity=60,
                wind_speed=5,
                wind_direction="N",
                feels_like=20,
                city=location
            )
    
    def get_city_scene(self, city: str) -> dict:
        """获取城市场景配置"""
        return CITY_SCENES.get(city, DEFAULT_SCENE)
    
    def get_outfit_recommendation(self, temp: int) -> OutfitRecommendation:
        for (low, high), outfit in self.TEMPERATURE_OUTFITS.items():
            if low <= temp < high:
                return outfit
        return self.TEMPERATURE_OUTFITS[(15, 20)]
    
    def build_prompt(self, weather: WeatherInfo, outfit: OutfitRecommendation, mood: Mood) -> str:
        """
        构建提示词
        
        三要素：
        - 心情 → 表情
        - 天气 → 天气氛围
        - 城市 → 场景特色
        """
        # 获取表情（心情决定）
        expression = self.MOOD_EXPRESSION[mood]
        
        # 获取天气氛围（天气决定）
        weather_type = weather.get_weather_type()
        atmosphere = self.WEATHER_ATMOSPHERE[weather_type]
        
        # 获取城市场景（城市决定）
        city_scene = self.get_city_scene(weather.city)
        
        prompt = f"""
{self.CHARACTER_FEATURES}

========================================
CITY SCENE: {weather.city}
========================================
- Landmarks: {city_scene['landmarks']}
- Scene: {city_scene['description']}
- Style: {city_scene['style']}

IMPORTANT: The background MUST show {weather.city} city characteristics.
Include recognizable landmarks or typical scenery of {weather.city}.

========================================
WEATHER ATMOSPHERE: {weather.condition} ({weather_type.value})
========================================
- Sky: {atmosphere['sky']}
- Lighting: {atmosphere['lighting']}
- Weather elements: {atmosphere['weather_elements']}

IMPORTANT: The weather MUST authentically show {weather.condition}.
- If RAINING: show falling rain, wet surfaces, puddles, grey sky
- If SUNNY: show bright sunlight, blue sky, clear visibility
- If CLOUDY: show diffused light, soft shadows
- NEVER add conflicting elements (no sun in rain, no rain in sun)

========================================
CHARACTER EXPRESSION: {mood.value}
========================================
- Expression: {expression}
- The character shows {mood.value} mood through facial expression
- Body language should be natural and relaxed

========================================
OUTFIT: Appropriate for {weather.temperature}°C
========================================
- Top: {outfit.top}
- Bottom: {outfit.bottom}
- Accessories: {outfit.accessories if outfit.accessories != "none needed" else "None"}

========================================
CRITICAL REQUIREMENTS
========================================
1. Keep EXACT same character from reference
2. Background shows {weather.city} landmarks/scenery
3. Weather authentically shows {weather.condition}
4. Expression shows {mood.value} mood
5. Outfit matches {weather.temperature}°C temperature
6. DO NOT add conflicting weather elements
7. Same art style as reference
8. Square 1:1 format
"""
        return prompt.strip()
    
    def generate_image(self, prompt: str, reference_image: str) -> tuple:
        """
        生成图片
        
        支持多种 API：
        - Coze API（默认）
        - 火山引擎 / 豆包 / Seedance
        - OpenAI DALL-E
        - Stability AI
        
        通过环境变量 IMAGE_API_TYPE 配置
        """
        try:
            from image_api import ImageGenerator
            
            generator = ImageGenerator()
            return generator.generate(prompt, reference_image, size="1024x1024")
            
        except ImportError:
            # 回退到默认的 Coze SDK
            try:
                from coze_coding_dev_sdk import ImageGenerationClient
                from coze_coding_utils.runtime_ctx.context import new_context
                
                ctx = new_context(method="generate")
                client = ImageGenerationClient(ctx=ctx)
                
                response = client.generate(
                    prompt=prompt,
                    image=reference_image,
                    size="1024x1024",
                    watermark=False
                )
                
                if response.success:
                    return True, response.image_urls[0]
                else:
                    return False, str(response.error_messages)
                    
            except Exception as e:
                return False, str(e)
    
    def download_image(self, url: str, filename: str) -> bool:
        try:
            response = requests.get(url, timeout=30)
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            print(f"⚠️ 下载失败: {e}")
            return False
    
    def run(
        self,
        mood: str = "开心",
        location: str = "常州",
        output_filename: str = "weather_character_output.png"
    ) -> GenerationResult:
        """运行技能"""
        print("=" * 60)
        print("🌤️ Weather Character Skill")
        print("=" * 60)
        
        # 1. 解析心情
        mood_map = {
            "开心": Mood.HAPPY,
            "平静": Mood.CALM,
            "兴奋": Mood.EXCITED,
            "忧郁": Mood.MELANCHOLY,
            "思考": Mood.THOUGHTFUL
        }
        parsed_mood = mood_map.get(mood, Mood.HAPPY)
        print(f"\n😊 心情: {parsed_mood.value} → 表情")
        
        # 2. 获取天气
        print(f"📍 地点: {location}")
        self.weather_info = self.get_weather(location)
        
        weather_type = self.weather_info.get_weather_type()
        print(f"🌡️ 天气: {self.weather_info.temperature}°C, {self.weather_info.condition}")
        print(f"☁️ 天气类型: {weather_type.value} → 天气氛围")
        
        # 3. 获取城市场景
        city_scene = self.get_city_scene(location)
        print(f"🏙️ 城市: {location} → 场景特色")
        print(f"   地标: {city_scene['landmarks'][:50]}...")
        
        # 4. 获取穿搭
        self.outfit = self.get_outfit_recommendation(self.weather_info.temperature)
        print(f"👕 穿搭: {self.outfit.description}")
        
        # 5. 生成推送消息
        message = self.weather_info.to_message()
        print(f"\n📝 推送内容:\n{message}")
        
        # 6. 获取参考图
        print(f"\n📷 参考图片: cankaotu.png")
        ref_image = self._get_reference_image_url()
        
        # 7. 构建提示词
        prompt = self.build_prompt(
            weather=self.weather_info,
            outfit=self.outfit,
            mood=parsed_mood
        )
        
        # 8. 生成图片
        print(f"\n🚀 生成图片中...")
        print(f"   表情: {parsed_mood.value} (心情)")
        print(f"   天气: {weather_type.value} (天气)")
        print(f"   场景: {location} (城市)")
        
        success, result = self.generate_image(prompt, ref_image)
        
        if success:
            print(f"✅ 生成成功!")
            print(f"   URL: {result}")
            
            output_path = os.path.join(os.path.dirname(__file__), output_filename)
            if self.download_image(result, output_path):
                print(f"✅ 已保存: {output_path}")
            
            return GenerationResult(
                success=True,
                image_url=result,
                local_path=output_path,
                weather=self.weather_info,
                outfit=self.outfit,
                mood=parsed_mood.value,
                message=message
            )
        else:
            print(f"❌ 生成失败: {result}")
            return GenerationResult(
                success=False,
                weather=self.weather_info,
                message=message,
                error=result
            )


def interactive_run():
    """交互式运行"""
    print("\n" + "=" * 60)
    print("🎭 欢迎使用 Weather Character Skill!")
    print("=" * 60)
    
    print("\n请选择心情：")
    print("  1. 开心 😊")
    print("  2. 平静 😌")
    print("  3. 兴奋 🤩")
    print("  4. 忧郁 😢")
    print("  5. 思考 🤔")
    
    mood_input = input("\n心情 [默认: 1-开心]: ").strip()
    mood_map = {"1": "开心", "2": "平静", "3": "兴奋", "4": "忧郁", "5": "思考"}
    mood = mood_map.get(mood_input, "开心")
    
    location_input = input("地点 [默认: 常州]: ").strip()
    location = location_input if location_input else "常州"
    
    skill = WeatherCharacterSkill()
    result = skill.run(mood=mood, location=location)
    
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_run()
    else:
        skill = WeatherCharacterSkill()
        result = skill.run()
        
        if result.success:
            print(f"\n🎉 完成! 图片已保存到: {result.local_path}")
            print(f"\n📤 推送消息:\n{result.message}")
        else:
            print(f"\n😢 失败: {result.error}")
            if result.message:
                print(f"\n📤 推送消息:\n{result.message}")
