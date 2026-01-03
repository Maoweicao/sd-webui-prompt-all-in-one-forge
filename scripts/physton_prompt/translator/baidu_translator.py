import os
import sys
import requests
import hashlib
import random

# 将父目录添加到Python路径中
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from translator.base_tanslator import BaseTranslator
from get_lang import get_lang


class BaiduTranslator(BaseTranslator):
    def __init__(self):
        super().__init__('baidu')

    def translate(self, text):
        if not text:
            return ''
        url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        app_id = self.api_config.get('app_id', '')
        app_secret = self.api_config.get('app_secret', '')
        
        # 检查是否需要API密钥
        if self.needs_api_key():
            if not app_id:
                raise Exception(get_lang('is_required', {'0': 'APP ID'}))
            if not app_secret:
                raise Exception(get_lang('is_required', {'0': 'APP Secret'}))
        else:
            # 如果不需要API密钥，使用默认值
            if not app_id:
                app_id = "dummy-app-id"
            if not app_secret:
                app_secret = "dummy-app-secret"
        
        salt = random.randint(32768, 65536)
        send_text = text
        if isinstance(text, list):
            send_text = '\n'.join(send_text)
        sign = app_id + send_text + str(salt) + app_secret
        sign = hashlib.md5(sign.encode()).hexdigest()
        params = {
            'q': send_text,
            'from': self.from_lang,
            'to': self.to_lang,
            'appid': app_id,
            'salt': salt,
            'sign': sign
        }
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        if 'error_code' in result:
            raise Exception(result['error_msg'])
        if 'trans_result' not in result:
            raise Exception(get_lang('no_response_from', {'0': 'Baidu'}))
        translated_text = []
        for item in result['trans_result']:
            translated_text.append(item['dst'])
        if isinstance(text, list):
            return translated_text
        else:
            return '\n'.join(translated_text)

    def translate_batch(self, texts):
        if not texts:
            return []
        for text in texts:
            text = text.replace('\n', ' ')
        return self.translate(texts)
