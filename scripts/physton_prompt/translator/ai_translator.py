import os
import sys
import json
import traceback

# 将父目录添加到Python路径中
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from translator.base_tanslator import BaseTranslator
from get_lang import get_lang


class AITranslator(BaseTranslator):
    """
    统一的 AI 翻译器，支持多种 AI 平台：
    - OpenAI
    - Deepseek
    - CherryIn
    - 硅基流动 (SiliconFlow)
    - 其他兼容 OpenAI API 的服务
    """
    
    # 预定义的 AI 平台配置
    PLATFORMS = {
        'openai': {
            'name': 'OpenAI',
            'api_base': 'https://api.openai.com/v1',
            'default_model': 'gpt-4o-mini'
        },
        'deepseek': {
            'name': 'Deepseek',
            'api_base': 'https://api.deepseek.com/v1',
            'default_model': 'deepseek-chat'
        },
        'cherryin': {
            'name': 'CherryIn',
            'api_base': 'https://open.cherryin.ai/v1',
            'default_model': 'gpt-4o-mini'
        },
        'siliconflow': {
            'name': '硅基流动',
            'api_base': 'https://api.siliconflow.cn/v1',
            'default_model': 'Qwen/Qwen2.5-7B-Instruct'
        },
        'custom': {
            'name': 'Custom',
            'api_base': '',
            'default_model': ''
        }
    }

    def __init__(self, api_key='ai_translate'):
        super().__init__(api_key)
        self.platform = 'openai'

    def set_platform(self, platform):
        """设置 AI 平台"""
        self.platform = platform
        return self

    def _get_client(self):
        """获取 OpenAI 兼容的客户端"""
        try:
            from openai import OpenAI
        except ImportError as e:
            error_msg = f"Failed to import OpenAI: {str(e)}\n{traceback.format_exc()}"
            raise Exception(error_msg)
        
        # 获取配置
        # 根据当前 API key 判断平台
        platform = self.platform
        if self.api == 'openai':
            platform = 'openai'
        elif self.api == 'deepseek':
            platform = 'deepseek'
        elif self.api == 'cherryin':
            platform = 'cherryin'
        elif self.api == 'siliconflow':
            platform = 'siliconflow'
        
        api_base = self.api_config.get('api_base', '')
        api_key = self.api_config.get('api_key', '')
        
        # 如果没有自定义 api_base，使用平台默认值
        if not api_base and platform in self.PLATFORMS:
            api_base = self.PLATFORMS[platform]['api_base']
        
        # 检查是否需要API密钥
        if self.needs_api_key():
            if not api_key:
                raise Exception(get_lang('is_required', {'0': 'API Key'}))
            
            if not api_base:
                raise Exception(get_lang('is_required', {'0': 'API Base'}))
        else:
            # 如果不需要API密钥，使用默认值或空值
            if not api_key:
                api_key = "dummy-key"
            if not api_base:
                api_base = self.PLATFORMS.get(platform, {}).get('api_base', '')
        
        return OpenAI(base_url=api_base, api_key=api_key)

    def _get_model(self):
        """获取模型名称"""
        model = self.api_config.get('model', '')
        if not model:
            # 根据当前 API key 判断平台
            platform = self.platform
            if self.api == 'openai':
                platform = 'openai'
            elif self.api == 'deepseek':
                platform = 'deepseek'
            elif self.api == 'cherryin':
                platform = 'cherryin'
            elif self.api == 'siliconflow':
                platform = 'siliconflow'
            
            if platform in self.PLATFORMS:
                model = self.PLATFORMS[platform]['default_model']
        return model or 'gpt-4o-mini'

    def translate(self, text):
        if not text:
            if isinstance(text, list):
                return []
            else:
                return ''
        
        client = self._get_client()
        model = self._get_model()
        
        body = []
        if isinstance(text, list):
            for item in text:
                body.append({'text': item})
        else:
            body.append({'text': text})

        body_str = json.dumps(body, ensure_ascii=False)

        messages = [
            {"role": "system", "content": "You are a translator assistant."},
            {
                "role": "user",
                "content": f"You are a translator assistant. Please translate the following JSON data to {self.to_lang}. Preserve the original format. Only return the translation result, without any additional content or annotations. If the prompt word is in the target language, please send it to me unchanged:\n{body_str}"
            },
        ]
        
        try:
            completion = client.chat.completions.create(
                model=model, 
                messages=messages, 
                timeout=60
            )
        except Exception as e:
            error_msg = f"AI API Error: {str(e)}\n{traceback.format_exc()}"
            raise Exception(error_msg)
        
        if len(completion.choices) == 0:
            platform_name = self.PLATFORMS.get(self.api_config.get('platform', 'openai'), {}).get('name', 'AI')
            raise Exception(get_lang('no_response_from', {'0': platform_name}))
        
        content = completion.choices[0].message.content
        
        try:
            # 找到第一个[，然后找到最后一个]，截取中间的内容
            start = content.index('[')
            end = content.rindex(']')
            if start == -1 or end == -1:
                raise Exception(get_lang('response_error', {'0': 'AI'}))
            result_json = '[' + content[start + 1:end] + ']'
            # 解析json
            result = json.loads(result_json)
            if isinstance(text, list):
                return [item['text'] for item in result]
            else:
                return result[0]['text']
        except Exception as e:
            raise Exception(get_lang('response_error', {'0': 'AI'}))

    def translate_batch(self, texts):
        return self.translate(texts)

    @staticmethod
    def get_models(api_base, api_key):
        """获取可用的模型列表"""
        try:
            from openai import OpenAI
        except ImportError as e:
            error_msg = f"Failed to import OpenAI: {str(e)}\n{traceback.format_exc()}"
            return {'success': False, 'message': error_msg, 'models': []}
        
        if not api_key:
            return {'success': False, 'message': 'API Key is required', 'models': []}
        
        if not api_base:
            return {'success': False, 'message': 'API Base is required', 'models': []}
        
        try:
            client = OpenAI(base_url=api_base, api_key=api_key)
            models_response = client.models.list()
            models = []
            for model in models_response.data:
                models.append({
                    'id': model.id,
                    'owned_by': getattr(model, 'owned_by', ''),
                    'created': getattr(model, 'created', 0)
                })
            # 按模型名称排序
            models.sort(key=lambda x: x['id'])
            return {'success': True, 'models': models}
        except Exception as e:
            error_msg = f"Failed to get models: {str(e)}\n{traceback.format_exc()}"
            return {'success': False, 'message': error_msg, 'models': []}
