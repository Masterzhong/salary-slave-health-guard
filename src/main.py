# -*- coding: utf-8 -*-
"""
牛马健康助手 - 主入口
兼容 Python 3.6.8
"""
import sys
import os

# 确保src目录在Python路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_window import main

if __name__ == "__main__":
    main()
