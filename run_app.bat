@echo off
echo PDF书签生成器启动脚本
echo ========================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查虚拟环境是否存在
if exist "venv\Scripts\activate.bat" (
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
) else (
    echo 虚拟环境不存在，使用系统Python...
)

REM 运行应用
echo 启动PDF书签生成器...
python pdf_bookmarker_gs.py

REM 如果应用异常退出，暂停显示错误信息
if errorlevel 1 (
    echo.
    echo 应用异常退出，错误代码: %errorlevel%
    pause
)

REM 如果使用了虚拟环境，退出虚拟环境
if exist "venv\Scripts\activate.bat" (
    deactivate
) 