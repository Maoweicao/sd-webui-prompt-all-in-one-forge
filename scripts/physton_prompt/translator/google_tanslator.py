import os
import sys
import requests

# 将父目录添加到Python路径中
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from translator.base_tanslator import BaseTranslator
from get_lang import get_lang


class GoogleTranslator(BaseTranslator):
    def __init__(self):
        super().__init__('google')

    def translate(self, text):
        if not text:
            return ''
        url = 'https://translation.googleapis.com/language/translate/v2/'
        api_key = self.api_config.get('api_key', '')
        
        # 检查是否需要API密钥
        if self.needs_api_key():
            if not api_key:
                raise Exception(get_lang('is_required', {'0': 'API Key'}))
        else:
            # 如果不需要API密钥，使用默认值
            if not api_key:
                api_key = "dummy-api-key"
        
        params = {
            'key': api_key,
            'q': text,
            'source': self.from_lang,
            'target': self.to_lang,
            'format': 'text'
        }
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        if 'error' in result:
            raise Exception(result['error']['message'])
        if 'data' not in result:
            raise Exception(get_lang('no_response_from', {'0': 'Google'}))
        if 'translations' not in result['data']:
            raise Exception(get_lang('no_response_from', {'0': 'Google'}))
        return result['data']['translations'][0]['translatedText']
