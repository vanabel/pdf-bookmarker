#!/bin/bash

# 🚀 PDF书签生成器 - 优化的macOS构建脚本
# 专门解决标题栏图标显示问题

set -e  # 遇到错误立即退出

echo "🎨 PDF书签生成器 - 优化的macOS构建"
echo "=================================="

# 检查Python环境
echo "🔍 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未找到，请先安装Python3"
    exit 1
fi

python_version=$(python3 --version)
echo "✅ Python版本: $python_version"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "🔧 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装/更新依赖
echo "📦 安装/更新依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 检查PyInstaller
if ! pip show pyinstaller &> /dev/null; then
    echo "📦 安装PyInstaller..."
    pip install pyinstaller
else
    echo "✅ PyInstaller已安装"
fi

# 检查图标文件
echo "🔍 检查图标文件..."
if [ ! -f "assets/icons/icon_256.png" ]; then
    echo "❌ 未找到256x256图标文件"
    echo "💡 请确保assets/icons/icon_256.png存在"
    exit 1
fi

if [ ! -f "assets/icons/icon_32.png" ]; then
    echo "❌ 未找到32x32图标文件"
    echo "💡 请先运行python generate_32x32_icon.py生成32x32图标"
    exit 1
fi

echo "✅ 所有图标文件检查通过"

# 清理之前的构建
echo "🧹 清理之前的构建..."
rm -rf build dist __pycache__

# 使用优化的spec文件构建
echo "🚀 开始构建应用..."
echo "📋 使用优化的配置文件: PDF书签生成器.spec"

pyinstaller --clean "PDF书签生成器.spec"

# 检查构建结果
if [ -d "dist/PDF书签生成器.app" ]; then
    echo "✅ 应用构建成功！"
    echo "📁 应用位置: dist/PDF书签生成器.app"
    
    # 显示应用信息
    echo "🔍 应用信息:"
    ls -la "dist/PDF书签生成器.app/Contents/MacOS/"
    
    # 检查图标是否正确嵌入
    echo "🎨 检查图标嵌入..."
    if [ -f "dist/PDF书签生成器.app/Contents/Resources/icon_256.png" ]; then
        echo "✅ 图标文件已正确嵌入"
    else
        echo "⚠️ 图标文件可能未正确嵌入"
    fi
    
    # 创建启动脚本
    echo "📝 创建启动脚本..."
    cat > "启动PDF书签生成器_优化版.sh" << 'EOF'
#!/bin/bash
# 🚀 PDF书签生成器启动脚本（优化版）

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PATH="$SCRIPT_DIR/dist/PDF书签生成器.app"

echo "🎨 启动PDF书签生成器..."
echo "📁 应用路径: $APP_PATH"

if [ -d "$APP_PATH" ]; then
    echo "✅ 应用文件存在，正在启动..."
    open "$APP_PATH"
else
    echo "❌ 应用文件不存在: $APP_PATH"
    echo "💡 请先运行构建脚本: ./build_macos_optimized.sh"
    exit 1
fi
EOF

    chmod +x "启动PDF书签生成器_优化版.sh"
    echo "✅ 启动脚本已创建: 启动PDF书签生成器_优化版.sh"
    
else
    echo "❌ 应用构建失败"
    echo "🔍 请检查构建日志和错误信息"
    exit 1
fi

echo ""
echo "🎉 构建完成！"
echo "=================================="
echo "📱 应用位置: dist/PDF书签生成器.app"
echo "🚀 启动命令: ./启动PDF书签生成器_优化版.sh"
echo "🔧 手动启动: open dist/PDF书签生成器.app"
echo ""
echo "💡 现在标题栏图标应该能正确显示了！"
echo "🎯 如果仍有问题，请检查macOS系统设置"
