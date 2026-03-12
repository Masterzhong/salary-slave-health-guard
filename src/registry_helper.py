# -*- coding: utf-8 -*-
"""
注册表助手 - 负责开机自启动注册表操作
兼容 Python 3.6.8
"""
import sys
import os
import winreg


class RegistryHelper:
    """注册表操作助手类"""
    
    APP_NAME = "SalarySlaveHealth"
    REG_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    @classmethod
    def get_exe_path(cls):
        """获取当前可执行文件路径"""
        if getattr(sys, 'frozen', False):
            # 打包后的exe
            return sys.executable
        else:
            # 开发环境下的python
            return sys.executable
    
    @classmethod
    def is_auto_start_enabled(cls):
        """检查是否已启用开机自启动"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                cls.REG_KEY_PATH,
                0,
                winreg.KEY_READ
            )
            try:
                value, _ = winreg.QueryValueEx(key, cls.APP_NAME)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except WindowsError:
            return False
    
    @classmethod
    def enable_auto_start(cls):
        """启用开机自启动"""
        try:
            exe_path = cls.get_exe_path()
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                cls.REG_KEY_PATH,
                0,
                winreg.KEY_WRITE
            )
            winreg.SetValueEx(key, cls.APP_NAME, 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            return True
        except WindowsError as e:
            print("启用开机自启动失败: {}".format(e))
            return False
    
    @classmethod
    def disable_auto_start(cls):
        """禁用开机自启动"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                cls.REG_KEY_PATH,
                0,
                winreg.KEY_WRITE
            )
            try:
                winreg.DeleteValue(key, cls.APP_NAME)
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            return True
        except WindowsError as e:
            print("禁用开机自启动失败: {}".format(e))
            return False
    
    @classmethod
    def toggle_auto_start(cls, enable):
        """切换开机自启动状态"""
        if enable:
            return cls.enable_auto_start()
        else:
            return cls.disable_auto_start()
