#!/bin/bash
# macOS专用打包脚本

echo "🍎 macOS PDF书签生成器打包脚本"
echo "=================================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 检查PyInstaller
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "📦 安装PyInstaller..."
    pip install pyinstaller
fi

# 检查主应用文件
if [ ! -f "pdf_bookmarker_gs.py" ]; then
    echo "❌ 主应用文件不存在: pdf_bookmarker_gs.py"
    exit 1
fi

echo "🔨 开始构建应用..."

# 构建命令
pyinstaller \
    --onefile \
    --windowed \
    --name="PDF书签生成器" \
    --add-data="demo:demo" \
    --hidden-import=tkinter \
    --hidden-import=tkinter.ttk \
    --clean \
    pdf_bookmarker_gs.py

if [ $? -eq 0 ]; then
    echo "✅ 应用构建成功！"
    
    # 创建启动脚本
    cat > "启动PDF书签生成器.sh" << 'EOF'
#!/bin/bash
echo "正在启动PDF书签生成器..."
cd "$(dirname "$0")"
./dist/PDF书签生成器
EOF
    
    chmod +x "启动PDF书签生成器.sh"
    echo "✅ 创建启动脚本: 启动PDF书签生成器.sh"
    
    # 创建使用说明
    cat > "应用使用说明.txt" << 'EOF'
PDF书签生成器 - 应用使用说明
=====================================

🎯 应用已成功打包！

📁 文件说明:
- dist/PDF书签生成器 (macOS可执行文件)
- 启动PDF书签生成器.sh (启动脚本)

🚀 使用方法:
1. 双击启动脚本或直接运行可执行文件
2. 确保系统已安装Ghostscript: brew install ghostscript
3. 按照界面提示操作

⚠️  注意事项:
- 首次运行可能需要几秒钟启动
- 确保有足够的磁盘空间
- 如果遇到问题，检查Ghostscript安装

🔧 系统要求:
- macOS 10.10+
- Ghostscript (必需): brew install ghostscript
- 至少100MB可用磁盘空间

📞 技术支持:
如有问题，请查看项目README.md或提交Issue
EOF
    
    echo "✅ 创建应用使用说明: 应用使用说明.txt"
    
    echo ""
    echo "🎉 打包完成！"
    echo "📁 可执行文件位置: dist/PDF书签生成器"
    echo "📖 查看应用使用说明.txt了解详细信息"
    echo ""
    echo "🚀 运行应用:"
    echo "   ./启动PDF书签生成器.sh"
    echo "   或直接运行: ./dist/PDF书签生成器"
    
else
    echo "❌ 构建失败"
    exit 1
fi 