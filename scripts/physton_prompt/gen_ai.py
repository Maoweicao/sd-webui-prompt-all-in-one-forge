import os
import sys

# 将当前目录添加到Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from get_lang import get_lang
from get_translate_apis import unprotected_translate_api_config
from translator.ai_translator import AITranslator


def gen_ai(messages, api_config, platform='openai'):
    """
    使用 AI 生成内容，支持多个平台
    
    Args:
        messages: 消息列表
        api_config: API 配置
        platform: AI 平台 (openai, deepseek, cherryin, siliconflow, custom_ai)
    
    Returns:
        生成的内容
    """
    api_config = unprotected_translate_api_config('ai_generate_key', api_config)
    
    if not messages or len(messages) == 0:
        raise Exception(get_lang('is_required', {'0': 'messages'}))
    
    try:
        from openai import OpenAI
    except ImportError:
        raise Exception(get_lang('package_not_found', {'0': 'openai'}))
    
    # 获取配置
    api_base = api_config.get('api_base', '')
    api_key = api_config.get('api_key', '')
    model = api_config.get('model', '')
    
    # 如果没有自定义 api_base，使用平台默认值
    if not api_base and platform in AITranslator.PLATFORMS:
        api_base = AITranslator.PLATFORMS[platform]['api_base']
    
    if not api_key:
        raise Exception(get_lang('is_required', {'0': 'API Key'}))
    
    if not api_base:
        raise Exception(get_lang('is_required', {'0': 'API Base'}))
    
    if not model:
        if platform in AITranslator.PLATFORMS:
            model = AITranslator.PLATFORMS[platform]['default_model']
        else:
            raise Exception(get_lang('is_required', {'0': 'Model'}))
    
    try:
        client = OpenAI(base_url=api_base, api_key=api_key)
        completion = client.chat.completions.create(
            model=model, 
            messages=messages, 
            timeout=60
        )
    except Exception as e:
        raise Exception(f"AI API Error: {str(e)}")
    
    if len(completion.choices) == 0:
        platform_name = AITranslator.PLATFORMS.get(platform, {}).get('name', 'AI')
        raise Exception(get_lang('no_response_from', {'0': platform_name}))
    
    content = completion.choices[0].message.content
    return content


def gen_openai(messages, api_config):
    """
    向后兼容的 OpenAI 生成函数
    """
    return gen_ai(messages, api_config, 'openai')
