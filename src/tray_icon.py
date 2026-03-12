# -*- coding: utf-8 -*-
"""
系统托盘图标模块
兼容 Python 3.6.8
"""
import os
import sys
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class TrayIcon(QSystemTrayIcon):
    """系统托盘图标类"""
    
    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        
        # 设置图标
        self.set_icon()
        
        # 创建菜单
        self.create_menu()
        
        # 连接信号
        self.activated.connect(self.on_tray_activated)
        
        # 设置提示信息
        self.setToolTip("牛马健康助手 - 打工人の守护神")
    
    def set_icon(self):
        """设置托盘图标"""
        # 尝试从资源目录加载图标
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "resources",
            "icon.ico"
        )
        
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
        else:
            # 尝试从应用程序图标加载
            try:
                import sys
                # 尝试从当前进程的图标获取
                from PyQt5.QtWidgets import QApplication
                app = QApplication.instance()
                if app and hasattr(app, 'windowIcon') and not app.windowIcon().isNull():
                    self.setIcon(app.windowIcon())
                else:
                    # 创建一个简单的图标
                    self._create_default_icon()
            except Exception as e:
                print("设置图标失败: {}".format(e))
                self._create_default_icon()
    
    def _create_default_icon(self):
        """创建默认图标"""
        try:
            from PyQt5.QtGui import QPixmap, QPainter, QColor
            from PyQt5.QtCore import QSize
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(66, 133, 244))  # 蓝色背景
            self.setIcon(QIcon(pixmap))
        except Exception as e:
            print("创建默认图标失败: {}".format(e))
    
    def create_menu(self):
        """创建托盘菜单"""
        self.menu = QMenu()
        
        # 状态显示
        self.status_action = QAction("状态: 运行中", self.menu)
        self.status_action.setEnabled(False)
        self.menu.addAction(self.status_action)
        
        self.menu.addSeparator()
        
        # 饮水提醒
        self.water_action = QAction("💧 饮水提醒", self.menu)
        self.water_action.triggered.connect(self.on_water_clicked)
        self.menu.addAction(self.water_action)
        
        # 久坐提醒
        self.sit_action = QAction("🏃 久坐提醒", self.menu)
        self.sit_action.triggered.connect(self.on_sit_clicked)
        self.menu.addAction(self.sit_action)
        
        self.menu.addSeparator()
        
        # 打开主窗口
        self.show_action = QAction("📋 打开主窗口", self.menu)
        self.show_action.triggered.connect(self.on_show_clicked)
        self.menu.addAction(self.show_action)
        
        self.menu.addSeparator()
        
        # 退出
        self.quit_action = QAction("❌ 退出", self.menu)
        self.quit_action.triggered.connect(self.on_quit_clicked)
        self.menu.addAction(self.quit_action)
        
        self.setContextMenu(self.menu)
    
    def on_tray_activated(self, reason):
        """托盘图标被点击"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.on_show_clicked()
    
    def on_water_clicked(self):
        """点击饮水提醒"""
        from notification import Notification
        Notification.send_water_notification(0)
    
    def on_sit_clicked(self):
        """点击久坐提醒"""
        from notification import Notification
        Notification.send_sit_notification(0)
    
    def on_show_clicked(self):
        """点击显示主窗口"""
        from main_window import MainWindow
        MainWindow.show_main_window()
    
    def on_quit_clicked(self):
        """点击退出"""
        from PyQt5.QtWidgets import QApplication
        QApplication.instance().quit()
    
    def update_status(self, status_text):
        """更新状态显示"""
        self.status_action.setText("状态: {}".format(status_text))
    
    def show_message(self, title, message):
        """显示托盘消息"""
        self.showMessage(title, message, QSystemTrayIcon.Information, 3000)
