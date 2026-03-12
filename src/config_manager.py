# -*- coding: utf-8 -*-
"""
配置管理器 - 负责读取和保存配置
兼容 Python 3.6.8
"""
import os
import json


class ConfigManager:
    """配置管理器类"""
    
    def __init__(self):
        self.config_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config"
        )
        self.config_file = os.path.join(self.config_dir, "settings.json")
        self.config = {}
        self.load()
    
    def load(self):
        """加载配置文件"""
        default_config = {
            "water_interval": 40,
            "sit_interval": 60,
            "work_hours": {
                "start": "09:00",
                "end": "18:00"
            },
            "auto_start": False,
            "notifications_enabled": True,
            "volume": 50
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception as e:
                print("加载配置失败，使用默认配置: {}".format(e))
                self.config = default_config
        else:
            self.config = default_config
            self.save()
    
    def save(self):
        """保存配置文件"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("保存配置失败: {}".format(e))
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self.config[key] = value
        self.save()
    
    def get_water_interval(self):
        """获取饮水提醒间隔（分钟）"""
        return self.config.get("water_interval", 40)
    
    def get_sit_interval(self):
        """获取久坐提醒间隔（分钟）"""
        return self.config.get("sit_interval", 60)
    
    def is_work_time(self):
        """判断当前是否在工作时间内"""
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        work_hours = self.config.get("work_hours", {"start": "09:00", "end": "18:00"})
        start = work_hours.get("start", "09:00")
        end = work_hours.get("end", "18:00")
        return start <= current_time <= end
    
    def is_notifications_enabled(self):
        """检查通知是否启用"""
        return self.config.get("notifications_enabled", True)
    
    def is_auto_start_enabled(self):
        """检查开机自启动是否启用"""
        return self.config.get("auto_start", False)
