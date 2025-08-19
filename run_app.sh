#!/bin/bash

echo "PDF书签生成器启动脚本"
echo "========================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "错误: 未找到Python，请先安装Python 3.7+"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# 检查虚拟环境是否存在
if [ -f "venv/bin/activate" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
else
    echo "虚拟环境不存在，使用系统Python..."
fi

# 检查Ghostscript是否安装
if ! command -v gs &> /dev/null; then
    echo "警告: 未找到Ghostscript，应用可能无法正常工作"
    echo "请安装Ghostscript:"
    echo "  macOS: brew install ghostscript"
    echo "  Ubuntu/Debian: sudo apt-get install ghostscript"
    echo "  CentOS/RHEL: sudo yum install ghostscript"
    echo ""
    read -p "是否继续运行应用? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 运行应用
echo "启动PDF书签生成器..."
$PYTHON_CMD pdf_bookmarker_gs.py

# 检查退出状态
if [ $? -ne 0 ]; then
    echo ""
    echo "应用异常退出，错误代码: $?"
fi

# 如果使用了虚拟环境，退出虚拟环境
if [ -f "venv/bin/activate" ]; then
    deactivate
fi 