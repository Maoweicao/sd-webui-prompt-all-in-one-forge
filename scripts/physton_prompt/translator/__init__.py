"""
Translator Module
"""

import os
import sys

# 将当前目录添加到Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)