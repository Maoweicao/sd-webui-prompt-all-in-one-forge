import os
import sys
import time

# 将当前目录添加到Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from get_lang import get_lang

model = None
tokenizer = None
model_name = "facebook/mbart-large-50-many-to-many-mmt"
cache_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + '/../../models')
loading = False

def initialize(reload=False):
    global model, tokenizer, model_name, cache_dir, loading
    if loading:
        # 等待模型加载完成
        while loading:
            time.sleep(0.1)
        # 检查模型是否成功加载
        if model is None or tokenizer is None:
            raise Exception(get_lang('model_not_initialized'))
        return
    if not reload and model is not None:
        return
    loading = True
    model = None
    tokenizer = None

    model_path = os.path.join(cache_dir, "mbart-large-50-many-to-many-mmt")
    model_file = os.path.join(model_path, "pytorch_model.bin")
    print(f'[sd-webui-prompt-all-in-one] Checking model path: {model_path}')
    print(f'[sd-webui-prompt-all-in-one] Model file exists: {os.path.exists(model_file)}')
    
    if os.path.exists(model_path) and os.path.exists(model_file):
        model_name = model_path
        print(f'[sd-webui-prompt-all-in-one] Using local model: {model_name}')
    else:
        print(f'[sd-webui-prompt-all-in-one] Using remote model: {model_name}')

    try:
        from transformers import MBart50TokenizerFast, MBartForConditionalGeneration
        print(f'[sd-webui-prompt-all-in-one] Loading model {model_name} from {cache_dir}...')
        model = MBartForConditionalGeneration.from_pretrained(model_name, cache_dir=cache_dir)
        tokenizer = MBart50TokenizerFast.from_pretrained(model_name, cache_dir=cache_dir)
        print(f'[sd-webui-prompt-all-in-one] Model {model_name} loaded successfully.')
        loading = False
    except Exception as e:
        loading = False
        error_msg = f'[sd-webui-prompt-all-in-one] Failed to load model {model_name}: {str(e)}'
        print(error_msg)
        raise Exception(error_msg)

def is_initialized():
    """检查模型是否已初始化"""
    global model, tokenizer
    return model is not None and tokenizer is not None

def translate(text, src_lang, target_lang):
    global model, tokenizer

    if not text:
        if isinstance(text, list):
            return []
        else:
            return ''

    if model is None:
        error_msg = '[sd-webui-prompt-all-in-one] Model is not initialized. Please initialize the model first.'
        print(error_msg)
        raise Exception(get_lang('model_not_initialized'))

    if tokenizer is None:
        error_msg = '[sd-webui-prompt-all-in-one] Tokenizer is not initialized. Please initialize the model first.'
        print(error_msg)
        raise Exception(get_lang('model_not_initialized'))

    if src_lang == target_lang:
        return text

    tokenizer.src_lang = src_lang
    encoded_input = tokenizer(text, return_tensors="pt", padding=True)
    generated_tokens = model.generate(
        **encoded_input, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],
        max_new_tokens=500
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
