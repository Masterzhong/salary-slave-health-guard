# -*- coding: utf-8 -*-
"""
主窗口模块 - GUI界面
兼容 Python 3.6.8
"""
import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QGroupBox, QSpinBox, QCheckBox,
    QMessageBox, QApplication, QSystemTrayIcon
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont

from config_manager import ConfigManager
from registry_helper import RegistryHelper
from reminder_engine import ReminderEngine
from tray_icon import TrayIcon


class MainWindow(QMainWindow):
    """主窗口类"""
    
    main_window_instance = None
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # 单例模式
        MainWindow.main_window_instance = self
        
        self.config = ConfigManager()
        self.reminder_engine = ReminderEngine()
        
        self.init_ui()
        self.init_tray()
        self.start_reminder()
        
        # 更新计时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)
    
    @staticmethod
    def show_main_window():
        """显示主窗口（静态方法）"""
        if MainWindow.main_window_instance:
            MainWindow.main_window_instance.show()
            MainWindow.main_window_instance.raise_()
            MainWindow.main_window_instance.activateWindow()
        else:
            app = QApplication.instance()
            if app:
                window = MainWindow()
                window.show()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("牛马健康助手 - 打工人の守护神")
        self.setGeometry(300, 300, 450, 400)
        
        # 禁止最大化
        self.setFixedSize(450, 400)
        
        # 设置窗口图标
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "resources",
            "icon.ico"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 标题
        title_label = QLabel("🐂 牛马健康助手 🐴")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 副标题
        subtitle_label = QLabel("打工人の健康守护神，守护你的每一根头发！")
        subtitle_font = QFont()
        subtitle_font.setPointSize(9)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(10)
        
        # 状态显示
        self.status_group = QGroupBox("📊 当前状态")
        status_layout = QVBoxLayout()
        
        self.water_status_label = QLabel("💧 饮水提醒: 未启动")
        self.sit_status_label = QLabel("🏃 久坐提醒: 未启动")
        self.work_time_label = QLabel("⏰ 工作时间: 检测中...")
        
        status_layout.addWidget(self.water_status_label)
        status_layout.addWidget(self.sit_status_label)
        status_layout.addWidget(self.work_time_label)
        
        self.status_group.setLayout(status_layout)
        main_layout.addWidget(self.status_group)
        
        # 设置区域
        self.settings_group = QGroupBox("⚙️ 设置")
        settings_layout = QVBoxLayout()
        
        # 饮水间隔
        water_layout = QHBoxLayout()
        water_layout.addWidget(QLabel("饮水提醒间隔（分钟）:"))
        self.water_spinbox = QSpinBox()
        self.water_spinbox.setRange(10, 120)
        self.water_spinbox.setValue(self.config.get_water_interval())
        self.water_spinbox.valueChanged.connect(self.on_water_interval_changed)
        water_layout.addWidget(self.water_spinbox)
        water_layout.addStretch()
        settings_layout.addLayout(water_layout)
        
        # 久坐间隔
        sit_layout = QHBoxLayout()
        sit_layout.addWidget(QLabel("久坐提醒间隔（分钟）:"))
        self.sit_spinbox = QSpinBox()
        self.sit_spinbox.setRange(30, 180)
        self.sit_spinbox.setValue(self.config.get_sit_interval())
        self.sit_spinbox.valueChanged.connect(self.on_sit_interval_changed)
        sit_layout.addWidget(self.sit_spinbox)
        sit_layout.addStretch()
        settings_layout.addLayout(sit_layout)
        
        # 开机自启动
        self.auto_start_checkbox = QCheckBox("开机自动启动")
        self.auto_start_checkbox.setChecked(RegistryHelper.is_auto_start_enabled())
        self.auto_start_checkbox.stateChanged.connect(self.on_auto_start_changed)
        settings_layout.addWidget(self.auto_start_checkbox)
        
        # 通知开关
        self.notification_checkbox = QCheckBox("启用桌面通知")
        self.notification_checkbox.setChecked(self.config.is_notifications_enabled())
        self.notification_checkbox.stateChanged.connect(self.on_notification_changed)
        settings_layout.addWidget(self.notification_checkbox)
        
        self.settings_group.setLayout(settings_layout)
        main_layout.addWidget(self.settings_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.reset_water_btn = QPushButton("⏰ 重置饮水计时")
        self.reset_water_btn.clicked.connect(self.on_reset_water)
        button_layout.addWidget(self.reset_water_btn)
        
        self.reset_sit_btn = QPushButton("⏰ 重置久坐计时")
        self.reset_sit_btn.clicked.connect(self.on_reset_sit)
        button_layout.addWidget(self.reset_sit_btn)
        
        main_layout.addLayout(button_layout)
        
        # 测试按钮
        test_layout = QHBoxLayout()
        
        self.test_water_btn = QPushButton("🧪 测试饮水通知")
        self.test_water_btn.clicked.connect(self.on_test_water)
        test_layout.addWidget(self.test_water_btn)
        
        self.test_sit_btn = QPushButton("🧪 测试久坐通知")
        self.test_sit_btn.clicked.connect(self.on_test_sit)
        test_layout.addWidget(self.test_sit_btn)
        
        main_layout.addLayout(test_layout)
        
        # 底部提示
        tip_label = QLabel("提示: 程序将隐藏在系统托盘，点击托盘图标可恢复窗口")
        tip_label.setStyleSheet("color: gray; font-size: 9pt;")
        tip_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(tip_label)
    
    def init_tray(self):
        """初始化系统托盘"""
        self.tray = TrayIcon(self)
        self.tray.show()
    
    def start_reminder(self):
        """启动提醒引擎"""
        self.reminder_engine.start()
    
    def update_status(self):
        """更新状态显示"""
        if self.reminder_engine.is_running():
            water_elapsed = self.reminder_engine.get_water_elapsed()
            sit_elapsed = self.reminder_engine.get_sit_elapsed()
            water_interval = self.config.get_water_interval()
            sit_interval = self.config.get_sit_interval()
            
            water_percent = min(100, int(water_elapsed / water_interval * 100))
            sit_percent = min(100, int(sit_elapsed / sit_interval * 100))
            
            self.water_status_label.setText(
                "💧 饮水提醒: 已过 {}分钟 / {}分钟 ({}{})".format(
                    water_elapsed, water_interval, water_percent, "%"
                )
            )
            self.sit_status_label.setText(
                "🏃 久坐提醒: 已过 {}分钟 / {}分钟 ({}{})".format(
                    sit_elapsed, sit_interval, sit_percent, "%"
                )
            )
        
        # 工作时间状态
        if self.config.is_work_time():
            self.work_time_label.setText("⏰ 工作时间: ✅ 是")
            self.work_time_label.setStyleSheet("color: green;")
        else:
            self.work_time_label.setText("⏰ 工作时间: ❌ 否")
            self.work_time_label.setStyleSheet("color: red;")
    
    def on_water_interval_changed(self, value):
        """饮水间隔改变"""
        self.config.set("water_interval", value)
        self.reminder_engine.update_water_interval(value)
    
    def on_sit_interval_changed(self, value):
        """久坐间隔改变"""
        self.config.set("sit_interval", value)
        self.reminder_engine.update_sit_interval(value)
    
    def on_auto_start_changed(self, state):
        """开机自启动改变"""
        enabled = (state == Qt.Checked)
        RegistryHelper.toggle_auto_start(enabled)
        self.config.set("auto_start", enabled)
    
    def on_notification_changed(self, state):
        """通知开关改变"""
        enabled = (state == Qt.Checked)
        self.config.set("notifications_enabled", enabled)
    
    def on_reset_water(self):
        """重置饮水计时"""
        self.reminder_engine.reset_water_timer()
        QMessageBox.information(self, "提示", "饮水计时已重置！")
    
    def on_reset_sit(self):
        """重置久坐计时"""
        self.reminder_engine.reset_sit_timer()
        QMessageBox.information(self, "提示", "久坐计时已重置！")
    
    def on_test_water(self):
        """测试饮水通知"""
        from notification import Notification
        Notification.send_water_notification(0)
    
    def on_test_sit(self):
        """测试久坐通知"""
        from notification import Notification
        Notification.send_sit_notification(0)
    
    def closeEvent(self, event):
        """关闭窗口事件 - 最小化到托盘"""
        event.ignore()
        self.hide()
        if self.tray:
            self.tray.show_message(
                "牛马健康助手",
                "程序已最小化到系统托盘，右键托盘图标可退出"
            )


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
