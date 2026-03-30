# Weather Character Skill / 天气角色生成技能

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### Overview

A skill that generates weather-themed character images based on your mood, local weather, and city.

**Key Features:**
- 😊 **Mood → Expression**: Your mood determines the character's facial expression
- 🌤️ **Weather → Atmosphere**: Real-time weather determines the background
- 🏙️ **City → Scene**: 27 Chinese cities with unique landmarks
- 🎨 **Character Consistency**: Uses your reference image
- 🔌 **Multiple APIs**: Supports Coze, Volcengine, OpenAI, Stability AI

---

### ⚠️ API Configuration (IMPORTANT)

#### Supported Image APIs

| API | Description | Get API Key |
|-----|-------------|-------------|
| **Coze** (Default) | Coze AI Platform | [coze.cn](https://www.coze.cn/) / [coze.com](https://www.coze.com/) |
| **Volcengine** | 火山引擎/豆包/Seedance | [console.volcengine.com](https://console.volcengine.com/) |
| **OpenAI** | DALL-E | [platform.openai.com](https://platform.openai.com/) |
| **Stability AI** | Stable Diffusion | [platform.stability.ai](https://platform.stability.ai/) |

#### Configuration Steps

**Step 1: Install Dependencies**

```bash
pip install requests schedule
pip install coze-coding-dev-sdk  # For Coze API
# OR
pip install openai  # For OpenAI API
```

**Step 2: Configure API**

**Option A: Use Coze API (Default)**

```bash
# Set environment variables
export IMAGE_API_TYPE=coze
export COZE_API_KEY="your-coze-api-key"
```

**Option B: Use Volcengine (火山引擎/豆包/Seedance)**

```bash
# Set environment variables
export IMAGE_API_TYPE=volcengine
export VOLCENGINE_API_KEY="your-volcengine-api-key"
```

**Option C: Use OpenAI**

```bash
# Set environment variables
export IMAGE_API_TYPE=openai
export OPENAI_API_KEY="your-openai-api-key"
```

**Option D: Use Stability AI**

```bash
# Set environment variables
export IMAGE_API_TYPE=stability
export STABILITY_API_KEY="your-stability-api-key"
```

**Option E: Use .env File**

```bash
# Copy template
cp .env.example .env

# Edit .env file
IMAGE_API_TYPE=coze
COZE_API_KEY=your-api-key
```

#### Get API Keys

| Platform | URL | Notes |
|----------|-----|-------|
| Coze (China) | https://www.coze.cn/ | Recommended for Chinese users |
| Coze (Global) | https://www.coze.com/ | International users |
| Volcengine | https://console.volcengine.com/ | 豆包/Seedance models |
| OpenAI | https://platform.openai.com/ | DALL-E models |
| Stability AI | https://platform.stability.ai/ | Stable Diffusion |

---

### Quick Start

```bash
# 1. Install dependencies
pip install requests schedule coze-coding-dev-sdk

# 2. Configure API key
export COZE_API_KEY="your-api-key"

# 3. Run
python weather_character.py

# 4. Or start scheduled task
python scheduler.py
```

---

### Replace Reference Image

Simply replace `cankaotu.png` with your own character image!

**Tips:**
- PNG format, clear image
- Single character
- Face clearly visible

---

### Configuration

#### Default Values

| Parameter | Default | Location |
|-----------|---------|----------|
| `mood` | 开心 | `DEFAULT_MOOD` |
| `location` | 常州 | `DEFAULT_LOCATION` |
| `timeout` | 300s | `TIMEOUT` |
| `schedule_time` | 07:30 | `scheduler.py` |

#### Available Moods

开心 (Happy) | 平静 (Calm) | 兴奋 (Excited) | 忧郁 (Melancholy) | 思考 (Thoughtful)

#### Supported Cities (27)

常州, 北京, 上海, 广州, 深圳, 杭州, 成都, 西安, 南京, 苏州, 重庆, 武汉, 长沙, 天津, 青岛, 厦门, 大连, 哈尔滨, 昆明, 三亚, 拉萨, 桂林, 丽江, 香港, 澳门, 台北

---

### File Structure

```
weather-character-skill/
├── weather_character.py   # Core skill code
├── image_api.py           # Multi-API wrapper
├── morning_dialog.py      # Interactive dialog
├── scheduler.py           # Task scheduler
├── cankaotu.png           # Reference image (replace with yours!)
├── .env.example           # Environment config template
├── requirements.txt       # Dependencies
├── README.md              # This file
├── QUICKSTART.md          # Quick start guide
└── LICENSE                # MIT License
```

---

### Dependencies

| Package | Required | Purpose |
|---------|----------|---------|
| `requests` | ✅ | Weather API |
| `schedule` | ✅ | Scheduled tasks |
| `coze-coding-dev-sdk` | ✅ | Coze API (default) |
| `openai` | ❌ | OpenAI API (optional) |

---

### Troubleshooting

#### "API key not configured"
Set your API key:
```bash
export COZE_API_KEY="your-api-key"
# OR for Volcengine
export VOLCENGINE_API_KEY="your-api-key"
```

#### "Image generation failed"
1. Check API key is valid
2. Check API quota
3. Check network connection

#### Want to use a different API?
```bash
export IMAGE_API_TYPE=volcengine  # or openai, stability
export VOLCENGINE_API_KEY="your-key"
```

---

<a name="中文"></a>
## 中文

### 概述

根据心情、天气、城市生成天气主题角色图片的技能。

**核心功能：**
- 😊 **心情 → 表情**：心情决定角色表情
- 🌤️ **天气 → 氛围**：天气决定背景氛围
- 🏙️ **城市 → 场景**：27个中国城市地标
- 🎨 **角色一致性**：使用你的参考图
- 🔌 **多 API 支持**：支持 Coze、火山引擎、OpenAI、Stability AI

---

### ⚠️ API 配置（重要）

#### 支持的图片生成 API

| API | 说明 | 获取 API Key |
|-----|------|--------------|
| **Coze**（默认）| Coze AI 平台 | [coze.cn](https://www.coze.cn/) |
| **Volcengine** | 火山引擎/豆包/Seedance | [console.volcengine.com](https://console.volcengine.com/) |
| **OpenAI** | DALL-E | [platform.openai.com](https://platform.openai.com/) |
| **Stability AI** | Stable Diffusion | [platform.stability.ai](https://platform.stability.ai/) |

#### 配置步骤

**第一步：安装依赖**

```bash
pip install requests schedule
pip install coze-coding-dev-sdk  # Coze API
# 或
pip install openai  # OpenAI API
```

**第二步：配置 API**

**方式一：使用 Coze API（默认）**

```bash
export IMAGE_API_TYPE=coze
export COZE_API_KEY="你的Coze密钥"
```

**方式二：使用火山引擎（豆包/Seedance）**

```bash
export IMAGE_API_TYPE=volcengine
export VOLCENGINE_API_KEY="你的火山引擎密钥"
```

**方式三：使用 OpenAI**

```bash
export IMAGE_API_TYPE=openai
export OPENAI_API_KEY="你的OpenAI密钥"
```

**方式四：使用 .env 文件**

```bash
# 复制模板
cp .env.example .env

# 编辑 .env 文件
IMAGE_API_TYPE=coze
COZE_API_KEY=你的API密钥
```

#### 获取 API Key

| 平台 | 网址 | 说明 |
|------|------|------|
| 扣子（中国）| https://www.coze.cn/ | 推荐中国用户使用 |
| 扣子（国际）| https://www.coze.com/ | 国际用户 |
| 火山引擎 | https://console.volcengine.com/ | 豆包/Seedance 模型 |
| OpenAI | https://platform.openai.com/ | DALL-E 模型 |
| Stability AI | https://platform.stability.ai/ | Stable Diffusion |

---

### 快速开始

```bash
# 1. 安装依赖
pip install requests schedule coze-coding-dev-sdk

# 2. 配置 API Key
export COZE_API_KEY="你的API密钥"

# 3. 运行
python weather_character.py

# 4. 或启动定时任务
python scheduler.py
```

---

### 替换参考图片

将 `cankaotu.png` 替换为你自己的角色图片！

**提示：**
- PNG 格式，清晰图片
- 单个角色
- 面部清晰可见

---

### 依赖

| 包名 | 必需 | 用途 |
|------|------|------|
| `requests` | ✅ | 天气 API |
| `schedule` | ✅ | 定时任务 |
| `coze-coding-dev-sdk` | ✅ | Coze API（默认）|
| `openai` | ❌ | OpenAI API（可选）|

---

### 常见问题

#### "API key not configured"
设置你的 API Key：
```bash
export COZE_API_KEY="你的密钥"
# 或使用火山引擎
export VOLCENGINE_API_KEY="你的密钥"
```

#### "图片生成失败"
1. 检查 API Key 是否有效
2. 检查 API 配额
3. 检查网络连接

#### 如何切换 API？
```bash
export IMAGE_API_TYPE=volcengine  # 或 openai, stability
export VOLCENGINE_API_KEY="你的密钥"
```

---

### 许可证

MIT License

---

## ⚠️ Security Note / 安全提示

**NEVER commit your .env file to GitHub! / 永远不要将 .env 文件提交到 GitHub！**

The `.env` file contains your API keys and should be kept private.

`.env` 文件包含你的 API 密钥，应保持私密。

```
# .gitignore
.env
*.pem
*_api_key*
```
