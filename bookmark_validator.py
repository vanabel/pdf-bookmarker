#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书签验证和预览工具
用于验证书签格式、预览内容和标记潜在问题
"""

import re
import sys
from pathlib import Path

class BookmarkValidator:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.info = []
        
    def validate_toc_text(self, toc_text, offset=1):
        """验证目录文本"""
        print("=" * 60)
        print("书签验证和预览")
        print("=" * 60)
        
        # 解析目录
        bookmarks = self.parse_toc(toc_text)
        if not bookmarks:
            print("❌ 无法解析目录内容")
            return False
            
        print(f"📚 成功解析 {len(bookmarks)} 个书签")
        print(f"📄 页面偏移: 书签第1页对应PDF第{offset}页")
        print()
        
        # 验证书签
        self.validate_bookmarks(bookmarks, offset)
        
        # 显示预览
        self.show_preview(bookmarks, offset)
        
        # 显示问题总结
        self.show_validation_summary()
        
        return len(self.issues) == 0
        
    def parse_toc(self, toc_text):
        """解析目录文本，支持动态偏移指令"""
        lines = toc_text.strip().split('\n')
        bookmarks = []
        current_offset = 0  # 当前偏移值
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            # 检查是否是偏移指令 - 使用HTML注释风格格式
            # 格式: <!---offset +/-数字--->
            offset_match = re.search(r'<!---\s*offset\s*([+-]?\d+)\s*--->', line)
            if offset_match:
                offset_change = int(offset_match.group(1))
                current_offset += offset_change
                print(f"第{line_num}行: 检测到偏移指令 '{line.strip()}'，当前偏移调整为: {current_offset}")
                continue
                
            # 匹配包含点线的格式：标题 ......................... 页码
            # 或者简单的格式：标题 页码（支持负数）
            match = re.search(r'(.*?)\s*[\.\s]*(-?\d+)\s*$', line)
            if match:
                title = match.group(1).strip()
                page = int(match.group(2))
                # 应用当前偏移
                adjusted_page = page + current_offset
                bookmarks.append((title, adjusted_page, line_num, current_offset))
            else:
                self.warnings.append(f"第{line_num}行无法解析: '{line}' (缺少页码)")
                
        return bookmarks
        
    def validate_bookmarks(self, bookmarks, offset):
        """验证书签内容"""
        print("🔍 验证书签内容...")
        print("-" * 40)
        
        for i, (title, adjusted_page, line_num, bookmark_offset) in enumerate(bookmarks):
            # 计算实际的PDF页码 (adjusted_page已经包含了动态偏移)
            final_page = adjusted_page + offset - 1
            offset_info = f" (偏移:{bookmark_offset:+d})" if bookmark_offset != 0 else ""
            print(f"书签 {i+1}: {title} (调整后第{adjusted_page}页 -> PDF第{final_page}页){offset_info}")
            
            # 验证页码
            if adjusted_page == 0:
                self.issues.append(f"第{line_num}行: 页码为0 ({adjusted_page})")
            elif final_page < 0:
                self.issues.append(f"第{line_num}行: 页码为负 ({adjusted_page} -> {final_page})")
            elif final_page > 1000:
                self.warnings.append(f"第{line_num}行: 页码过大 ({adjusted_page} -> {final_page})")
                
            # 验证标题
            if not title.strip():
                self.issues.append(f"第{line_num}行: 标题为空")
            elif len(title) > 100:
                self.warnings.append(f"第{line_num}行: 标题过长 ({len(title)}字符)")
                
            # 检查特殊字符
            special_chars = self.check_special_characters(title)
            if special_chars:
                self.warnings.append(f"第{line_num}行: 包含特殊字符 {special_chars}")
                
        # 验证页码连续性
        pages = [adjusted_page for _, adjusted_page, _, _ in bookmarks]
        if len(pages) > 1:
            sorted_pages = sorted(pages)
            if pages != sorted_pages:
                self.warnings.append("页码顺序不正确，建议按页码排序")
                
        # 验证偏移设置
        if offset < 1:
            self.issues.append("页面偏移小于1，可能导致页码错误")
        elif offset > 1000:
            self.warnings.append("页面偏移过大，请检查设置")
            
        print()
        
    def check_special_characters(self, title):
        """检查特殊字符"""
        special_chars = []
        for char in title:
            if char in '()\\':
                special_chars.append(char)
        return special_chars if special_chars else None
        
    def show_preview(self, bookmarks, offset):
        """显示预览"""
        print("📋 书签预览:")
        print("-" * 40)
        
        for i, (title, adjusted_page, _, bookmark_offset) in enumerate(bookmarks, 1):
            final_page = adjusted_page + offset - 1
            offset_info = f" (偏移:{bookmark_offset:+d})" if bookmark_offset != 0 else ""
            print(f"{i:2d}. {title:<40} (调整后第{adjusted_page:2d}页 -> PDF第{final_page:2d}页){offset_info}")
            
        print()
        print("📄 生成的pdfmarks内容:")
        print("-" * 40)
        
        pdfmarks_content = self.generate_pdfmarks(bookmarks, offset)
        print(pdfmarks_content)
        print()
        
    def generate_pdfmarks(self, bookmarks, offset):
        """生成pdfmarks内容"""
        pdfmarks = ['%!PS']
        
        for title, adjusted_page, _, bookmark_offset in bookmarks:  # bookmarks包含(title, adjusted_page, line_num, bookmark_offset)
            # 计算最终的PDF页码（Ghostscript从0开始计数）
            # adjusted_page已经包含了动态偏移，现在加上基础偏移
            final_page = adjusted_page + offset - 1
            clean_title = self.clean_title_for_postscript(title)
            pdfmark = f'[ /Title ({clean_title}) /Page {final_page} /OUT pdfmark'
            pdfmarks.append(pdfmark)
            
        return '\n'.join(pdfmarks)
        
    def clean_title_for_postscript(self, title):
        """清理标题，使其符合PostScript语法"""
        clean_title = title.replace('\\', '\\\\')
        clean_title = clean_title.replace('(', '\\(')
        clean_title = clean_title.replace(')', '\\)')
        clean_title = clean_title.replace('\n', ' ')
        clean_title = clean_title.replace('\r', ' ')
        clean_title = clean_title.replace('\t', ' ')
        return clean_title.strip()
        
    def show_validation_summary(self):
        """显示验证总结"""
        print("=" * 60)
        print("验证总结")
        print("=" * 60)
        
        if self.issues:
            print("❌ 发现错误:")
            for issue in self.issues:
                print(f"  • {issue}")
            print()
            
        if self.warnings:
            print("⚠️  发现警告:")
            for warning in self.warnings:
                print(f"  • {warning}")
            print()
            
        if self.info:
            print("ℹ️  信息:")
            for info in self.info:
                print(f"  • {info}")
            print()
            
        if not self.issues and not self.warnings:
            print("✅ 验证通过！未发现明显问题")
        elif not self.issues:
            print("✅ 验证通过！但有一些警告需要注意")
        else:
            print("❌ 验证失败！请修复上述错误后重试")
            
        print()
        
    def save_validation_report(self, filename, toc_text, offset):
        """保存验证报告"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("书签验证报告\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("原始目录内容:\n")
                f.write("-" * 30 + "\n")
                f.write(toc_text)
                f.write("\n\n")
                
                f.write("验证结果:\n")
                f.write("-" * 30 + "\n")
                
                if self.issues:
                    f.write("错误:\n")
                    for issue in self.issues:
                        f.write(f"  • {issue}\n")
                    f.write("\n")
                    
                if self.warnings:
                    f.write("警告:\n")
                    for warning in self.warnings:
                        f.write(f"  • {warning}\n")
                    f.write("\n")
                    
                if self.info:
                    f.write("信息:\n")
                    for info in self.info:
                        f.write(f"  • {info}\n")
                    f.write("\n")
                    
            print(f"📄 验证报告已保存到: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ 保存报告失败: {str(e)}")
            return False

def main():
    """主函数"""
    print("书签验证和预览工具")
    print("用于验证PDF书签格式和预览内容")
    print()
    
    # 示例目录内容
    example_toc = """PREFACE V
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
    
    # 创建验证器
    validator = BookmarkValidator()
    
    # 验证示例
    print("🔍 验证示例目录...")
    success = validator.validate_toc_text(example_toc, offset=12)
    
    # 保存报告
    if success:
        validator.save_validation_report("validation_report.txt", example_toc, 12)
    
    print("\n" + "=" * 60)
    print("验证完成！")
    print("=" * 60)
    
    if success:
        print("✅ 书签格式正确，可以生成PDF")
    else:
        print("❌ 请修复错误后重试")
        
    print("\n使用说明:")
    print("1. 在主应用中点击'预览书签'按钮")
    print("2. 或运行此脚本验证目录格式")
    print("3. 修复所有错误后再生成PDF")

if __name__ == "__main__":
    main() 