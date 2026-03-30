#!/usr/bin/env python3
"""
Image Generation API Wrapper
图片生成 API 包装器

支持多种 API：
- Coze API (默认)
- 火山引擎 / 豆包 / Seedance
- OpenAI DALL-E
- Stability AI
- 自定义 API
"""

import os
import requests
import base64
from typing import Optional, Tuple
from enum import Enum


class ImageAPI(Enum):
    """支持的图片生成 API"""
    COZE = "coze"
    VOLCENGINE = "volcengine"  # 火山引擎/豆包/Seedance
    OPENAI = "openai"
    STABILITY = "stability"
    CUSTOM = "custom"


class ImageGenerator:
    """
    图片生成器
    
    支持多种 API，通过环境变量配置
    """
    
    def __init__(self, api_type: Optional[str] = None):
        """
        初始化图片生成器
        
        Args:
            api_type: API 类型，默认从环境变量读取
        """
        # 从环境变量获取 API 类型
        self.api_type = api_type or os.getenv("IMAGE_API_TYPE", "coze")
        
        # 加载配置
        self._load_config()
    
    def _load_config(self):
        """加载 API 配置"""
        if self.api_type == ImageAPI.COZE.value:
            self.api_key = os.getenv("COZE_API_KEY", "")
            self.base_url = os.getenv("COZE_BASE_URL", "https://api.coze.cn")
            
        elif self.api_type == ImageAPI.VOLCENGINE.value:
            # 火山引擎 / 豆包 / Seedance
            self.api_key = os.getenv("VOLCENGINE_API_KEY", "")
            self.base_url = os.getenv("VOLCENGINE_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
            
        elif self.api_type == ImageAPI.OPENAI.value:
            self.api_key = os.getenv("OPENAI_API_KEY", "")
            self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            
        elif self.api_type == ImageAPI.STABILITY.value:
            self.api_key = os.getenv("STABILITY_API_KEY", "")
            self.base_url = os.getenv("STABILITY_BASE_URL", "https://api.stability.ai")
            
        else:
            # 自定义 API
            self.api_key = os.getenv("CUSTOM_IMAGE_API_KEY", "")
            self.base_url = os.getenv("CUSTOM_IMAGE_BASE_URL", "")
    
    def generate(
        self,
        prompt: str,
        reference_image: str,
        size: str = "1024x1024",
        **kwargs
    ) -> Tuple[bool, str]:
        """
        生成图片
        
        Args:
            prompt: 提示词
            reference_image: 参考图片（URL 或 base64 data URI）
            size: 图片尺寸
            **kwargs: 其他参数
            
        Returns:
            Tuple[bool, str]: (是否成功, 图片URL或错误信息)
        """
        if self.api_type == ImageAPI.COZE.value:
            return self._generate_coze(prompt, reference_image, size, **kwargs)
        elif self.api_type == ImageAPI.VOLCENGINE.value:
            return self._generate_volcengine(prompt, reference_image, size, **kwargs)
        elif self.api_type == ImageAPI.OPENAI.value:
            return self._generate_openai(prompt, reference_image, size, **kwargs)
        elif self.api_type == ImageAPI.STABILITY.value:
            return self._generate_stability(prompt, reference_image, size, **kwargs)
        else:
            return self._generate_custom(prompt, reference_image, size, **kwargs)
    
    def _generate_coze(self, prompt: str, reference_image: str, size: str, **kwargs) -> Tuple[bool, str]:
        """使用 Coze API 生成图片"""
        try:
            from coze_coding_dev_sdk import ImageGenerationClient
            from coze_coding_utils.runtime_ctx.context import new_context
            
            ctx = new_context(method="generate")
            client = ImageGenerationClient(ctx=ctx)
            
            response = client.generate(
                prompt=prompt,
                image=reference_image,
                size=size,
                watermark=False
            )
            
            if response.success:
                return True, response.image_urls[0]
            else:
                return False, str(response.error_messages)
                
        except ImportError:
            return False, "请安装 coze-coding-dev-sdk: pip install coze-coding-dev-sdk"
        except Exception as e:
            return False, str(e)
    
    def _generate_volcengine(self, prompt: str, reference_image: str, size: str, **kwargs) -> Tuple[bool, str]:
        """
        使用火山引擎 API 生成图片
        
        火山引擎图片生成 API 文档：
        https://www.volcengine.com/docs/6791/1347773
        
        支持的模型：
        - seedance-2.0 (豆包图片生成)
        """
        try:
            # 火山引擎 API 调用
            endpoint = f"{self.base_url}/images/generations"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 处理参考图片
            image_data = reference_image
            if reference_image.startswith("data:image"):
                # 已经是 data URI，直接使用
                pass
            elif reference_image.startswith("http"):
                # URL，需要先下载转 base64
                response = requests.get(reference_image, timeout=30)
                b64_data = base64.b64encode(response.content).decode('utf-8')
                image_data = f"data:image/png;base64,{b64_data}"
            
            payload = {
                "model": kwargs.get("model", "seedance-v3.5"),  # 火山引擎模型
                "prompt": prompt,
                "image": image_data,
                "size": size,
                "n": 1
            }
            
            response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    return True, data["data"][0].get("url", "")
                else:
                    return False, f"API 返回异常: {data}"
            else:
                return False, f"API 错误 ({response.status_code}): {response.text}"
                
        except Exception as e:
            return False, str(e)
    
    def _generate_openai(self, prompt: str, reference_image: str, size: str, **kwargs) -> Tuple[bool, str]:
        """使用 OpenAI DALL-E 生成图片"""
        try:
            import openai
            
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url if "OPENAI_BASE_URL" in os.environ else None
            )
            
            # DALL-E 3 的图片编辑 API
            # 注意：OpenAI 的图片编辑需要 PNG 格式的图片文件
            response = client.images.edit(
                model=kwargs.get("model", "dall-e-2"),
                image=reference_image,  # 需要 PNG 文件
                prompt=prompt,
                n=1,
                size=size
            )
            
            return True, response.data[0].url
            
        except ImportError:
            return False, "请安装 openai: pip install openai"
        except Exception as e:
            return False, str(e)
    
    def _generate_stability(self, prompt: str, reference_image: str, size: str, **kwargs) -> Tuple[bool, str]:
        """使用 Stability AI 生成图片"""
        try:
            # Stability AI API 调用
            endpoint = f"{self.base_url}/v1/generation/{kwargs.get('engine', 'stable-diffusion-xl-1024-v1-0')}/image-to-image"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 处理参考图片
            if reference_image.startswith("data:image"):
                # 提取 base64 部分
                b64_data = reference_image.split(",", 1)[1]
            else:
                b64_data = reference_image
            
            payload = {
                "init_image": b64_data,
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "image_strength": 0.35
            }
            
            response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if "artifacts" in data and len(data["artifacts"]) > 0:
                    return True, data["artifacts"][0].get("base64", "")  # 返回 base64
                else:
                    return False, f"API 返回异常: {data}"
            else:
                return False, f"API 错误 ({response.status_code}): {response.text}"
                
        except Exception as e:
            return False, str(e)
    
    def _generate_custom(self, prompt: str, reference_image: str, size: str, **kwargs) -> Tuple[bool, str]:
        """使用自定义 API 生成图片"""
        # 用户可以继承此类并重写此方法
        return False, "请配置自定义 API 或继承 ImageGenerator 类并重写 _generate_custom 方法"


# ============================================
# 使用示例
# ============================================

if __name__ == "__main__":
    # 示例：使用不同 API
    
    # 1. 使用 Coze API（默认）
    # export IMAGE_API_TYPE=coze
    # export COZE_API_KEY=your-key
    
    # 2. 使用火山引擎
    # export IMAGE_API_TYPE=volcengine
    # export VOLCENGINE_API_KEY=your-key
    
    # 3. 使用 OpenAI
    # export IMAGE_API_TYPE=openai
    # export OPENAI_API_KEY=your-key
    
    generator = ImageGenerator()
    print(f"当前 API 类型: {generator.api_type}")
    print(f"API Key 已配置: {'是' if generator.api_key else '否'}")
