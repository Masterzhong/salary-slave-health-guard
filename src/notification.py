# -*- coding: utf-8 -*-
"""
通知模块 - 负责发送桌面通知
兼容 Python 3.6.8
"""
import random
import time


class Notification:
    """通知类"""
    
    # 饮水提醒幽默文案
    WATER_MESSAGES = [
        "骚年，该喝水了！你身体70%是水，别让自己变成牛肉干！🥤",
        "喝水时间到！研究表明，喝水的人比不喝水的人...更容易尿尿！但还是得喝！💧",
        "叮！您的膀胱已就绪，请及时补充水分！别等到变成仙人掌才后悔！🌵",
        "老板来了...不是，是水来了！快去喝水吧！BOSS直聘不能让你升职，但喝水能让你健康！💦",
        "饮水提醒：再不买水喝，你的血液就要变成沙漠了！快去倒水！🏜️",
        "打工人の自我修养：上班喝水，下班喝水，争取每天喝够8杯！喝完这杯还有三杯！☕",
        "温馨提示：您已缺水{minutes}分钟，再不喝水就要变成木乃伊了！速去补水！👻",
        "喝水啦！别让你的肾对你失望！它们全年无休地为你工作，给点奖励行不行？🚰",
        "叮！您的水分已耗尽，请立即补充！现在下单还有机会获得...一泡尿的容量！😂",
        "打工人，打工魂，打工要喝养生神！喝水こそ王道を生きる！💪",
    ]
    
    # 久坐提醒幽默文案
    SIT_MESSAGES = [
        "久坐警告！再坐下去你的屁股就要和椅子融为一体了！快站起来！🏃",
        "是时候站起来了！你的腰椎正在发出SOS求救信号！再不起来就要罢工了！⚠️",
        "打工而已，别真把自己钉在椅子上！起来活动活动，否则35岁后你将收获一个铁板屁股！🦴",
        "温馨提示：您已保持坐姿{minutes}分钟，痔疮正在积极开发中...快站起来！🚫",
        "站起来！别让椅子太寂寞！它已经爱你爱到无法自拔了！💕",
        "打工人，anyway，站起来活动一下吧！你的身体不是永动机，需要加油（活动）！⛽",
        "您的屁股已超时服役，请立即起立致敬！稍息！立正！解散！🚶",
        "再坐下去，你就要变成椅子上的化石了！快起来变成自由的灵魂！🦋",
        "打工人，anyways，站起来走走吧！虽然工作做不完，但腰椎只有一个！且用且珍惜！🧘",
        "警告：您的菊花正在受到威胁！请立即执行站立命令！保护菊花，人人有责！🌻",
    ]
    
    def __init__(self):
        self.last_water_time = time.time()
        self.last_sit_time = time.time()
    
    @staticmethod
    def send_water_notification(minutes=40):
        """发送饮水提醒通知"""
        from win10toast import ToastNotifier
        import threading
        
        message = random.choice(Notification.WATER_MESSAGES)
        message = message.format(minutes=minutes)
        
        def show_toast():
            try:
                toaster = ToastNotifier()
                toaster.show_toast(
                    "牛马健康助手 💧 饮水提醒",
                    message,
                    duration=10,
                    threaded=True
                )
            except Exception as e:
                print("通知发送失败: {}".format(e))
        
        thread = threading.Thread(target=show_toast)
        thread.daemon = True
        thread.start()
    
    @staticmethod
    def send_sit_notification(minutes=60):
        """发送久坐提醒通知"""
        from win10toast import ToastNotifier
        import threading
        
        message = random.choice(Notification.SIT_MESSAGES)
        message = message.format(minutes=minutes)
        
        def show_toast():
            try:
                toaster = ToastNotifier()
                toaster.show_toast(
                    "牛马健康助手 🏃 久坐提醒",
                    message,
                    duration=10,
                    threaded=True
                )
            except Exception as e:
                print("通知发送失败: {}".format(e))
        
        thread = threading.Thread(target=show_toast)
        thread.daemon = True
        thread.start()
    
    @staticmethod
    def send_custom_notification(title, message):
        """发送自定义通知"""
        from win10toast import ToastNotifier
        import threading
        
        def show_toast():
            try:
                toaster = ToastNotifier()
                toaster.show_toast(
                    title,
                    message,
                    duration=10,
                    threaded=True
                )
            except Exception as e:
                print("通知发送失败: {}".format(e))
        
        thread = threading.Thread(target=show_toast)
        thread.daemon = True
        thread.start()
    
    def update_last_water_time(self):
        """更新最后一次饮水时间"""
        self.last_water_time = time.time()
    
    def update_last_sit_time(self):
        """更新最后一次活动时间"""
        self.last_sit_time = time.time()
    
    def get_elapsed_minutes(self, last_time):
        """获取经过的分钟数"""
        return int((time.time() - last_time) / 60)
