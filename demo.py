#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF书签生成器演示脚本
展示核心功能，不依赖GUI
"""

import re
import tempfile
import os
from pathlib import Path

def demo_toc_parsing():
    """演示目录解析功能"""
    print("=" * 50)
    print("演示：目录解析功能")
    print("=" * 50)
    
    # 示例目录内容
    sample_toc = """PREFACE V
PREFACE TO REVISED EDITION vii
Chapter I. INTRODUCTION
1. Outline of this book 1
2. Further remarks 4
3. Notation 5
Chapter II. MAXIMUM PRINCIPLES
1. The weak maximum principle 7
2. The strong maximum principle 10
3. A priori estimates 14
Notes 18
Exercises 18"""
    
    print("输入目录内容:")
    print(sample_toc)
    print()
    
    # 解析目录
    lines = sample_toc.strip().split('\n')
    bookmarks = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 匹配行末的页码
        match = re.search(r'(.*?)\s*(\d+)\s*$', line)
        if match:
            title = match.group(1).strip()
            page = int(match.group(2))
            bookmarks.append((title, page))
    
    print(f"解析结果：找到 {len(bookmarks)} 个书签")
    for i, (title, page) in enumerate(bookmarks, 1):
        print(f"  {i:2d}. {title:<35} (第{page:2d}页)")
    
    return bookmarks

def demo_pdfmarks_generation(bookmarks, offset=12):
    """演示PDF书签格式生成"""
    print("\n" + "=" * 50)
    print("演示：PDF书签格式生成")
    print("=" * 50)
    
    print(f"页面偏移设置：书签第1页对应PDF第{offset}页")
    print()
    
    # 生成PDF书签格式
    pdfmarks = []
    for title, adjusted_page, bookmark_offset in bookmarks:
        # 调整页码（Ghostscript从0开始计数）
        # adjusted_page已经包含了动态偏移，现在加上基础偏移
        final_page = adjusted_page + offset - 1
        pdfmark = f'[ /Title ({title}) /Page {final_page} /OUT pdfmark ]'
        pdfmarks.append(pdfmark)
    
    pdfmarks_content = '\n'.join(pdfmarks)
    
    print("生成的pdfmarks内容:")
    print(pdfmarks_content)
    
    return pdfmarks_content

def demo_ghostscript_command(input_pdf, output_pdf, pdfmarks_file):
    """演示Ghostscript命令"""
    print("\n" + "=" * 50)
    print("演示：Ghostscript命令")
    print("=" * 50)
    
    # 构建命令
    cmd = [
        'gs',
        '-dBATCH',
        '-dNOPAUSE',
        '-q',
        '-sDEVICE=pdfwrite',
        f'-sOutputFile={output_pdf}',
        input_pdf,
        pdfmarks_file
    ]
    
    print("完整的Ghostscript命令:")
    print(' '.join(cmd))
    print()
    
    print("命令参数说明:")
    print("  -dBATCH     : 批处理模式，完成后退出")
    print("  -dNOPAUSE   : 不暂停等待用户输入")
    print("  -q          : 安静模式，减少输出")
    print("  -sDEVICE=pdfwrite : 输出设备为PDF写入器")
    print(f"  -sOutputFile={output_pdf} : 输出文件名")
    print(f"  {input_pdf} : 输入PDF文件")
    print(f"  {pdfmarks_file} : 书签文件")
    
    return cmd

def demo_file_operations():
    """演示文件操作"""
    print("\n" + "=" * 50)
    print("演示：文件操作")
    print("=" * 50)
    
    # 模拟文件路径
    input_pdf = Path("/path/to/input.pdf")
    output_pdf = input_pdf.parent / f"{input_pdf.stem}_with_bookmarks.pdf"
    
    print(f"输入PDF文件: {input_pdf}")
    print(f"输出PDF文件: {output_pdf}")
    print()
    
    # 创建临时书签文件
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pdfmarks', 
                                       delete=False, encoding='utf-8') as f:
            f.write("示例书签内容")
            temp_file = f.name
        
        print(f"临时书签文件: {temp_file}")
        print("（实际应用中会自动清理此文件）")
        
        # 清理
        os.unlink(temp_file)
        
    except Exception as e:
        print(f"临时文件操作失败: {e}")

def main():
    """主演示函数"""
    print("PDF书签生成器功能演示")
    print("=" * 60)
    
    # 演示各个功能
    bookmarks = demo_toc_parsing()
    pdfmarks_content = demo_pdfmarks_generation(bookmarks)
    demo_ghostscript_command("input.pdf", "output_with_bookmarks.pdf", "toc.pdfmarks")
    demo_file_operations()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print()
    print("使用说明:")
    print("1. 运行主应用: python pdf_bookmarker_gs.py")
    print("2. 或使用脚本: ./run_app.sh (Linux/macOS) 或 run_app.bat (Windows)")
    print("3. 确保系统已安装Ghostscript")
    print("4. 按照GUI界面提示操作")

if __name__ == "__main__":
    main() 