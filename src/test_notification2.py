# 测试通知功能
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from notification import Notification

print("测试通知功能...")
print("1. 测试饮水通知...")
Notification.send_water_notification(0)
print("等待3秒...")
time.sleep(3)
print("2. 测试久坐通知...")
Notification.send_sit_notification(0)
print("等待3秒...")
time.sleep(3)
print("测试完成，请检查是否有通知弹出。")
print("如果没有通知，可能是win10toast在Win11上不兼容。")
print("尝试使用备用方案...")

# 直接测试备用方案
import ctypes
user32 = ctypes.windll.user32
print("测试Windows MessageBox...")
user32.MessageBoxW(0, "测试消息", "测试标题", 0x40)
print("MessageBox应该已经显示了。")