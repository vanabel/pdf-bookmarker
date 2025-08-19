import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
import tempfile
import re
from pathlib import Path

class PDFBookmarkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF书签生成器 - 使用Ghostscript")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # 设置样式和主题
        self.setup_styles()
        self.setup_ui()
        
        # 设置窗口居中
        self.center_window()
        
    def setup_styles(self):
        """设置现代化的样式"""
        style = ttk.Style()
        
        # 尝试使用更现代的主题
        available_themes = style.theme_names()
        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'clam' in available_themes:
            style.theme_use('clam')
        else:
            style.theme_use('default')
        
        # 自定义样式
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#7f8c8d')
        
        # 按钮样式
        style.configure('Primary.TButton', 
                       font=('Arial', 10, 'bold'),
                       background='#3498db',
                       foreground='white')
        
        style.configure('Success.TButton',
                       font=('Arial', 10, 'bold'),
                       background='#27ae60',
                       foreground='white')
        
        style.configure('Warning.TButton',
                       font=('Arial', 10, 'bold'),
                       background='#f39c12',
                       foreground='white')
        
        style.configure('Danger.TButton',
                       font=('Arial', 10, 'bold'),
                       background='#e74c3c',
                       foreground='white')
        
        # 框架样式
        style.configure('Card.TFrame', relief='raised', borderwidth=1)
        style.configure('Info.TFrame', relief='sunken', borderwidth=1)
        
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """设置现代化的用户界面"""
        # 主容器
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 标题区域
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="📚 PDF书签生成器", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(title_frame, text="使用Ghostscript生成标准PDF书签", style='Info.TLabel')
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0), pady=(5, 0))
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_container, text="📁 输入文件", padding="15")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # PDF文件选择
        pdf_label = ttk.Label(file_frame, text="PDF文件:", style='Header.TLabel')
        pdf_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.pdf_path_var = tk.StringVar()
        pdf_entry = ttk.Entry(file_frame, textvariable=self.pdf_path_var, font=('Arial', 10))
        pdf_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=(0, 10))
        
        browse_btn = ttk.Button(file_frame, text="🔍 浏览", command=self.browse_pdf, style='Primary.TButton')
        browse_btn.grid(row=0, column=2, pady=(0, 10))
        
        # 配置列权重
        file_frame.columnconfigure(1, weight=1)
        
        # 设置区域
        settings_frame = ttk.LabelFrame(main_container, text="⚙️ 设置", padding="15")
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 页面偏移设置
        offset_label = ttk.Label(settings_frame, text="页面偏移:", style='Header.TLabel')
        offset_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        offset_desc_frame = ttk.Frame(settings_frame)
        offset_desc_frame.grid(row=0, column=1, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(offset_desc_frame, text="书签第1页对应PDF第", style='Info.TLabel').pack(side=tk.LEFT)
        self.offset_var = tk.StringVar(value="1")
        offset_spin = ttk.Spinbox(offset_desc_frame, from_=1, to=9999, textvariable=self.offset_var, 
                                 width=8, font=('Arial', 10))
        offset_spin.pack(side=tk.LEFT, padx=(5, 5))
        ttk.Label(offset_desc_frame, text="页", style='Info.TLabel').pack(side=tk.LEFT)
        
        # 调试模式开关
        self.debug_var = tk.BooleanVar(value=False)
        debug_check = ttk.Checkbutton(settings_frame, text="🐛 调试模式", 
                                     variable=self.debug_var, style='Info.TLabel')
        debug_check.grid(row=0, column=2, padx=(30, 0), pady=(0, 10))
        
        # 配置列权重
        settings_frame.columnconfigure(1, weight=1)
        
        # 目录输入区域
        toc_frame = ttk.LabelFrame(main_container, text="📝 目录内容", padding="15")
        toc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 目录说明
        toc_info = ttk.Label(toc_frame, text="支持格式: 标题 页码 | 标题 ..................... 页码 | <!---offset +/-数字--->", 
                            style='Info.TLabel')
        toc_info.pack(anchor=tk.W, pady=(0, 10))
        
        # 文本输入区域
        text_container = ttk.Frame(toc_frame)
        text_container.pack(fill=tk.BOTH, expand=True)
        
        self.toc_text = scrolledtext.ScrolledText(text_container, wrap=tk.WORD, 
                                                font=('Consolas', 10),
                                                bg='#f8f9fa', fg='#2c3e50',
                                                insertbackground='#3498db',
                                                selectbackground='#3498db',
                                                selectforeground='white')
        self.toc_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # 右侧按钮区域
        button_container = ttk.Frame(text_container)
        button_container.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # 示例按钮
        example_btn = ttk.Button(button_container, text="📖 加载示例", 
                                command=self.load_example, style='Info.TButton')
        example_btn.pack(fill=tk.X, pady=(0, 10))
        
        # 预览按钮
        preview_btn = ttk.Button(button_container, text="👁️ 预览书签", 
                                command=self.preview_bookmarks, style='Warning.TButton')
        preview_btn.pack(fill=tk.X, pady=(0, 10))
        
        # 清空按钮
        clear_btn = ttk.Button(button_container, text="🗑️ 清空", 
                              command=self.clear_all, style='Danger.TButton')
        clear_btn.pack(fill=tk.X, pady=(0, 10))
        
        # 主操作按钮区域
        action_frame = ttk.Frame(main_container)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 生成书签按钮
        generate_btn = ttk.Button(action_frame, text="🚀 生成书签", 
                                 command=self.generate_bookmarks, style='Success.TButton')
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 测试Ghostscript按钮
        test_btn = ttk.Button(action_frame, text="🧪 测试Ghostscript", 
                             command=self.test_ghostscript, style='Primary.TButton')
        test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 退出按钮
        exit_btn = ttk.Button(action_frame, text="❌ 退出", 
                             command=self.root.quit, style='Danger.TButton')
        exit_btn.pack(side=tk.RIGHT)
        
        # 状态栏
        status_frame = ttk.Frame(main_container, style='Info.TFrame')
        status_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.status_var = tk.StringVar(value="✅ 就绪 - 请选择PDF文件并输入目录内容")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                style='Info.TLabel', padding="8")
        status_label.pack(fill=tk.X)
        
    def browse_pdf(self):
        filename = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if filename:
            self.pdf_path_var.set(filename)
            
    def load_example(self):
        example_text = """<!---offset -13--->
PREFACE 5
PREFACE TO REVISED EDITION 7
<!---offset +13 --->
Chapter I. INTRODUCTION
1. Outline of this book 1
2. Further remarks 4
3. Notation 5
Chapter II. MAXIMUM PRINCIPLES
1. The weak maximum principle 7
2. The strong maximum principle 10
3. A priori estimates 14
Notes 18
Exercises 18
Chapter III. INTRODUCTION TO THEORY OF WEAK SOLUTIONS
1. The theory of weak derivatives 21
2. The method of continuity 29
3. Problems in small balls 30
4. Global existence and the Perron process 36
Notes 41
Exercises 42

# 提示：更多示例文件在 demo/ 目录中：
# - simple_bookmarks.txt (简单示例)
# - dots_format_bookmarks.txt (点线格式)
# - dynamic_offset_bookmarks.txt (动态偏移)
# - full_bookmarks.txt (完整学术书籍目录)"""
        self.toc_text.delete(1.0, tk.END)
        self.toc_text.insert(1.0, example_text)
        
    def clear_all(self):
        self.toc_text.delete(1.0, tk.END)
        self.pdf_path_var.set("")
        self.offset_var.set("1")
        self.status_var.set("🗑️ 已清空所有内容")
        
    def parse_toc(self, toc_text):
        """解析目录文本，提取标题和页码，支持动态偏移指令"""
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
                bookmarks.append((title, adjusted_page, current_offset))
                
        return bookmarks
        
    def generate_pdfmarks(self, bookmarks, offset):
        """生成PDF书签格式"""
        # 添加PostScript头部
        pdfmarks = ['%!PS']
        
        for title, adjusted_page, bookmark_offset in bookmarks:
            # 计算最终的PDF页码（Ghostscript从0开始计数）
            # adjusted_page已经包含了动态偏移，现在加上基础偏移
            final_page = adjusted_page + offset - 1
            
            # 清理标题中的特殊字符，避免PostScript语法错误
            clean_title = self.clean_title_for_postscript(title)
            
            pdfmark = f'[ /Title ({clean_title}) /Page {final_page} /OUT pdfmark'
            pdfmarks.append(pdfmark)
            
        return '\n'.join(pdfmarks)
        
    def clean_title_for_postscript(self, title):
        """清理标题，使其符合PostScript语法要求"""
        # 移除或转义可能导致PostScript语法错误的字符
        # PostScript字符串中需要转义的字符: ( ) \ 
        clean_title = title.replace('\\', '\\\\')  # 转义反斜杠
        clean_title = clean_title.replace('(', '\\(')  # 转义左括号
        clean_title = clean_title.replace(')', '\\)')  # 转义右括号
        
        # 移除其他可能导致问题的字符
        clean_title = clean_title.replace('\n', ' ')  # 换行符替换为空格
        clean_title = clean_title.replace('\r', ' ')  # 回车符替换为空格
        clean_title = clean_title.replace('\t', ' ')  # 制表符替换为空格
        
        # 移除首尾空格
        clean_title = clean_title.strip()
        
        return clean_title
        
    def check_ghostscript(self):
        """检查Ghostscript是否可用"""
        try:
            # 尝试运行ghostscript命令
            result = subprocess.run(['gs', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return True, result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
        # 尝试其他可能的命令名
        for cmd in ['gswin64c', 'gswin32c', 'gs']:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return True, result.stdout.strip()
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
                
        return False, None
        
    def generate_bookmarks(self):
        """生成PDF书签"""
        # 检查输入
        if not self.pdf_path_var.get():
            messagebox.showerror("错误", "请选择PDF文件")
            return
            
        if not self.toc_text.get(1.0, tk.END).strip():
            messagebox.showerror("错误", "请输入目录内容")
            return
            
        # 验证PDF文件
        input_pdf_path = Path(self.pdf_path_var.get())
        if not input_pdf_path.exists():
            messagebox.showerror("错误", f"PDF文件不存在:\n{input_pdf_path}")
            return
            
        if not input_pdf_path.is_file():
            messagebox.showerror("错误", f"选择的路径不是文件:\n{input_pdf_path}")
            return
            
        # 检查文件大小
        file_size = input_pdf_path.stat().st_size
        if file_size == 0:
            messagebox.showerror("错误", "PDF文件大小为0，可能已损坏")
            return
            
        if self.debug_var.get():
            print(f"PDF文件信息:")
            print(f"  路径: {input_pdf_path}")
            print(f"  大小: {file_size} 字节")
            print(f"  存在: {input_pdf_path.exists()}")
            print(f"  可读: {os.access(input_pdf_path, os.R_OK)}")
            
        try:
            offset = int(self.offset_var.get())
        except ValueError:
            messagebox.showerror("错误", "页面偏移必须是数字")
            return
            
        # 检查Ghostscript
        gs_available, gs_version = self.check_ghostscript()
        if not gs_available:
            messagebox.showerror("错误", 
                "未找到Ghostscript。请安装Ghostscript并确保它在系统PATH中。\n\n"
                "安装说明:\n"
                "Windows: 下载并安装Ghostscript\n"
                "macOS: brew install ghostscript\n"
                "Linux: sudo apt-get install ghostscript")
            return
            
        self.status_var.set(f"✅ 使用Ghostscript版本: {gs_version}")
        
        try:
            # 解析目录
            toc_text = self.toc_text.get(1.0, tk.END)
            bookmarks = self.parse_toc(toc_text)
            
            if not bookmarks:
                messagebox.showerror("错误", "无法解析目录内容，请检查格式")
                return
                
            # 生成PDF书签
            pdfmarks_content = self.generate_pdfmarks(bookmarks, offset)
            
            if self.debug_var.get():
                print(f"生成的pdfmarks内容:")
                print(pdfmarks_content)
                print(f"书签数量: {len(bookmarks)}")
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.pdfmarks', 
                                           delete=False, encoding='utf-8') as f:
                f.write(pdfmarks_content)
                pdfmarks_file = f.name
                
            # 生成输出文件名
            input_pdf = Path(self.pdf_path_var.get())
            output_pdf = input_pdf.parent / f"{input_pdf.stem}_with_bookmarks.pdf"
            
            # 检查输出目录权限
            if not os.access(input_pdf.parent, os.W_OK):
                messagebox.showerror("错误", f"没有输出目录的写入权限:\n{input_pdf.parent}")
                return
                
            if self.debug_var.get():
                print(f"输出文件信息:")
                print(f"  路径: {output_pdf}")
                print(f"  目录: {input_pdf.parent}")
                print(f"  目录可写: {os.access(input_pdf.parent, os.W_OK)}")
                print(f"  输出文件已存在: {output_pdf.exists()}")
            
            # 运行Ghostscript命令
            gs_cmd = self.get_ghostscript_command()
            cmd = [
                gs_cmd,
                '-dBATCH',
                '-dNOPAUSE',
                '-q',
                '-sDEVICE=pdfwrite',
                '-sOutputFile=' + str(output_pdf),
                str(input_pdf),
                '-f',  # 表示后面是PostScript文件
                pdfmarks_file
            ]
            
            self.status_var.set("🔄 正在生成PDF书签...")
            self.root.update()
            
            # 执行命令
            self.status_var.set("⚙️ 正在执行Ghostscript命令...")
            self.root.update()
            
            # 显示执行的命令
            cmd_str = ' '.join(cmd)
            if self.debug_var.get():
                print(f"执行命令: {cmd_str}")
                print(f"工作目录: {os.getcwd()}")
                print(f"输入PDF: {input_pdf}")
                print(f"输出PDF: {output_pdf}")
                print(f"书签文件: {pdfmarks_file}")
            
            # 执行命令并捕获详细输出
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            # 清理临时文件
            try:
                os.unlink(pdfmarks_file)
            except:
                pass
                
            if result.returncode == 0:
                messagebox.showinfo("成功", 
                    f"PDF书签已生成成功！\n\n"
                    f"输出文件: {output_pdf}\n"
                    f"书签数量: {len(bookmarks)}")
                self.status_var.set("🎉 书签生成完成！输出文件已保存")
            else:
                # 显示详细的错误信息
                error_msg = f"Ghostscript执行失败 (退出代码: {result.returncode})\n\n"
                error_msg += f"执行的命令:\n{cmd_str}\n\n"
                error_msg += f"标准输出:\n{result.stdout}\n\n"
                error_msg += f"错误输出:\n{result.stderr}\n\n"
                error_msg += f"临时书签文件内容:\n{pdfmarks_content}"
                
                # 创建详细的错误日志窗口
                self.show_error_log(error_msg)
                self.status_var.set("❌ 书签生成失败，请查看错误详情")
                
        except Exception as e:
            messagebox.showerror("❌ 错误", f"生成过程中发生错误:\n{str(e)}")
            self.status_var.set("❌ 书签生成失败，请查看错误详情")
            
    def get_ghostscript_command(self):
        """获取可用的Ghostscript命令"""
        for cmd in ['gs', 'gswin64c', 'gswin32c']:
            try:
                subprocess.run([cmd, '--version'], 
                              capture_output=True, timeout=5)
                return cmd
            except:
                continue
        return 'gs'  # 默认返回
        
    def show_error_log(self, error_msg):
        """显示美化的错误日志窗口"""
        # 创建新窗口
        error_window = tk.Toplevel(self.root)
        error_window.title("🚨 Ghostscript错误详情")
        error_window.geometry("900x650")
        error_window.resizable(True, True)
        error_window.configure(bg='#fff5f5')
        
        # 设置窗口图标
        try:
            error_window.iconbitmap('icon.ico')
        except:
            pass
        
        # 创建主框架
        main_frame = ttk.Frame(error_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 错误标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 错误图标和标题
        error_icon = ttk.Label(title_frame, text="🚨", font=("Arial", 24))
        error_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Ghostscript执行失败", 
                               style='Title.TLabel', foreground="#e74c3c")
        title_label.pack(side=tk.LEFT)
        
        # 错误说明
        error_desc = ttk.Label(title_frame, text="请查看详细错误信息并检查Ghostscript配置", 
                              style='Info.TLabel')
        error_desc.pack(side=tk.RIGHT, pady=(5, 0))
        
        # 创建文本区域容器
        text_container = ttk.LabelFrame(main_frame, text="📋 错误详情", padding="15")
        text_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 滚动文本区域
        text_widget = scrolledtext.ScrolledText(text_container, wrap=tk.WORD, 
                                              font=("Consolas", 10),
                                              bg='#ffffff', fg='#2c3e50',
                                              insertbackground='#e74c3c',
                                              selectbackground='#e74c3c',
                                              selectforeground='white',
                                              relief='flat',
                                              borderwidth=1)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # 插入错误信息
        text_widget.insert(tk.END, error_msg)
        text_widget.config(state=tk.DISABLED)  # 设置为只读
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 复制到剪贴板按钮
        def copy_to_clipboard():
            error_window.clipboard_clear()
            error_window.clipboard_append(error_msg)
            messagebox.showinfo("📋 提示", "错误信息已复制到剪贴板")
        
        copy_btn = ttk.Button(button_frame, text="📋 复制到剪贴板", 
                             command=copy_to_clipboard, style='Primary.TButton')
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 保存到文件按钮
        def save_to_file():
            filename = filedialog.asksaveasfilename(
                title="💾 保存错误日志",
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(error_msg)
                    messagebox.showinfo("✅ 成功", f"错误日志已保存到:\n{filename}")
                except Exception as e:
                    messagebox.showerror("❌ 错误", f"保存文件失败:\n{str(e)}")
        
        save_btn = ttk.Button(button_frame, text="💾 保存到文件", 
                             command=save_to_file, style='Success.TButton')
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 关闭按钮
        close_btn = ttk.Button(button_frame, text="❌ 关闭", 
                              command=error_window.destroy, style='Danger.TButton')
        close_btn.pack(side=tk.RIGHT)
        
        # 设置焦点
        error_window.focus_set()
        error_window.grab_set()  # 模态窗口
        
    def test_ghostscript(self):
        """测试Ghostscript连接和功能"""
        try:
            # 检查Ghostscript是否可用
            gs_available, gs_version = self.check_ghostscript()
            if not gs_available:
                messagebox.showerror("测试失败", "未找到Ghostscript")
                return
            
            # 获取可用的命令
            gs_cmd = self.get_ghostscript_command()
            
            # 测试基本功能
            test_results = []
            test_results.append(f"Ghostscript版本: {gs_version}")
            test_results.append(f"使用命令: {gs_cmd}")
            
            # 测试版本信息
            try:
                result = subprocess.run([gs_cmd, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    test_results.append(f"版本测试: ✓ 成功")
                    test_results.append(f"版本输出: {result.stdout.strip()}")
                else:
                    test_results.append(f"版本测试: ✗ 失败 (退出代码: {result.returncode})")
            except Exception as e:
                test_results.append(f"版本测试: ✗ 异常: {str(e)}")
            
            # 测试帮助信息
            try:
                result = subprocess.run([gs_cmd, '--help'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    test_results.append(f"帮助测试: ✓ 成功")
                else:
                    test_results.append(f"帮助测试: ✗ 失败 (退出代码: {result.returncode})")
            except Exception as e:
                test_results.append(f"帮助测试: ✗ 异常: {str(e)}")
            
            # 测试设备列表
            try:
                result = subprocess.run([gs_cmd, '-h'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    test_results.append(f"设备测试: ✓ 成功")
                    # 检查是否支持pdfwrite
                    if 'pdfwrite' in result.stdout:
                        test_results.append("pdfwrite设备: ✓ 支持")
                    else:
                        test_results.append("pdfwrite设备: ✗ 不支持")
                else:
                    test_results.append(f"设备测试: ✗ 失败 (退出代码: {result.returncode})")
            except Exception as e:
                test_results.append(f"设备测试: ✗ 异常: {str(e)}")
            
            # 显示美化的测试结果窗口
            self.show_test_results_window(test_results, gs_cmd)
            
        except Exception as e:
            messagebox.showerror("测试异常", f"测试过程中发生异常:\n{str(e)}")
    
    def show_test_results_window(self, test_results, gs_cmd):
        """显示美化的Ghostscript测试结果窗口"""
        # 创建新窗口
        test_window = tk.Toplevel(self.root)
        test_window.title("🧪 Ghostscript测试结果")
        test_window.geometry("800x600")
        test_window.resizable(True, True)
        test_window.configure(bg='#f0f8ff')
        
        # 设置窗口图标
        try:
            test_window.iconbitmap('icon.ico')
        except:
            pass
        
        # 创建主框架
        main_frame = ttk.Frame(test_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 测试图标和标题
        test_icon = ttk.Label(title_frame, text="🧪", font=("Arial", 24))
        test_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Ghostscript测试结果", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # 命令信息
        cmd_label = ttk.Label(title_frame, text=f"使用命令: {gs_cmd}", style='Info.TLabel')
        cmd_label.pack(side=tk.RIGHT, pady=(5, 0))
        
        # 创建结果容器
        results_container = ttk.LabelFrame(main_frame, text="📊 测试详情", padding="15")
        results_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 滚动文本区域
        text_widget = scrolledtext.ScrolledText(results_container, wrap=tk.WORD, 
                                              font=("Consolas", 10),
                                              bg='#ffffff', fg='#2c3e50',
                                              insertbackground='#3498db',
                                              selectbackground='#3498db',
                                              selectforeground='white',
                                              relief='flat',
                                              borderwidth=1)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # 插入测试结果
        for result in test_results:
            if "✓" in result:
                # 成功结果使用绿色
                text_widget.insert(tk.END, result + "\n", "success")
            elif "✗" in result:
                # 失败结果使用红色
                text_widget.insert(tk.END, result + "\n", "error")
            else:
                # 普通信息
                text_widget.insert(tk.END, result + "\n")
        
        # 配置标签样式
        text_widget.tag_configure("success", foreground="#27ae60", font=("Consolas", 10, "bold"))
        text_widget.tag_configure("error", foreground="#e74c3c", font=("Consolas", 10, "bold"))
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 复制结果按钮
        def copy_results():
            test_window.clipboard_clear()
            test_window.clipboard_append("\n".join(test_results))
            messagebox.showinfo("📋 提示", "测试结果已复制到剪贴板")
        
        copy_btn = ttk.Button(button_frame, text="📋 复制结果", 
                             command=copy_results, style='Primary.TButton')
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 保存结果按钮
        def save_results():
            filename = filedialog.asksaveasfilename(
                title="💾 保存测试结果",
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("\n".join(test_results))
                    messagebox.showinfo("✅ 成功", f"测试结果已保存到:\n{filename}")
                except Exception as e:
                    messagebox.showerror("❌ 错误", f"保存文件失败:\n{str(e)}")
        
        save_btn = ttk.Button(button_frame, text="💾 保存结果", 
                             command=save_results, style='Success.TButton')
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 关闭按钮
        close_btn = ttk.Button(button_frame, text="❌ 关闭", 
                              command=test_window.destroy, style='Danger.TButton')
        close_btn.pack(side=tk.RIGHT)
        
        # 设置焦点
        test_window.focus_set()
        
    def preview_bookmarks(self):
        """预览书签内容"""
        try:
            # 获取目录文本
            toc_text = self.toc_text.get(1.0, tk.END).strip()
            if not toc_text:
                messagebox.showwarning("警告", "请先输入目录内容")
                return
            
            # 获取页面偏移
            try:
                offset = int(self.offset_var.get())
            except ValueError:
                messagebox.showerror("错误", "页面偏移必须是数字")
                return
            
            # 解析目录
            bookmarks = self.parse_toc(toc_text)
            if not bookmarks:
                messagebox.showerror("错误", "无法解析目录内容")
                return
            
            # 生成预览内容
            preview_content = self.generate_preview_content(bookmarks, offset)
            
            # 显示预览窗口
            self.show_preview_window(preview_content, bookmarks, offset)
            
        except Exception as e:
            messagebox.showerror("预览错误", f"预览过程中发生错误:\n{str(e)}")
        
    def generate_preview_content(self, bookmarks, offset):
        """生成预览内容"""
        preview_lines = []
        preview_lines.append("=" * 60)
        preview_lines.append("书签预览")
        preview_lines.append("=" * 60)
        preview_lines.append(f"页面偏移: 书签第1页对应PDF第{offset}页")
        preview_lines.append(f"书签数量: {len(bookmarks)}")
        preview_lines.append("")
        
        # 添加书签列表
        preview_lines.append("书签列表:")
        preview_lines.append("-" * 40)
        
        for i, (title, adjusted_page, bookmark_offset) in enumerate(bookmarks, 1):
            final_page = adjusted_page + offset - 1
            offset_info = f" (偏移:{bookmark_offset:+d})" if bookmark_offset != 0 else ""
            preview_lines.append(f"{i:2d}. {title:<40} (调整后第{adjusted_page:2d}页 -> PDF第{final_page:2d}页){offset_info}")
        
        preview_lines.append("")
        preview_lines.append("=" * 60)
        preview_lines.append("生成的pdfmarks内容:")
        preview_lines.append("=" * 60)
        
        # 添加pdfmarks内容
        pdfmarks_content = self.generate_pdfmarks(bookmarks, offset)
        preview_lines.append(pdfmarks_content)
        
        return "\n".join(preview_lines)
        
    def show_preview_window(self, preview_content, bookmarks, offset):
        """显示美化的预览窗口"""
        # 创建新窗口
        preview_window = tk.Toplevel(self.root)
        preview_window.title("👁️ 书签预览和验证")
        preview_window.geometry("1000x750")
        preview_window.resizable(True, True)
        preview_window.configure(bg='#f8f9fa')
        
        # 设置窗口图标
        try:
            preview_window.iconbitmap('icon.ico')
        except:
            pass
        
        # 创建主框架
        main_frame = ttk.Frame(preview_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="👁️ 书签预览和验证", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # 统计信息
        stats_frame = ttk.Frame(title_frame)
        stats_frame.pack(side=tk.RIGHT)
        
        ttk.Label(stats_frame, text=f"📊 书签数量: {len(bookmarks)}", 
                 style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 15))
        ttk.Label(stats_frame, text=f"⚙️ 页面偏移: {offset}", 
                 style='Info.TLabel').pack(side=tk.LEFT)
        
        # 创建文本区域容器
        text_container = ttk.LabelFrame(main_frame, text="📋 预览内容", padding="15")
        text_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 滚动文本区域
        text_widget = scrolledtext.ScrolledText(text_container, wrap=tk.WORD, 
                                              font=("Consolas", 10),
                                              bg='#ffffff', fg='#2c3e50',
                                              insertbackground='#3498db',
                                              selectbackground='#3498db',
                                              selectforeground='white',
                                              relief='flat',
                                              borderwidth=1)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # 插入预览内容
        text_widget.insert(tk.END, preview_content)
        
        # 标记潜在错误
        self.mark_potential_errors(text_widget, bookmarks, offset)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 保存到文件按钮
        def save_preview():
            filename = filedialog.asksaveasfilename(
                title="💾 保存预览内容",
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(preview_content)
                    messagebox.showinfo("✅ 成功", f"预览内容已保存到:\n{filename}")
                except Exception as e:
                    messagebox.showerror("❌ 错误", f"保存文件失败:\n{str(e)}")
        
        save_btn = ttk.Button(button_frame, text="💾 保存预览", 
                             command=save_preview, style='Primary.TButton')
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 复制到剪贴板按钮
        def copy_preview():
            preview_window.clipboard_clear()
            preview_window.clipboard_append(preview_content)
            messagebox.showinfo("📋 提示", "预览内容已复制到剪贴板")
        
        copy_btn = ttk.Button(button_frame, text="📋 复制内容", 
                             command=copy_preview, style='Success.TButton')
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 关闭按钮
        ttk.Button(button_frame, text="关闭", 
                  command=preview_window.destroy).pack(side=tk.LEFT, padx=5)
        
        # 设置焦点
        preview_window.focus_set()
        
    def mark_potential_errors(self, text_widget, bookmarks, offset):
        """标记潜在错误"""
        # 配置标签样式
        text_widget.tag_configure("error", background="lightcoral", foreground="darkred")
        text_widget.tag_configure("warning", background="lightyellow", foreground="darkorange")
        text_widget.tag_configure("info", background="lightblue", foreground="darkblue")
        
        # 检查潜在问题
        issues = []
        
        # 检查页码问题
        for i, (title, adjusted_page, bookmark_offset) in enumerate(bookmarks):
            # 计算实际的PDF页码 (adjusted_page已经包含了动态偏移)
            final_page = adjusted_page + offset - 1
            
            if adjusted_page == 0:
                issues.append((f"第{i+1}个书签页码为0: {title}", "error"))
            elif final_page < 0:
                issues.append((f"第{i+1}个书签: {title} (调整后第{adjusted_page}页 -> PDF第{final_page}页, 页码为负)", "error"))
            elif final_page > 1000:
                issues.append((f"第{i+1}个书签: {title} (调整后第{adjusted_page}页 -> PDF第{final_page}页, 页码过大)", "warning"))
        
        # 检查标题长度
        for i, (title, adjusted_page, bookmark_offset) in enumerate(bookmarks):
            if len(title) > 100:
                issues.append((f"第{i+1}个书签标题过长: {title[:50]}...", "warning"))
            elif len(title.strip()) == 0:
                issues.append((f"第{i+1}个书签标题为空", "error"))
        
        # 检查页码连续性
        pages = [adjusted_page for _, adjusted_page, _ in bookmarks]
        if len(pages) > 1:
            sorted_pages = sorted(pages)
            if pages != sorted_pages:
                issues.append(("书签页码顺序不正确，建议按页码排序", "warning"))
        
        # 检查偏移设置
        if offset < 1:
            issues.append(("页面偏移小于1，可能导致页码错误", "error"))
        elif offset > 1000:
            issues.append(("页面偏移过大，请检查设置", "warning"))
        
        # 在文本末尾添加问题列表
        if issues:
            text_widget.insert(tk.END, "\n\n" + "=" * 60 + "\n")
            text_widget.insert(tk.END, "潜在问题和建议:\n")
            text_widget.insert(tk.END, "=" * 60 + "\n")
            
            for issue, tag_type in issues:
                text_widget.insert(tk.END, f"• {issue}\n", tag_type)
        else:
            text_widget.insert(tk.END, "\n\n" + "=" * 60 + "\n")
            text_widget.insert(tk.END, "✓ 未发现明显问题，书签格式正确\n", "info")
            text_widget.insert(tk.END, "=" * 60 + "\n")

def main():
    root = tk.Tk()
    app = PDFBookmarkerApp(root)
    
    # 设置窗口图标（如果有的话）
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
        
    root.mainloop()

if __name__ == "__main__":
    main() 