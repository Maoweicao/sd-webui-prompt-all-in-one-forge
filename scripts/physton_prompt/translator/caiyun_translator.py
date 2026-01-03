import os
import sys
import uuid
import requests
import json

# 将父目录添加到Python路径中
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from translator.base_tanslator import BaseTranslator
from get_lang import get_lang


class CaiyunTranslator(BaseTranslator):
    def __init__(self):
        super().__init__('caiyun')

    def translate(self, text):
        if not text:
            return ''
        url = 'http://api.interpreter.caiyunai.com/v1/translator'
        token = self.api_config.get('token', '')
        
        # 检查是否需要API密钥
        if self.needs_api_key():
            if not token:
                raise Exception(get_lang('is_required', {'0': 'Token'}))
        else:
            # 如果不需要API密钥，使用默认值
            if not token:
                token = "dummy-token"

        payload = {
            "source": text,
            "trans_type": f'{self.from_lang}2{self.to_lang}',
            "request_id": str(uuid.uuid4()),
            "detect": True,
        }

        headers = {
            "content-type": "application/json",
            "x-authorization": "token " + token,
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if not response.text:
            raise Exception(get_lang('response_is_empty', {'0': 'caiyun'}))
        result = response.json()
        if 'message' in result:
            raise Exception(result['message'])
        if 'target' not in result:
            raise Exception(get_lang('no_response_from', {'0': 'caiyun'}))
        return result['target']
