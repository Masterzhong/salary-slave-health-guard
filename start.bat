@echo off
:: 牛马健康助手 - 快速启动脚本
echo ========================================
echo   牛马健康助手 - 打工人の守护神
echo ========================================
echo.

:: 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.6.8
    pause
    exit /b 1
)

:: 检查依赖
echo [1/3] 检查依赖...
pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo [警告] PyQt5未安装，正在安装...
    pip install PyQt5==5.12.3
)

pip show win10toast >nul 2>&1
if errorlevel 1 (
    echo [警告] win10toast未安装，正在安装...
    pip install win10toast
)

:: 启动程序
echo [2/3] 启动程序...
cd /d "%~dp0src"
python main.py

echo [3/3] 程序已退出
pause
