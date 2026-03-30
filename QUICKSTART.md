# 快速入门指南 / Quick Start Guide

[English](#english-quick-start) | [中文](#中文快速入门)

---

<a name="english-quick-start"></a>
## English Quick Start

### Step 1: Install Dependencies

```bash
pip install requests schedule coze-coding-dev-sdk
```

### Step 2: Configure API Key (IMPORTANT)

This skill requires an API key for AI image generation.

```bash
# Set environment variable
export COZE_API_KEY="your-api-key-here"
```

**Get your API key:**
1. Visit [Coze Platform](https://www.coze.cn/) or [Coze Global](https://www.coze.com/)
2. Sign up / Sign in
3. Go to API Keys section
4. Create and copy your API key

### Step 3: Replace Reference Image (Optional)

Replace `cankaotu.png` with your own character image:

```
weather-character-skill/
└── cankaotu.png  ← Replace this with your character!
```

**Recommended:**
- PNG format, clear image
- Single character
- Face clearly visible

### Step 4: Run

```bash
# Quick test
python weather_character.py

# Or start daily task
python scheduler.py
```

### Step 5: Customize (Optional)

Edit `weather_character.py`:

```python
DEFAULT_MOOD = Mood.HAPPY      # Change default mood
DEFAULT_LOCATION = "常州"       # Change default city
```

---

<a name="中文快速入门"></a>
## 中文快速入门

### 第一步：安装依赖

```bash
pip install requests schedule coze-coding-dev-sdk
```

### 第二步：配置 API Key（重要）

本技能需要 API Key 进行 AI 图片生成。

```bash
# 设置环境变量
export COZE_API_KEY="你的API密钥"
```

**获取 API Key：**
1. 访问 [扣子平台](https://www.coze.cn/) 或 [Coze Global](https://www.coze.com/)
2. 注册/登录
3. 进入 API Keys 页面
4. 创建并复制你的 API Key

### 第三步：替换参考图片（可选）

将 `cankaotu.png` 替换为你自己的角色图片：

```
weather-character-skill/
└── cankaotu.png  ← 替换为你的角色！
```

**推荐：**
- PNG 格式，清晰图片
- 单个角色
- 面部清晰可见

### 第四步：运行

```bash
# 快速测试
python weather_character.py

# 或启动每日定时任务
python scheduler.py
```

### 第五步：自定义（可选）

编辑 `weather_character.py`：

```python
DEFAULT_MOOD = Mood.HAPPY      # 修改默认心情
DEFAULT_LOCATION = "常州"       # 修改默认城市
```

---

## API Configuration Summary / API 配置摘要

| Item | Description |
|------|-------------|
| SDK | `coze-coding-dev-sdk` |
| Env Variable | `COZE_API_KEY` |
| Get Key | [Coze Platform](https://www.coze.cn/) |

| 项目 | 说明 |
|------|------|
| SDK | `coze-coding-dev-sdk` |
| 环境变量 | `COZE_API_KEY` |
| 获取密钥 | [扣子平台](https://www.coze.cn/) |

---

## Output Example / 输出示例

```
早上好！今天是2026年03月30日，星期一。

📍 常州
🌡️ 气温：16°C（体感 16°C）
☁️ 天气：小雨
💧 湿度：86%
🌬️ 风力：东南风 14km/h

👕 气温适中，穿件单薄的卫衣或运动衫即可，无需外套围巾。

祝您今天心情愉快！😊
```

---

## Need Help? / 需要帮助？

See [README.md](README.md) for full documentation.

查看 [README.md](README.md) 获取完整文档。
