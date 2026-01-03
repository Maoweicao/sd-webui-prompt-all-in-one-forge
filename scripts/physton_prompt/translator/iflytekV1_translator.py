import os
import sys
import requests
import datetime
import hashlib
import base64
import hmac
import json

# 将父目录添加到Python路径中
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from translator.base_tanslator import BaseTranslator
from get_lang import get_lang


class IflytekV1Translator(BaseTranslator):
    def __init__(self):
        super().__init__('iflytekV1')

    def translate(self, text):
        if not text:
            return ''
        app_id = self.api_config.get('app_id', '')
        api_secret = self.api_config.get('api_secret', '')
        api_key = self.api_config.get('api_key', '')
        
        # 检查是否需要API密钥
        if self.needs_api_key():
            if not app_id:
                raise Exception(get_lang('is_required', {'0': 'APP ID'}))
            if not api_secret:
                raise Exception(get_lang('is_required', {'0': 'API Secret'}))
            if not api_key:
                raise Exception(get_lang('is_required', {'0': 'API Key'}))
        else:
            # 如果不需要API密钥，使用默认值
            if not app_id:
                app_id = "dummy-app-id"
            if not api_secret:
                api_secret = "dummy-api-secret"
            if not api_key:
                api_key = "dummy-api-key"

        response = translate(text, From=self.from_lang, To=self.to_lang, APPID=app_id, Secret=api_secret, APIKey=api_key)
        if response.status_code != 200:
            raise Exception(get_lang('request_error', {'0': 'iflytekV1'}))
        if not response.text:
            raise Exception(get_lang('response_is_empty', {'0': 'iflytekV1'}))
        result = response.json()
        if 'code' not in result:
            raise Exception(get_lang('no_response_from', {'0': 'iflytekV1'}))
        if result['code'] != 0:
            raise Exception(result['message'])
        return result['data']['result']['trans_result']['dst']


def hashlib_256(res):
    m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
    result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
    return result

def httpdate(dt):
    """
    Return a string representation of a date according to RFC 1123
    (HTTP/1.1).

    The supplied date must be in UTC.

    """
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                "Oct", "Nov", "Dec"][dt.month - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                    dt.year, dt.hour, dt.minute, dt.second)

def translate(Text, From, To, APPID, Secret, APIKey, Host="itrans.xfyun.cn"):
    RequestUri = "/v2/its"
    url="https://"+Host+RequestUri
    HttpMethod = "POST"
    Algorithm = "hmac-sha256"
    HttpProto = "HTTP/1.1"

    # 设置当前时间
    curTime_utc = datetime.datetime.utcnow()
    Date = httpdate(curTime_utc)
    # 设置业务参数
    # 语种列表参数值请参照接口文档：https://www.xfyun.cn/doc/nlp/xftrans/API.html
    BusinessArgs={
        "from":From,
        "to": To,
    }

    content = str(base64.b64encode(Text.encode('utf-8')), 'utf-8')
    postdata = {
        "common": {"app_id": APPID},
        "business": BusinessArgs,
        "data": {
            "text": content,
        }
    }
    body = json.dumps(postdata)

    digest = hashlib_256(body)
    signatureStr = "host: " + Host + "\n"
    signatureStr += "date: " + Date + "\n"
    signatureStr += HttpMethod + " " + RequestUri \
                    + " " + HttpProto + "\n"
    signatureStr += "digest: " + digest
    signature = hmac.new(bytes(Secret.encode(encoding='utf-8')),
                            bytes(signatureStr.encode(encoding='utf-8')),
                            digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(signature).decode(encoding='utf-8')

    authHeader = 'api_key="%s", algorithm="%s", ' \
                    'headers="host date request-line digest", ' \
                    'signature="%s"' \
                    % (APIKey, Algorithm, sign)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Method": "POST",
        "Host": Host,
        "Date": Date,
        "Digest": digest,
        "Authorization": authHeader
    }

    response = requests.post(url, data=body, headers=headers,timeout=60)
    return response
