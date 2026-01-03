import os
import sys
import traceback

# 将父目录添加到Python路径中
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from translator.base_tanslator import BaseTranslator
from get_lang import get_lang


class TranslatorsTranslator(BaseTranslator):
    """
    本地翻译器实现，不依赖外部 translators 包
    支持通过本地实现的翻译接口
    """
    translator = None

    def set_translator(self, translator):
        self.translator = translator
        return self

    def translate(self, text):
        """
        使用本地实现的翻译方法
        """
        try:
            # 根据翻译器类型调用相应的本地实现
            if self.translator == 'google':
                return self._translate_google(text)
            elif self.translator == 'bing':
                return self._translate_bing(text)
            elif self.translator == 'baidu':
                return self._translate_baidu(text)
            elif self.translator == 'alibaba':
                return self._translate_alibaba(text)
            else:
                raise Exception(f"Unsupported translator: {self.translator}. Please use local translator implementations instead of external 'translators' package.")
        except Exception as e:
            error_msg = f"TranslatorsTranslator Error: {str(e)}\n{traceback.format_exc()}"
            raise Exception(error_msg)

    def _translate_google(self, text):
        """使用本地 Google 翻译实现"""
        # 导入本地的 Google 翻译器
        from translator.google_tanslator import GoogleTranslator
        translator = GoogleTranslator()
        # 直接设置已转换的语言代码，不再调用 set_from_lang/set_to_lang
        translator.from_lang = self.from_lang
        translator.to_lang = self.to_lang
        translator.api_item = self.api_item
        translator.set_api_config(self.api_config)
        return translator.translate(text)

    def _translate_bing(self, text):
        """使用本地 Bing 翻译实现"""
        # 如果需要 Bing 翻译，可以使用 Microsoft 翻译器
        from translator.microsoft_translator import MicrosoftTranslator
        translator = MicrosoftTranslator()
        # 直接设置已转换的语言代码，不再调用 set_from_lang/set_to_lang
        translator.from_lang = self.from_lang
        translator.to_lang = self.to_lang
        translator.api_item = self.api_item
        translator.set_api_config(self.api_config)
        return translator.translate(text)

    def _translate_baidu(self, text):
        """使用本地百度翻译实现"""
        from translator.baidu_translator import BaiduTranslator
        translator = BaiduTranslator()
        # 直接设置已转换的语言代码，不再调用 set_from_lang/set_to_lang
        translator.from_lang = self.from_lang
        translator.to_lang = self.to_lang
        translator.api_item = self.api_item
        translator.set_api_config(self.api_config)
        return translator.translate(text)

    def _translate_alibaba(self, text):
        """使用本地阿里巴巴翻译实现"""
        from translator.alibaba_translator import AlibabaTranslator
        translator = AlibabaTranslator()
        # 直接设置已转换的语言代码，不再调用 set_from_lang/set_to_lang
        translator.from_lang = self.from_lang
        translator.to_lang = self.to_lang
        translator.api_item = self.api_item
        translator.set_api_config(self.api_config)
        return translator.translate(text)
