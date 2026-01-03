import os
import sys
import requests

# 将父目录添加到Python路径中
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from translator.base_tanslator import BaseTranslator
from get_lang import get_lang


class DeeplTranslator(BaseTranslator):
    def __init__(self):
        super().__init__('deepl')

    def translate(self, text):
        if not text:
            if isinstance(text, list):
                return []
            else:
                return ''
        url = 'https://api-free.deepl.com/v2/translate'
        api_key = self.api_config.get('api_key', '')
        
        # 检查是否需要API密钥
        if self.needs_api_key():
            if not api_key:
                raise Exception(get_lang('is_required', {'0': 'API Key'}))
        else:
            # 如果不需要API密钥，使用默认值
            if not api_key:
                api_key = "dummy-api-key"
        
        headers = {"Authorization": f"DeepL-Auth-Key {api_key}"}
        data = {
            'text': text,
            'source_lang': self.from_lang,
            'target_lang': self.to_lang
        }

        response = requests.post(url, headers=headers, data=data, timeout=10)
        if response.status_code != 200:
            raise Exception(get_lang('request_error', {'0': 'DeepL'}))
        if not response.text:
            raise Exception(get_lang('response_is_empty', {'0': 'DeepL'}))
        result = response.json()
        if 'message' in result:
            raise Exception(result['message'])
        if 'translations' not in result:
            raise Exception(get_lang('no_response_from', {'0': 'DeepL'}))
        if isinstance(text, list):
            results = []
            for item in result['translations']:
                results.append(item['text'])
            return results
        else:
            return result['translations'][0]['text']

    def translate_batch(self, texts):
        return self.translate(texts)
