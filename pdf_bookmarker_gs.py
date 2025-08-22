import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
import tempfile
import re
from pathlib import Path

# 导入图标配置
try:
    from assets.icons.icon_config import icon_config
except ImportError:
    # 如果图标配置不可用，创建默认配置
    icon_config = None

class PDFBookmarkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF书签生成器 - 使用Ghostscript")
        self.root.geometry("1200x800")  # 增加窗口大小
        self.root.minsize(1000, 700)    # 增加最小尺寸
        
        # 设置窗口图标
        self.setup_window_icon()
        
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
        
        # 自定义样式 - 增加字体大小
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Arial', 12), foreground='#7f8c8d')
        
        # 按钮样式 - 使用更简单的样式确保可见性
        style.configure('Primary.TButton', 
                       font=('Arial', 12, 'bold'))
        
        style.configure('Success.TButton',
                       font=('Arial', 12, 'bold'))
        
        style.configure('Warning.TButton',
                       font=('Arial', 12, 'bold'))
        
        style.configure('Danger.TButton',
                       font=('Arial', 12, 'bold'))
        
        # 框架样式
        style.configure('Card.TFrame', relief='raised', borderwidth=1)
        style.configure('Info.TFrame', relief='sunken', borderwidth=1)
        
        # 修复复选框样式
        style.configure('TCheckbutton', font=('Arial', 12))
        
    def setup_window_icon(self):
        """设置窗口图标"""
        if icon_config:
            try:
                # 根据平台选择合适的图标
                icon_path = icon_config.get_platform_icon()
                if icon_path:
                    if sys.platform == "darwin":  # macOS
                        # macOS使用PhotoImage
                        icon_image = tk.PhotoImage(file=icon_path)
                        self.root.iconphoto(True, icon_image)
                    elif sys.platform == "win32":  # Windows
                        # Windows使用iconbitmap
                        self.root.iconbitmap(icon_path)
                    else:  # Linux
                        # Linux使用PhotoImage
                        icon_image = tk.PhotoImage(file=icon_path)
                        self.root.iconphoto(True, icon_image)
                    print(f"✅ 窗口图标设置成功: {icon_path}")
                else:
                    print("⚠️ 未找到合适的图标文件")
            except Exception as e:
                print(f"❌ 设置窗口图标失败: {e}")
        else:
            print("⚠️ 图标配置不可用，使用默认图标")
    
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
        self.pdf_entry = ttk.Entry(file_frame, textvariable=self.pdf_path_var, font=('Arial', 12))
        self.pdf_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=(0, 10))
        
        # 设置占位符文本和状态
        self.placeholder_text = "/Users/vanabel/Zotero/storage/RIPGDEB6/DonaldsonKronheimer_1990_The_geometry_of_four-manifolds.pdf"
        self.is_placeholder = True
        self.setup_placeholder()
        
        # 启用粘贴功能
        self.pdf_entry.bind('<Control-v>', self.paste_pdf_path)
        self.pdf_entry.bind('<Command-v>', self.paste_pdf_path)  # macOS支持
        
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
                                 width=8, font=('Arial', 12))
        offset_spin.pack(side=tk.LEFT, padx=(5, 5))
        ttk.Label(offset_desc_frame, text="页", style='Info.TLabel').pack(side=tk.LEFT)
        
        # 调试模式开关
        self.debug_var = tk.BooleanVar(value=False)
        debug_check = ttk.Checkbutton(settings_frame, text="🐛 调试模式", 
                                     variable=self.debug_var)
        debug_check.grid(row=0, column=2, padx=(30, 0), pady=(0, 10))
        
        # 调试模式说明
        debug_desc = ttk.Label(settings_frame, 
                              text="(启用后会在控制台显示详细执行信息，帮助排查问题)", 
                              style='Info.TLabel')
        debug_desc.grid(row=1, column=2, padx=(30, 0), pady=(0, 10))
        
        # 配置列权重
        settings_frame.columnconfigure(1, weight=1)
        
        # 目录输入区域
        toc_frame = ttk.LabelFrame(main_container, text="📝 目录内容", padding="15")
        toc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 目录说明
        toc_info = ttk.Label(toc_frame, text="支持格式: 标题 页码 | 标题 ..................... 页码 | <!---offset +/-数字--->", 
                            style='Info.TLabel')
        toc_info.pack(anchor=tk.W, pady=(0, 10))
        
        # 文本输入区域 - 限制高度，确保不覆盖按钮
        text_container = ttk.Frame(toc_frame)
        text_container.pack(fill=tk.BOTH, expand=True)
        
        self.toc_text = scrolledtext.ScrolledText(text_container, wrap=tk.WORD, 
                                                font=('Consolas', 12),
                                                bg='#f8f9fa', fg='#2c3e50',
                                                insertbackground='#3498db',
                                                selectbackground='#3498db',
                                                selectforeground='white',
                                                height=15)  # 限制高度
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
        
        # 主操作按钮区域 - 完全重新设计
        action_frame = ttk.LabelFrame(main_container, text="🎯 操作按钮", padding="20")
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 使用网格布局确保按钮位置
        # 清除原始书签按钮
        clear_bookmarks_btn = tk.Button(action_frame, text="🧹 清除原始书签", 
                                       command=self.clear_original_bookmarks, 
                                       font=('Arial', 14, 'bold'),
                                       bg='#f39c12', fg='black',
                                       relief='raised', bd=3,
                                       padx=30, pady=10)
        clear_bookmarks_btn.grid(row=0, column=0, padx=(0, 20), pady=10)
        
        # 生成书签按钮
        generate_btn = tk.Button(action_frame, text="🚀 生成书签", 
                                command=self.generate_bookmarks, 
                                font=('Arial', 14, 'bold'),
                                bg='#27ae60', fg='black',
                                relief='raised', bd=3,
                                padx=30, pady=10)
        generate_btn.grid(row=0, column=1, padx=(0, 20), pady=10)
        
        # 测试工具按钮
        test_btn = tk.Button(action_frame, text="🧪 测试工具", 
                            command=self.test_all_tools, 
                            font=('Arial', 14, 'bold'),
                            bg='#3498db', fg='black',
                            relief='raised', bd=3,
                            padx=30, pady=10)
        test_btn.grid(row=0, column=2, padx=(0, 20), pady=10)
        
        # 退出按钮
        exit_btn = tk.Button(action_frame, text="❌ 退出", 
                            command=self.root.quit, 
                            font=('Arial', 14, 'bold'),
                            bg='#e74c3c', fg='black',
                            relief='raised', bd=3,
                            padx=30, pady=10)
        exit_btn.grid(row=0, column=3, padx=(0, 0), pady=10)
        
        # 配置列权重
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        action_frame.columnconfigure(2, weight=1)
        action_frame.columnconfigure(3, weight=1)
        
        # 等待布局完成后再获取位置信息
        self.root.after(200, self.show_button_positions, action_frame, clear_bookmarks_btn, generate_btn, test_btn, exit_btn)
        
        # 在窗口显示完成后强制更新
        self.root.after(500, self.force_update_layout, action_frame, clear_bookmarks_btn, generate_btn, test_btn, exit_btn)
        
        # 状态栏
        status_frame = ttk.Frame(main_container, style='Info.TFrame')
        status_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 创建状态栏容器
        status_container = ttk.Frame(status_frame)
        status_container.pack(fill=tk.X, padx=8, pady=8)
        
        # 左侧状态信息
        self.status_var = tk.StringVar(value="✅ 就绪 - 请选择PDF文件并输入目录内容")
        status_label = ttk.Label(status_container, textvariable=self.status_var, 
                                style='Info.TLabel')
        status_label.pack(side=tk.LEFT)
        
        # 右侧Ghostscript状态
        self.gs_status_var = tk.StringVar(value="")
        gs_status_label = ttk.Label(status_container, textvariable=self.gs_status_var, 
                                   style='Info.TLabel')
        gs_status_label.pack(side=tk.RIGHT)
        
        # 初始化时检查Ghostscript状态
        self.update_ghostscript_status()
        
        # 调试：检查按钮是否正确创建
        if self.debug_var.get():
            print("按钮创建状态:")
            print(f"  清除书签按钮: {clear_bookmarks_btn.winfo_exists()}")
            print(f"  生成书签按钮: {generate_btn.winfo_exists()}")
            print(f"  测试按钮: {test_btn.winfo_exists()}")
            print(f"  退出按钮: {exit_btn.winfo_exists()}")
            print(f"  动作框架: {action_frame.winfo_exists()}")
        
    def browse_pdf(self):
        filename = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if filename:
            # 清除占位符状态
            if self.is_placeholder:
                self.is_placeholder = False
                self.pdf_entry.config(foreground='black')
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
        # 首先检查系统PATH中的命令
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
        
        # 检查常见的安装路径
        common_paths = self.get_common_ghostscript_paths()
        for path in common_paths:
            if os.path.exists(path):
                try:
                    result = subprocess.run([path, '--version'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        return True, result.stdout.strip()
                except:
                    continue
                
        return False, None
    
    def check_qpdf(self):
        """检查qpdf是否可用"""
        try:
            # 尝试运行qpdf命令
            result = subprocess.run(['qpdf', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return True, result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
        # 尝试其他可能的命令名
        for cmd in ['qpdf', 'qpdf.exe']:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return True, result.stdout.strip()
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
                
        return False, None
    
    def get_common_ghostscript_paths(self):
        """获取常见的Ghostscript安装路径"""
        paths = []
        
        # 获取当前脚本所在目录
        if getattr(sys, 'frozen', False):
            # 打包后的可执行文件
            base_path = os.path.dirname(sys.executable)
        else:
            # 开发环境
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        # 检查当前目录和子目录
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.lower() in ['gs', 'gswin64c', 'gswin32c']:
                    paths.append(os.path.join(root, file))
        
        # Windows常见路径
        if os.name == 'nt':
            program_files = os.environ.get('PROGRAMFILES', 'C:\\Program Files')
            program_files_x86 = os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')
            
            gs_paths = [
                os.path.join(program_files, 'gs', 'gs*', 'bin', 'gswin64c.exe'),
                os.path.join(program_files_x86, 'gs', 'gs*', 'bin', 'gswin32c.exe'),
                os.path.join(program_files, 'gs', 'gs*', 'bin', 'gs.exe'),
                os.path.join(program_files_x86, 'gs', 'gs*', 'bin', 'gs.exe'),
            ]
            
            for pattern in gs_paths:
                import glob
                matches = glob.glob(pattern)
                paths.extend(matches)
        
        # macOS常见路径
        elif sys.platform == 'darwin':
            mac_paths = [
                '/usr/local/bin/gs',
                '/opt/homebrew/bin/gs',
                '/usr/bin/gs'
            ]
            paths.extend(mac_paths)
        
        # Linux常见路径
        elif sys.platform.startswith('linux'):
            linux_paths = [
                '/usr/bin/gs',
                '/usr/local/bin/gs',
                '/opt/gs/bin/gs'
            ]
            paths.extend(linux_paths)
        
        return paths
        
    def generate_bookmarks(self):
        """生成PDF书签"""
        # 检查输入
        if not self.pdf_path_var.get() or self.is_placeholder:
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
            self.update_ghostscript_status()  # 更新状态栏
            return
            
        self.status_var.set(f"✅ 使用Ghostscript版本: {gs_version}")
        self.update_ghostscript_status()  # 更新状态栏
        
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
        # 首先检查系统PATH中的命令
        for cmd in ['gs', 'gswin64c', 'gswin32c']:
            try:
                subprocess.run([cmd, '--version'], 
                              capture_output=True, timeout=5)
                return cmd
            except:
                continue
        
        # 检查常见安装路径
        common_paths = self.get_common_ghostscript_paths()
        for path in common_paths:
            if os.path.exists(path):
                try:
                    subprocess.run([path, '--version'], 
                                  capture_output=True, timeout=5)
                    return path
                except:
                    continue
        
        # 如果都找不到，返回默认命令
        return 'gs'
        
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
        
    def test_all_tools(self):
        """测试所有工具（Ghostscript和qpdf）"""
        try:
            test_results = []
            test_results.append("=" * 60)
            test_results.append("PDF书签生成器 - 工具测试报告")
            test_results.append("=" * 60)
            test_results.append("")
            
            # 测试Ghostscript
            test_results.append("🔧 Ghostscript 测试")
            test_results.append("-" * 30)
            gs_available, gs_version = self.check_ghostscript()
            if gs_available:
                gs_cmd = self.get_ghostscript_command()
                test_results.append(f"✓ Ghostscript已找到")
                test_results.append(f"  版本: {gs_version}")
                test_results.append(f"  命令: {gs_cmd}")
                
                # 测试版本信息
                try:
                    result = subprocess.run([gs_cmd, '--version'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        test_results.append(f"  版本测试: ✓ 成功")
                    else:
                        test_results.append(f"  版本测试: ✗ 失败 (退出代码: {result.returncode})")
                except Exception as e:
                    test_results.append(f"  版本测试: ✗ 异常: {str(e)}")
                
                # 测试pdfwrite设备
                try:
                    result = subprocess.run([gs_cmd, '-h'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0 and 'pdfwrite' in result.stdout:
                        test_results.append("  pdfwrite设备: ✓ 支持")
                    else:
                        test_results.append("  pdfwrite设备: ✗ 不支持")
                except Exception:
                    test_results.append("  pdfwrite设备: ✗ 测试失败")
            else:
                test_results.append("✗ Ghostscript未找到")
                test_results.append("  状态: 无法检测到Ghostscript")
                test_results.append("  建议: 请安装Ghostscript并确保添加到PATH")
            
            test_results.append("")
            
            # 测试qpdf
            test_results.append("🔧 qpdf 测试")
            test_results.append("-" * 30)
            qpdf_available, qpdf_version = self.check_qpdf()
            if qpdf_available:
                test_results.append(f"✓ qpdf已找到")
                test_results.append(f"  版本: {qpdf_version}")
                test_results.append(f"  命令: qpdf")
                
                # 测试版本信息
                try:
                    result = subprocess.run(['qpdf', '--version'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        test_results.append(f"  版本测试: ✓ 成功")
                    else:
                        test_results.append(f"  版本测试: ✗ 失败 (退出代码: {result.returncode})")
                except Exception as e:
                    test_results.append(f"  版本测试: ✗ 异常: {str(e)}")
                
                # 测试帮助信息
                try:
                    result = subprocess.run(['qpdf', '--help'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        test_results.append("  帮助测试: ✓ 成功")
                    else:
                        test_results.append("  帮助测试: ✗ 失败")
                except Exception:
                    test_results.append("  帮助测试: ✗ 测试失败")
                    
            else:
                test_results.append("✗ qpdf未找到")
                test_results.append("  状态: 无法检测到qpdf")
                test_results.append("  建议: 请安装qpdf并确保添加到PATH")
            
            test_results.append("")
            
            # 功能可用性总结
            test_results.append("📊 功能可用性总结")
            test_results.append("-" * 30)
            if gs_available and qpdf_available:
                test_results.append("✓ 所有功能完全可用")
                test_results.append("  🚀 生成书签: 可用 (需要Ghostscript)")
                test_results.append("  🧹 清除原始书签: 可用 (需要qpdf)")
                test_results.append("  📝 建议: 您可以使用所有功能")
            elif gs_available and not qpdf_available:
                test_results.append("⚠️ 部分功能可用")
                test_results.append("  🚀 生成书签: 可用 (Ghostscript已安装)")
                test_results.append("  🧹 清除原始书签: 不可用 (缺少qpdf)")
                test_results.append("  📝 建议: 安装qpdf以使用清除书签功能")
            elif not gs_available and qpdf_available:
                test_results.append("⚠️ 部分功能可用")
                test_results.append("  🚀 生成书签: 不可用 (缺少Ghostscript)")
                test_results.append("  🧹 清除原始书签: 可用 (qpdf已安装)")
                test_results.append("  📝 建议: 安装Ghostscript以使用生成书签功能")
            else:
                test_results.append("✗ 无法使用主要功能")
                test_results.append("  🚀 生成书签: 不可用 (缺少Ghostscript)")
                test_results.append("  🧹 清除原始书签: 不可用 (缺少qpdf)")
                test_results.append("  📝 建议: 请安装Ghostscript和qpdf")
            
            test_results.append("")
            test_results.append("=" * 60)
            
            # 显示综合测试结果窗口
            self.show_comprehensive_test_window(test_results, gs_available, qpdf_available)
            
        except Exception as e:
            messagebox.showerror("测试异常", f"测试过程中发生异常:\n{str(e)}")
    
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
    
    def show_comprehensive_test_window(self, test_results, gs_available, qpdf_available):
        """显示综合工具测试结果窗口"""
        # 创建新窗口
        test_window = tk.Toplevel(self.root)
        test_window.title("🧪 工具测试报告")
        test_window.geometry("900x700")
        test_window.resizable(True, True)
        
        # 根据测试结果设置背景色
        if gs_available and qpdf_available:
            bg_color = '#f0fff0'  # 浅绿色 - 全部可用
        elif gs_available or qpdf_available:
            bg_color = '#fff8dc'  # 浅黄色 - 部分可用
        else:
            bg_color = '#ffe4e1'  # 浅红色 - 都不可用
            
        test_window.configure(bg=bg_color)
        
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
        
        title_label = ttk.Label(title_frame, text="工具测试报告", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # 状态指示器
        if gs_available and qpdf_available:
            status_text = "✓ 所有工具可用"
            status_color = "#27ae60"
        elif gs_available or qpdf_available:
            status_text = "⚠️ 部分工具可用"
            status_color = "#f39c12"
        else:
            status_text = "✗ 工具缺失"
            status_color = "#e74c3c"
            
        status_label = ttk.Label(title_frame, text=status_text, 
                                font=('Arial', 14, 'bold'), foreground=status_color)
        status_label.pack(side=tk.RIGHT, pady=(5, 0))
        
        # 创建结果容器
        results_container = ttk.LabelFrame(main_frame, text="📊 测试详情", padding="15")
        results_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 滚动文本区域
        text_widget = scrolledtext.ScrolledText(results_container, wrap=tk.WORD, 
                                              font=("Consolas", 11),
                                              bg='#ffffff', fg='#2c3e50',
                                              insertbackground='#3498db',
                                              selectbackground='#3498db',
                                              selectforeground='white',
                                              relief='flat',
                                              borderwidth=1)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # 插入测试结果并应用样式
        for result in test_results:
            if "✓" in result and ("成功" in result or "可用" in result or "支持" in result):
                # 成功结果使用绿色
                text_widget.insert(tk.END, result + "\n", "success")
            elif "✗" in result and ("失败" in result or "不可用" in result or "不支持" in result or "未找到" in result):
                # 失败结果使用红色
                text_widget.insert(tk.END, result + "\n", "error")
            elif "⚠️" in result:
                # 警告结果使用橙色
                text_widget.insert(tk.END, result + "\n", "warning")
            elif result.startswith("🔧") or result.startswith("📊"):
                # 标题使用蓝色
                text_widget.insert(tk.END, result + "\n", "header")
            elif "建议:" in result or "📝" in result:
                # 建议使用紫色
                text_widget.insert(tk.END, result + "\n", "suggestion")
            else:
                # 普通信息
                text_widget.insert(tk.END, result + "\n")
        
        # 配置标签样式
        text_widget.tag_configure("success", foreground="#27ae60", font=("Consolas", 11, "bold"))
        text_widget.tag_configure("error", foreground="#e74c3c", font=("Consolas", 11, "bold"))
        text_widget.tag_configure("warning", foreground="#f39c12", font=("Consolas", 11, "bold"))
        text_widget.tag_configure("header", foreground="#3498db", font=("Consolas", 12, "bold"))
        text_widget.tag_configure("suggestion", foreground="#9b59b6", font=("Consolas", 11, "italic"))
        
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
                title="💾 保存测试报告",
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("\n".join(test_results))
                    messagebox.showinfo("✅ 成功", f"测试报告已保存到:\n{filename}")
                except Exception as e:
                    messagebox.showerror("❌ 错误", f"保存文件失败:\n{str(e)}")
        
        save_btn = ttk.Button(button_frame, text="💾 保存报告", 
                             command=save_results, style='Success.TButton')
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 安装指南按钮
        def show_install_guide():
            guide_text = ""
            if not gs_available:
                guide_text += "🔧 Ghostscript 安装指南:\n"
                guide_text += "• Windows: 下载官方安装包并运行\n"
                guide_text += "• macOS: brew install ghostscript\n"
                guide_text += "• Linux: sudo apt-get install ghostscript\n\n"
            
            if not qpdf_available:
                guide_text += "🔧 qpdf 安装指南:\n"
                guide_text += "• Windows: 下载官方安装包并运行\n"
                guide_text += "• macOS: brew install qpdf\n"
                guide_text += "• Linux: sudo apt-get install qpdf\n\n"
            
            if guide_text:
                guide_text += "安装完成后请重启应用并重新测试。"
                messagebox.showinfo("📚 安装指南", guide_text)
            else:
                messagebox.showinfo("✅ 提示", "所有工具都已正确安装！")
        
        if not (gs_available and qpdf_available):
            install_btn = ttk.Button(button_frame, text="📚 安装指南", 
                                   command=show_install_guide, style='Warning.TButton')
            install_btn.pack(side=tk.LEFT, padx=(0, 10))
        
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

    def update_ghostscript_status(self):
        """更新Ghostscript状态栏信息"""
        gs_available, gs_version = self.check_ghostscript()
        if gs_available:
            self.gs_status_var.set(f"✅ 已找到Ghostscript: {gs_version}")
        else:
            self.gs_status_var.set("❌ 未找到Ghostscript。请安装Ghostscript并确保它在系统PATH中。")

    def setup_placeholder(self):
        """设置placeholder效果"""
        # 显示占位符文本
        self.pdf_path_var.set(self.placeholder_text)
        self.pdf_entry.config(foreground='gray')
        
        # 绑定事件
        self.pdf_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.pdf_entry.bind('<FocusOut>', self.on_entry_focus_out)
        self.pdf_entry.bind('<Key>', self.on_entry_key)
    
    def on_entry_focus_in(self, event):
        """输入框获得焦点时"""
        if self.is_placeholder:
            self.pdf_path_var.set("")
            self.pdf_entry.config(foreground='black')
            self.is_placeholder = False
    
    def on_entry_focus_out(self, event):
        """输入框失去焦点时"""
        if not self.pdf_path_var.get().strip():
            self.pdf_path_var.set(self.placeholder_text)
            self.pdf_entry.config(foreground='gray')
            self.is_placeholder = True
    
    def on_entry_key(self, event):
        """按键事件处理"""
        if self.is_placeholder:
            # 如果当前是占位符状态，任何按键都清除占位符
            self.pdf_path_var.set("")
            self.pdf_entry.config(foreground='black')
            self.is_placeholder = False
    
    def paste_pdf_path(self, event):
        """处理粘贴PDF路径"""
        try:
            # 获取剪贴板内容
            pasted_text = self.root.clipboard_get()
            
            # 清除占位符状态
            if self.is_placeholder:
                self.is_placeholder = False
                self.pdf_entry.config(foreground='black')
            
            # 检查是否是文件路径
            if os.path.exists(pasted_text) and pasted_text.lower().endswith('.pdf'):
                self.pdf_path_var.set(pasted_text)
                messagebox.showinfo("📋 提示", f"PDF路径已粘贴: {pasted_text}")
            else:
                messagebox.showwarning("警告", "粘贴的文本不是有效的PDF文件路径。")
        except tk.TclError:
            messagebox.showwarning("警告", "剪贴板为空或无法访问。")

    def show_button_positions(self, action_frame, clear_bookmarks_btn, generate_btn, test_btn, exit_btn):
        """显示按钮位置信息"""
        print(f"按钮区域位置: x={action_frame.winfo_x()}, y={action_frame.winfo_y()}")
        print(f"按钮区域大小: width={action_frame.winfo_width()}, height={action_frame.winfo_height()}")
        print(f"清除书签按钮位置: x={clear_bookmarks_btn.winfo_x()}, y={clear_bookmarks_btn.winfo_y()}")
        print(f"生成按钮位置: x={generate_btn.winfo_x()}, y={generate_btn.winfo_y()}")
        print(f"测试按钮位置: x={test_btn.winfo_x()}, y={test_btn.winfo_y()}")
        print(f"退出按钮位置: x={exit_btn.winfo_x()}, y={exit_btn.winfo_y()}")

    def force_update_layout(self, action_frame, clear_bookmarks_btn, generate_btn, test_btn, exit_btn):
        """强制更新布局，确保按钮位置正确"""
        self.root.update_idletasks()
        self.root.update()
        print("布局已强制更新。")
        self.show_button_positions(action_frame, clear_bookmarks_btn, generate_btn, test_btn, exit_btn)
    
    def clear_original_bookmarks(self):
        """清除PDF原始书签"""
        # 检查输入
        if not self.pdf_path_var.get() or self.is_placeholder:
            messagebox.showerror("错误", "请先选择PDF文件")
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
        
        # 检查qpdf是否可用
        qpdf_available, qpdf_version = self.check_qpdf()
        if not qpdf_available:
            messagebox.showerror("错误", 
                "未找到qpdf。请安装qpdf并确保它在系统PATH中。\n\n"
                "安装说明:\n"
                "Windows: 下载并安装qpdf\n"
                "macOS: brew install qpdf\n"
                "Linux: sudo apt-get install qpdf")
            return
            
        self.status_var.set(f"✅ 使用qpdf版本: {qpdf_version}")
        
        try:
            # 生成输出文件名
            output_pdf = input_pdf_path.parent / f"{input_pdf_path.stem}_no_bookmarks.pdf"
            
            # 检查输出目录权限
            if not os.access(input_pdf_path.parent, os.W_OK):
                messagebox.showerror("错误", f"没有输出目录的写入权限:\n{input_pdf_path.parent}")
                return
                
            if self.debug_var.get():
                print(f"清除书签信息:")
                print(f"  输入PDF: {input_pdf_path}")
                print(f"  输出PDF: {output_pdf}")
                print(f"  使用qpdf: {qpdf_version}")
            
            # 运行qpdf命令清除书签
            cmd = [
                'qpdf',
                '--empty',
                '--pages', str(input_pdf_path), '1-z',
                '--', str(output_pdf)
            ]
            
            self.status_var.set("🔄 正在清除原始书签...")
            self.root.update()
            
            # 显示执行的命令
            cmd_str = ' '.join(cmd)
            if self.debug_var.get():
                print(f"执行命令: {cmd_str}")
                print(f"工作目录: {os.getcwd()}")
            
            # 执行命令并捕获详细输出
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                messagebox.showinfo("成功", 
                    f"PDF原始书签已清除成功！\n\n"
                    f"输出文件: {output_pdf}\n"
                    f"原文件: {input_pdf_path}")
                self.status_var.set("🎉 原始书签清除完成！输出文件已保存")
                
                # 询问是否要更新输入路径为清理后的文件
                if messagebox.askyesno("更新路径", 
                    f"是否将输入路径更新为清理后的文件？\n{output_pdf}"):
                    self.pdf_path_var.set(str(output_pdf))
                    if self.is_placeholder:
                        self.is_placeholder = False
                        self.pdf_entry.config(foreground='black')
            else:
                # 显示详细的错误信息
                error_msg = f"qpdf执行失败 (退出代码: {result.returncode})\n\n"
                error_msg += f"执行的命令:\n{cmd_str}\n\n"
                error_msg += f"标准输出:\n{result.stdout}\n\n"
                error_msg += f"错误输出:\n{result.stderr}"
                
                messagebox.showerror("❌ 错误", error_msg)
                self.status_var.set("❌ 原始书签清除失败，请查看错误详情")
                
        except Exception as e:
            messagebox.showerror("❌ 错误", f"清除过程中发生错误:\n{str(e)}")
            self.status_var.set("❌ 原始书签清除失败，请查看错误详情")

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