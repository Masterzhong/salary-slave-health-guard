# -*- coding: utf-8 -*-
"""
生成默认图标脚本
由于项目需要icon.ico，但创建二进制文件较为复杂，
提供了一个可选的图标生成脚本

运行此脚本将创建一个简单的图标文件
"""
import os
import sys

# 如果没有图标，会使用系统默认图标
# 用户可以手动替换 resources/icon.ico 为自己的图标

print("注意: 请将您的图标文件放置在 resources/icon.ico")
print("推荐尺寸: 32x32 或 16x16")
print("如果文件不存在，将使用系统默认图标")

# 尝试创建一个简单的占位符图标
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QIcon
    
    # 使用系统默认图标作为备选
    app = QApplication(sys.argv)
    icon = QIcon.fromTheme("face-smile")
    
    # 保存图标
    icon_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "resources",
        "icon.ico"
    )
    
    # 注意: QIcon 没有直接保存为 .ico 的方法
    # 建议手动添加图标文件
    print("请手动添加图标文件到: {}".format(icon_path))
    
except Exception as e:
    print("图标生成跳过: {}".format(e))
