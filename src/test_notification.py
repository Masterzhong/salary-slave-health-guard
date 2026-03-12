# 测试通知功能
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from notification import Notification

print("测试通知功能...")
print("1. 测试饮水通知...")
Notification.send_water_notification(0)
print("2. 测试久坐通知...")
Notification.send_sit_notification(0)
print("测试完成，请检查是否有通知弹出。")
input("按回车键继续...")