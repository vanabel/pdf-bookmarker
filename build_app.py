#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF书签生成器 - 应用打包脚本
使用PyInstaller将应用打包成可执行文件
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller未安装")
        print("请运行: pip install pyinstaller")
        return False

def get_platform_info():
    """获取平台信息"""
    system = platform.system()
    machine = platform.machine()
    print(f"🖥️ 平台: {system} {machine}")
    return system, machine

def build_app():
    """构建应用"""
    print("🔨 开始构建PDF书签生成器应用...")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    main_app = current_dir / "pdf_bookmarker_gs.py"
    
    if not main_app.exists():
        print(f"❌ 主应用文件不存在: {main_app}")
        return False
    
    # 构建命令
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个文件
        "--windowed",                   # 无控制台窗口（GUI应用）
        "--name=PDF书签生成器",          # 应用名称
        "--icon=icon.ico",              # 图标文件（如果存在）
        "--add-data=demo:demo",         # 包含demo目录
        "--hidden-import=tkinter",      # 确保tkinter被包含
        "--hidden-import=tkinter.ttk",  # 确保ttk被包含
        "--clean",                      # 清理临时文件
        str(main_app)
    ]
    
    # 如果图标文件不存在，移除图标参数
    if not (current_dir / "icon.ico").exists():
        cmd = [c for c in cmd if not c.startswith("--icon")]
        print("⚠️  图标文件不存在，将使用默认图标")
    
    print("📋 构建命令:")
    print(" ".join(cmd))
    print()
    
    # 执行构建
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 应用构建成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def create_launcher_scripts():
    """创建启动脚本"""
    print("📝 创建启动脚本...")
    
    current_dir = Path(__file__).parent
    dist_dir = current_dir / "dist"
    
    if not dist_dir.exists():
        print("❌ dist目录不存在，构建可能失败")
        return
    
    # Windows启动脚本
    if platform.system() == "Windows":
        launcher_bat = current_dir / "启动PDF书签生成器.bat"
        launcher_bat.write_text("""@echo off
echo 正在启动PDF书签生成器...
cd /d "%~dp0"
"dist\\PDF书签生成器.exe"
pause
""", encoding='gbk')
        print("✅ 创建Windows启动脚本: 启动PDF书签生成器.bat")
    
    # macOS/Linux启动脚本
    else:
        launcher_sh = current_dir / "启动PDF书签生成器.sh"
        launcher_sh.write_text("""#!/bin/bash
echo "正在启动PDF书签生成器..."
cd "$(dirname "$0")"
./dist/PDF书签生成器
""", encoding='utf-8')
        
        # 设置执行权限
        os.chmod(launcher_sh, 0o755)
        print("✅ 创建Unix启动脚本: 启动PDF书签生成器.sh")
    
    # 创建README
    readme = current_dir / "应用使用说明.txt"
    readme.write_text("""PDF书签生成器 - 应用使用说明
=====================================

🎯 应用已成功打包！

📁 文件说明:
- dist/PDF书签生成器.exe (Windows) 或 dist/PDF书签生成器 (macOS/Linux)
- 启动PDF书签生成器.bat (Windows启动脚本)
- 启动PDF书签生成器.sh (macOS/Linux启动脚本)

🚀 使用方法:
1. 双击启动脚本或直接运行可执行文件
2. 确保系统已安装Ghostscript
3. 按照界面提示操作

⚠️  注意事项:
- 首次运行可能需要几秒钟启动
- 确保有足够的磁盘空间
- 如果遇到问题，检查Ghostscript安装

🔧 系统要求:
- Windows 7+ / macOS 10.10+ / Linux (Ubuntu 16.04+)
- Ghostscript (必需)
- 至少100MB可用磁盘空间

📞 技术支持:
如有问题，请查看项目README.md或提交Issue
""", encoding='utf-8')
    
    print("✅ 创建应用使用说明: 应用使用说明.txt")

def main():
    """主函数"""
    print("🎯 PDF书签生成器 - 应用打包工具")
    print("=" * 50)
    
    # 检查PyInstaller
    if not check_pyinstaller():
        return
    
    # 获取平台信息
    get_platform_info()
    print()
    
    # 构建应用
    if build_app():
        print()
        # 创建启动脚本
        create_launcher_scripts()
        print()
        print("🎉 打包完成！")
        print("📁 可执行文件位置: dist/PDF书签生成器")
        print("📖 查看应用使用说明.txt了解详细信息")
    else:
        print("❌ 打包失败，请检查错误信息")

if __name__ == "__main__":
    main() 