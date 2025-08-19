#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo示例加载器
帮助用户快速加载和测试不同的书签示例
"""

import os
import sys
from pathlib import Path

def list_demo_files():
    """列出demo目录中的所有示例文件"""
    demo_dir = Path(__file__).parent
    print("📁 Demo目录中的示例文件:")
    print("=" * 60)
    
    # 书签示例文件
    print("📚 书签示例文件:")
    bookmark_files = [
        ("simple_bookmarks.txt", "简单书签示例 - 基础章节结构"),
        ("dots_format_bookmarks.txt", "点线格式示例 - 自动识别点线分隔"),
        ("dynamic_offset_bookmarks.txt", "动态偏移示例 - HTML注释风格偏移指令"),
        ("full_bookmarks.txt", "完整书签示例 - 15章节学术书籍目录")
    ]
    
    for filename, description in bookmark_files:
        filepath = demo_dir / filename
        if filepath.exists():
            print(f"  ✅ {filename:<25} - {description}")
        else:
            print(f"  ❌ {filename:<25} - {description} (文件不存在)")
    
    print()
    
    # PDF文件
    print("📄 PDF文件:")
    pdf_files = [
        ("Lieberman_1996_Second order parabolic differential equations.pdf", "原始PDF文件"),
        ("Lieberman_1996_Second order parabolic differential equations_with_bookmarks.pdf", "带书签的PDF文件")
    ]
    
    for filename, description in pdf_files:
        filepath = demo_dir / filename
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"  ✅ {filename:<25} - {description} ({size_mb:.1f} MB)")
        else:
            print(f"  ❌ {filename:<25} - {description} (文件不存在)")
    
    print()

def show_file_content(filename):
    """显示指定文件的内容"""
    demo_dir = Path(__file__).parent
    filepath = demo_dir / filename
    
    if not filepath.exists():
        print(f"❌ 文件 {filename} 不存在")
        return
    
    print(f"📖 文件内容: {filename}")
    print("=" * 60)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")

def copy_to_clipboard(filename):
    """将文件内容复制到剪贴板（如果支持）"""
    demo_dir = Path(__file__).parent
    filepath = demo_dir / filename
    
    if not filepath.exists():
        print(f"❌ 文件 {filename} 不存在")
        return
    
    try:
        import pyperclip
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        pyperclip.copy(content)
        print(f"✅ 文件 {filename} 的内容已复制到剪贴板")
        print("现在可以在主应用中粘贴到目录文本区域")
    except ImportError:
        print("❌ 需要安装 pyperclip 来支持剪贴板功能")
        print("安装命令: pip install pyperclip")
    except Exception as e:
        print(f"❌ 复制到剪贴板失败: {e}")

def main():
    """主函数"""
    print("🎯 PDF书签生成器 - Demo示例加载器")
    print("=" * 60)
    
    if len(sys.argv) == 1:
        # 显示所有示例文件
        list_demo_files()
        
        print("🚀 使用方法:")
        print("1. 查看文件内容: python load_examples.py <文件名>")
        print("2. 复制到剪贴板: python load_examples.py <文件名> --copy")
        print("3. 示例:")
        print("   python load_examples.py simple_bookmarks.txt")
        print("   python load_examples.py full_bookmarks.txt --copy")
        
    elif len(sys.argv) == 2:
        # 显示指定文件内容
        filename = sys.argv[1]
        show_file_content(filename)
        
    elif len(sys.argv) == 3 and sys.argv[2] == "--copy":
        # 复制文件内容到剪贴板
        filename = sys.argv[1]
        copy_to_clipboard(filename)
        
    else:
        print("❌ 无效的参数")
        print("使用方法:")
        print("  python load_examples.py                    # 列出所有示例")
        print("  python load_examples.py <文件名>           # 显示文件内容")
        print("  python load_examples.py <文件名> --copy    # 复制到剪贴板")

if __name__ == "__main__":
    main() 