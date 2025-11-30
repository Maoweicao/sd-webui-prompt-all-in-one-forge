import os
import sys

# 将父目录添加到Python路径中
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from translator.base_tanslator import BaseTranslator


class TranslatorsTranslator(BaseTranslator):
    translator = None

    def set_translator(self, translator):
        self.translator = translator
        return self

    def translate(self, text):
        region = self.api_config.get('region', 'CN')
        host = self.api_config.get('host', '')
        os.environ['translators_default_region'] = region
        from scripts.physton_prompt.translators.server import translate_text, tss, AlibabaV1
        tss.server_region = region
        tss._bing.server_region = region
        tss._google.server_region = region

        params = {
            'from_language': self.from_lang,
            'to_language': self.to_lang,
            'translator': self.translator,
            'reset_host_url': host,
            'if_check_reset_host_url': False,
            'timeout': 30
        }
        return translate_text(text, **params)
        # return translate_text(text, from_language=self.from_lang, to_language=self.to_lang, translator=self.translator, timeout=30)
