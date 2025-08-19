#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ghostscript调试工具
用于诊断Ghostscript相关的问题
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def print_header(title):
    """打印标题"""
    print("=" * 60)
    print(f" {title}")
    print("=" * 60)

def print_section(title):
    """打印章节标题"""
    print(f"\n--- {title} ---")

def check_system_info():
    """检查系统信息"""
    print_header("系统信息")
    
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    print(f"PATH环境变量: {os.environ.get('PATH', '未设置')}")

def check_ghostscript_installation():
    """检查Ghostscript安装"""
    print_header("Ghostscript安装检查")
    
    # 可能的命令名
    possible_commands = ['gs', 'gswin64c', 'gswin32c', 'ghostscript']
    
    for cmd in possible_commands:
        print_section(f"测试命令: {cmd}")
        
        try:
            # 测试版本
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✓ 命令可用: {cmd}")
                print(f"  版本: {result.stdout.strip()}")
                
                # 测试帮助
                help_result = subprocess.run([cmd, '--help'], 
                                           capture_output=True, text=True, timeout=10)
                if help_result.returncode == 0:
                    print(f"  帮助: ✓ 可用")
                else:
                    print(f"  帮助: ✗ 不可用")
                
                # 测试设备列表
                device_result = subprocess.run([cmd, '-h'], 
                                             capture_output=True, text=True, timeout=10)
                if device_result.returncode == 0:
                    print(f"  设备列表: ✓ 可用")
                    if 'pdfwrite' in device_result.stdout:
                        print(f"  pdfwrite设备: ✓ 支持")
                    else:
                        print(f"  pdfwrite设备: ✗ 不支持")
                else:
                    print(f"  设备列表: ✗ 不可用")
                
                return cmd, result.stdout.strip()
                
            else:
                print(f"✗ 命令不可用: {cmd}")
                print(f"  退出代码: {result.returncode}")
                if result.stderr:
                    print(f"  错误: {result.stderr.strip()}")
                    
        except subprocess.TimeoutExpired:
            print(f"✗ 命令超时: {cmd}")
        except FileNotFoundError:
            print(f"✗ 命令未找到: {cmd}")
        except Exception as e:
            print(f"✗ 命令异常: {cmd} - {str(e)}")
    
    return None, None

def test_ghostscript_functionality(cmd):
    """测试Ghostscript功能"""
    if not cmd:
        print_section("跳过功能测试 - 未找到可用的Ghostscript命令")
        return
    
    print_header("Ghostscript功能测试")
    
    # 测试1: 创建简单的PDF
    print_section("测试1: 创建简单PDF")
    try:
        test_pdf = "test_output.pdf"
        gs_cmd = [
            cmd, '-dBATCH', '-dNOPAUSE', '-q',
            '-sDEVICE=pdfwrite',
            f'-sOutputFile={test_pdf}',
            '-c', 'showpage'
        ]
        
        print(f"执行命令: {' '.join(gs_cmd)}")
        result = subprocess.run(gs_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ 成功创建测试PDF")
            if os.path.exists(test_pdf):
                size = os.path.getsize(test_pdf)
                print(f"  文件大小: {size} 字节")
                # 清理测试文件
                os.remove(test_pdf)
                print("  已清理测试文件")
            else:
                print("✗ 测试PDF文件未创建")
        else:
            print(f"✗ 创建测试PDF失败")
            print(f"  退出代码: {result.returncode}")
            if result.stdout:
                print(f"  标准输出: {result.stdout}")
            if result.stderr:
                print(f"  错误输出: {result.stderr}")
                
    except Exception as e:
        print(f"✗ 测试异常: {str(e)}")
    
    # 测试2: 测试pdfwrite设备
    print_section("测试2: pdfwrite设备")
    try:
        gs_cmd = [cmd, '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-f']
        print(f"执行命令: {' '.join(gs_cmd)}")
        result = subprocess.run(gs_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ pdfwrite设备测试成功")
        else:
            print(f"✗ pdfwrite设备测试失败")
            print(f"  退出代码: {result.returncode}")
            if result.stderr:
                print(f"  错误输出: {result.stderr}")
                
    except Exception as e:
        print(f"✗ 测试异常: {str(e)}")

def test_pdf_processing(cmd):
    """测试PDF处理功能"""
    if not cmd:
        print_section("跳过PDF处理测试 - 未找到可用的Ghostscript命令")
        return
    
    print_header("PDF处理测试")
    
    # 检查是否有测试PDF文件
    test_files = list(Path('.').glob('*.pdf'))
    if not test_files:
        print("未找到测试PDF文件，跳过PDF处理测试")
        return
    
    test_pdf = test_files[0]
    print(f"使用测试文件: {test_pdf}")
    
    # 测试PDF信息
    print_section("测试PDF信息")
    try:
        gs_cmd = [cmd, '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=nullpage', '-f', str(test_pdf)]
        print(f"执行命令: {' '.join(gs_cmd)}")
        result = subprocess.run(gs_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ PDF文件读取成功")
        else:
            print(f"✗ PDF文件读取失败")
            print(f"  退出代码: {result.returncode}")
            if result.stderr:
                print(f"  错误输出: {result.stderr}")
                
    except Exception as e:
        print(f"✗ 测试异常: {str(e)}")

def generate_test_pdfmarks():
    """生成测试用的pdfmarks文件"""
    print_header("生成测试pdfmarks文件")
    
    # 使用正确的PostScript格式
    test_content = """%!PS
[ /Title (Test Bookmark 1) /Page 0 /OUT pdfmark
[ /Title (Test Bookmark 2) /Page 1 /OUT pdfmark
[ /Title (Test Bookmark 3) /Page 2 /OUT pdfmark"""
    
    test_file = "test.pdfmarks"
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"✓ 测试pdfmarks文件已创建: {test_file}")
        print("文件内容:")
        print(test_content)
        
        return test_file
        
    except Exception as e:
        print(f"✗ 创建测试文件失败: {str(e)}")
        return None

def test_pdfmarks_integration(cmd, pdfmarks_file):
    """测试pdfmarks集成"""
    if not cmd or not pdfmarks_file:
        print_section("跳过pdfmarks集成测试")
        return
    
    print_header("pdfmarks集成测试")
    
    # 检查是否有测试PDF文件
    test_files = list(Path('.').glob('*.pdf'))
    if not test_files:
        print("未找到测试PDF文件，跳过集成测试")
        return
    
    test_pdf = test_files[0]
    output_pdf = "test_with_bookmarks.pdf"
    
    print(f"输入PDF: {test_pdf}")
    print(f"输出PDF: {output_pdf}")
    print(f"书签文件: {pdfmarks_file}")
    
    try:
        gs_cmd = [
            cmd, '-dBATCH', '-dNOPAUSE', '-q',
            '-sDEVICE=pdfwrite',
            f'-sOutputFile={output_pdf}',
            str(test_pdf),
            '-f',  # 表示后面是PostScript文件
            pdfmarks_file
        ]
        
        print(f"执行命令: {' '.join(gs_cmd)}")
        result = subprocess.run(gs_cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✓ 成功添加书签")
            if os.path.exists(output_pdf):
                size = os.path.getsize(output_pdf)
                print(f"  输出文件大小: {size} 字节")
                # 清理测试文件
                os.remove(output_pdf)
                print("  已清理测试输出文件")
            else:
                print("✗ 输出PDF文件未创建")
        else:
            print(f"✗ 添加书签失败")
            print(f"  退出代码: {result.returncode}")
            if result.stdout:
                print(f"  标准输出: {result.stdout}")
            if result.stderr:
                print(f"  错误输出: {result.stderr}")
                
    except Exception as e:
        print(f"✗ 测试异常: {str(e)}")

def cleanup_test_files():
    """清理测试文件"""
    print_header("清理测试文件")
    
    test_files = ['test.pdfmarks']
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✓ 已清理: {file}")
            except Exception as e:
                print(f"✗ 清理失败: {file} - {str(e)}")
        else:
            print(f"- 文件不存在: {file}")

def main():
    """主函数"""
    print("Ghostscript调试工具")
    print("用于诊断PDF书签生成器的问题")
    
    try:
        # 系统信息
        check_system_info()
        
        # 检查Ghostscript安装
        cmd, version = check_ghostscript_installation()
        
        # 功能测试
        test_ghostscript_functionality(cmd)
        
        # PDF处理测试
        test_pdf_processing(cmd)
        
        # 生成测试pdfmarks
        pdfmarks_file = generate_test_pdfmarks()
        
        # pdfmarks集成测试
        test_pdfmarks_integration(cmd, pdfmarks_file)
        
        # 清理测试文件
        cleanup_test_files()
        
        print_header("调试完成")
        if cmd:
            print(f"✓ 找到可用的Ghostscript: {cmd} {version}")
            print("建议: 检查PDF文件格式和权限")
        else:
            print("✗ 未找到可用的Ghostscript")
            print("建议: 安装Ghostscript并确保在PATH中")
            
    except KeyboardInterrupt:
        print("\n\n用户中断调试")
    except Exception as e:
        print(f"\n\n调试过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 