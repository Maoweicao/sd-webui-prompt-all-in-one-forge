import os
import sys

# 将父目录添加到Python路径中
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from translator.base_tanslator import BaseTranslator
from get_lang import get_lang
from mbart50 import initialize as mbart50_initialize, translate as mbart50_translate, is_initialized as mbart50_is_initialized


class MBart50Translator(BaseTranslator):
    def __init__(self):
        super().__init__('mbart50')
        # 确保模型在创建翻译器实例时就被初始化
        try:
            mbart50_initialize()
        except Exception as e:
            print(f'[sd-webui-prompt-all-in-one] Failed to initialize MBart50 model: {str(e)}')

    def translate(self, text):
        if not text:
            if isinstance(text, list):
                return []
            else:
                return ''

        # 检查模型是否已初始化，如果没有则尝试初始化
        if not mbart50_is_initialized():
            print('[sd-webui-prompt-all-in-one] Model not initialized, attempting to initialize...')
            try:
                mbart50_initialize()
                if not mbart50_is_initialized():
                    raise Exception(get_lang('model_not_initialized'))
            except Exception as e:
                print(f'[sd-webui-prompt-all-in-one] Failed to initialize MBart50 model: {str(e)}')
                raise Exception(get_lang('model_not_initialized'))

        result = mbart50_translate(text=text, src_lang=self.from_lang, target_lang=self.to_lang)
        if not result:
            raise Exception(get_lang('response_is_empty', {'0': 'mbart50'}))

        if isinstance(text, list):
            return result
        else:
            return result[0]

    def translate_batch(self, texts):
        return self.translate(texts)
