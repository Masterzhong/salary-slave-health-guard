# -*- coding: utf-8 -*-
"""
提醒引擎 - 负责定时发送提醒
兼容 Python 3.6.8
"""
import time
import threading
from config_manager import ConfigManager
from notification import Notification


class ReminderEngine:
    """提醒引擎类"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.notification = Notification()
        self.running = False
        self.thread = None
        self.water_last_remind_time = time.time()
        self.sit_last_remind_time = time.time()
    
    def start(self):
        """启动提醒引擎"""
        if self.running:
            return
        
        self.running = True
        self.water_last_remind_time = time.time()
        self.sit_last_remind_time = time.time()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        print("提醒引擎已启动")
    
    def stop(self):
        """停止提醒引擎"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("提醒引擎已停止")
    
    def _run(self):
        """提醒引擎主循环"""
        while self.running:
            try:
                # 检查是否在工作时间内
                if not self.config.is_work_time():
                    # 不在工作时间内，休息1分钟再检查
                    time.sleep(60)
                    continue
                
                # 检查通知是否启用
                if not self.config.is_notifications_enabled():
                    time.sleep(10)
                    continue
                
                # 检查饮水提醒
                self._check_water_reminder()
                
                # 检查久坐提醒
                self._check_sit_reminder()
                
                # 每10秒检查一次
                time.sleep(10)
                
            except Exception as e:
                print("提醒引擎异常: {}".format(e))
                time.sleep(10)
    
    def _check_water_reminder(self):
        """检查是否需要发送饮水提醒"""
        water_interval = self.config.get_water_interval()
        elapsed_minutes = int((time.time() - self.water_last_remind_time) / 60)
        
        if elapsed_minutes >= water_interval:
            self.notification.send_water_notification(elapsed_minutes)
            self.water_last_remind_time = time.time()
            print("已发送饮水提醒，间隔: {}分钟".format(elapsed_minutes))
    
    def _check_sit_reminder(self):
        """检查是否需要发送久坐提醒"""
        sit_interval = self.config.get_sit_interval()
        elapsed_minutes = int((time.time() - self.sit_last_remind_time) / 60)
        
        if elapsed_minutes >= sit_interval:
            self.notification.send_sit_notification(elapsed_minutes)
            self.sit_last_remind_time = time.time()
            print("已发送久坐提醒，间隔: {}分钟".format(elapsed_minutes))
    
    def reset_water_timer(self):
        """手动重置饮水提醒计时器"""
        self.water_last_remind_time = time.time()
    
    def reset_sit_timer(self):
        """手动重置久坐提醒计时器"""
        self.sit_last_remind_time = time.time()
    
    def update_water_interval(self, minutes):
        """更新饮水提醒间隔"""
        self.config.set("water_interval", minutes)
    
    def update_sit_interval(self, minutes):
        """更新久坐提醒间隔"""
        self.config.set("sit_interval", minutes)
    
    def get_water_elapsed(self):
        """获取饮水提醒已过去时间（分钟）"""
        return int((time.time() - self.water_last_remind_time) / 60)
    
    def get_sit_elapsed(self):
        """获取久坐提醒已过去时间（分钟）"""
        return int((time.time() - self.sit_last_remind_time) / 60)
    
    def is_running(self):
        """检查引擎是否运行"""
        return self.running
