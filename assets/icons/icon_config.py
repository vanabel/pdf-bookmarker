#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标配置文件
定义不同平台和场景下的图标路径
"""

import os
import sys
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

class IconConfig:
    """图标配置类"""
    
    def __init__(self):
        self.icons_dir = PROJECT_ROOT / "assets" / "icons"
        self.icons = {
            "512": self.icons_dir / "icon_512.png",
            "256": self.icons_dir / "icon_256.png", 
            "128": self.icons_dir / "icon_128.png",
            "64": self.icons_dir / "icon_64.png",
            "32": self.icons_dir / "icon_32.png",  # 如果需要的话
        }
    
    def get_icon_path(self, size="512"):
        """获取指定尺寸的图标路径"""
        icon_path = self.icons.get(str(size), self.icons["512"])
        if icon_path.exists():
            return str(icon_path)
        return None
    
    def get_all_icons(self):
        """获取所有可用的图标"""
        return {size: path for size, path in self.icons.items() if path.exists()}
    
    def get_platform_icon(self):
        """根据平台获取合适的图标"""
        if sys.platform == "darwin":  # macOS
            return self.get_icon_path("512")  # macOS支持高分辨率
        elif sys.platform == "win32":  # Windows
            return self.get_icon_path("256")  # Windows通常使用256x256
        else:  # Linux
            return self.get_icon_path("128")  # Linux通常使用128x128
    
    def get_tray_icon(self):
        """获取系统托盘图标"""
        return self.get_icon_path("64") or self.get_icon_path("32")
    
    def get_taskbar_icon(self):
        """获取任务栏图标"""
        return self.get_icon_path("128") or self.get_icon_path("64")

# 全局图标配置实例
icon_config = IconConfig()

if __name__ == "__main__":
    # 测试图标配置
    print("图标配置测试:")
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"图标目录: {icon_config.icons_dir}")
    print(f"可用图标: {icon_config.get_all_icons()}")
    print(f"平台图标: {icon_config.get_platform_icon()}")
    print(f"托盘图标: {icon_config.get_tray_icon()}")
