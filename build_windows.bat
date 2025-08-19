@echo off
chcp 65001 >nul
echo 🪟 Windows PDF书签生成器打包脚本
echo ====================================

REM 检查虚拟环境
if not exist "venv" (
    echo ❌ 虚拟环境不存在，请先创建虚拟环境
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 检查PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo 📦 安装PyInstaller...
    pip install pyinstaller
)

REM 检查主应用文件
if not exist "pdf_bookmarker_gs.py" (
    echo ❌ 主应用文件不存在: pdf_bookmarker_gs.py
    pause
    exit /b 1
)

echo 🔨 开始构建应用...

REM 构建命令
pyinstaller ^
    --onefile ^
    --windowed ^
    --name="PDF书签生成器" ^
    --add-data="demo;demo" ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --clean ^
    pdf_bookmarker_gs.py

if errorlevel 0 (
    echo ✅ 应用构建成功！
    
    REM 创建启动脚本
    echo @echo off > "启动PDF书签生成器.bat"
    echo echo 正在启动PDF书签生成器... >> "启动PDF书签生成器.bat"
    echo cd /d "%%~dp0" >> "启动PDF书签生成器.bat"
    echo "dist\PDF书签生成器.exe" >> "启动PDF书签生成器.bat"
    echo pause >> "启动PDF书签生成器.bat"
    
    echo ✅ 创建启动脚本: 启动PDF书签生成器.bat
    
    REM 创建使用说明
    echo PDF书签生成器 - 应用使用说明 > "应用使用说明.txt"
    echo ===================================== >> "应用使用说明.txt"
    echo. >> "应用使用说明.txt"
    echo 🎯 应用已成功打包！ >> "应用使用说明.txt"
    echo. >> "应用使用说明.txt"
    echo 📁 文件说明: >> "应用使用说明.txt"
    echo - dist\PDF书签生成器.exe (Windows可执行文件) >> "应用使用说明.txt"
    echo - 启动PDF书签生成器.bat (启动脚本) >> "应用使用说明.txt"
    echo. >> "应用使用说明.txt"
    echo 🚀 使用方法: >> "应用使用说明.txt"
    echo 1. 双击启动脚本或直接运行可执行文件 >> "应用使用说明.txt"
    echo 2. 确保系统已安装Ghostscript >> "应用使用说明.txt"
    echo 3. 按照界面提示操作 >> "应用使用说明.txt"
    echo. >> "应用使用说明.txt"
    echo ⚠️  注意事项: >> "应用使用说明.txt"
    echo - 首次运行可能需要几秒钟启动 >> "应用使用说明.txt"
    echo - 确保有足够的磁盘空间 >> "应用使用说明.txt"
    echo - 如果遇到问题，检查Ghostscript安装 >> "应用使用说明.txt"
    echo. >> "应用使用说明.txt"
    echo 🔧 系统要求: >> "应用使用说明.txt"
    echo - Windows 7+ >> "应用使用说明.txt"
    echo - Ghostscript (必需) >> "应用使用说明.txt"
    echo - 至少100MB可用磁盘空间 >> "应用使用说明.txt"
    echo. >> "应用使用说明.txt"
    echo 📞 技术支持: >> "应用使用说明.txt"
    echo 如有问题，请查看项目README.md或提交Issue >> "应用使用说明.txt"
    
    echo ✅ 创建应用使用说明: 应用使用说明.txt
    
    echo.
    echo 🎉 打包完成！
    echo 📁 可执行文件位置: dist\PDF书签生成器.exe
    echo 📖 查看应用使用说明.txt了解详细信息
    echo.
    echo 🚀 运行应用:
    echo    启动PDF书签生成器.bat
    echo    或直接运行: dist\PDF书签生成器.exe
    
) else (
    echo ❌ 构建失败
)

pause 