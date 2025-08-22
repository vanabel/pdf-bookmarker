#!/bin/bash

# PDF书签生成器 - macOS优化构建脚本
# 支持Intel Mac (x86_64)

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 PDF书签生成器 - macOS构建脚本${NC}"
echo "=================================="

# 检查系统架构
ARCH=$(uname -m)
echo -e "${BLUE}📱 系统架构: ${ARCH}${NC}"

if [ "$ARCH" != "x86_64" ]; then
    echo -e "${YELLOW}⚠️  警告: 此脚本专为Intel Mac (x86_64)优化${NC}"
    echo -e "${YELLOW}   当前架构: ${ARCH}${NC}"
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "构建已取消"
        exit 1
    fi
fi

# 检查系统版本
OS_VERSION=$(sw_vers -productVersion)
echo -e "${BLUE}🖥️  macOS版本: ${OS_VERSION}${NC}"

# 检查Python环境
echo -e "${BLUE}🐍 检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3未找到${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ Python版本: ${PYTHON_VERSION}${NC}"

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo -e "${GREEN}✅ 虚拟环境已激活: ${VIRTUAL_ENV}${NC}"
else
    echo -e "${YELLOW}⚠️  建议在虚拟环境中运行${NC}"
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "构建已取消"
        exit 1
    fi
fi

# 安装依赖
echo -e "${BLUE}📦 安装依赖...${NC}"
python3 -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo -e "${GREEN}✅ 依赖安装完成${NC}"

# 清理之前的构建
echo -e "${BLUE}🧹 清理之前的构建...${NC}"
rm -rf build dist __pycache__
find . -name "*.pyc" -delete
echo -e "${GREEN}✅ 清理完成${NC}"

# 检查必要文件
echo -e "${BLUE}🔍 检查必要文件...${NC}"
if [ ! -f "PDF书签生成器.spec" ]; then
    echo -e "${RED}❌ 未找到PDF书签生成器.spec文件${NC}"
    exit 1
fi

if [ ! -f "pdf_bookmarker_gs.py" ]; then
    echo -e "${RED}❌ 未找到pdf_bookmarker_gs.py文件${NC}"
    exit 1
fi

if [ ! -d "assets/icons" ]; then
    echo -e "${RED}❌ 未找到assets/icons目录${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 所有必要文件检查通过${NC}"

# 构建应用
echo -e "${BLUE}🔨 开始构建应用...${NC}"
pyinstaller "PDF书签生成器.spec"

# 验证构建结果
if [ ! -d "dist/PDF书签生成器.app" ]; then
    echo -e "${RED}❌ 构建失败：未找到应用文件${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 应用构建成功${NC}"

# 检查应用架构
echo -e "${BLUE}🔍 检查应用架构...${NC}"
APP_ARCH=$(file "dist/PDF书签生成器.app/Contents/MacOS/PDF书签生成器" | grep -o 'x86_64\|arm64' || echo "unknown")
echo -e "${BLUE}📱 应用架构: ${APP_ARCH}${NC}"

if [ "$APP_ARCH" = "x86_64" ]; then
    echo -e "${GREEN}✅ 应用架构正确 (Intel Mac兼容)${NC}"
elif [ "$APP_ARCH" = "arm64" ]; then
    echo -e "${YELLOW}⚠️  应用是ARM64架构，可能不兼容Intel Mac${NC}"
else
    echo -e "${YELLOW}⚠️  无法确定应用架构${NC}"
fi

# 创建发布包
echo -e "${BLUE}📦 创建发布包...${NC}"
cd dist
zip -r "PDF书签生成器_$(date +%Y%m%d_%H%M%S)_macOS_x86_64.zip" "PDF书签生成器.app"
cd ..

ZIP_FILE=$(ls -t dist/PDF书签生成器_*_macOS_x86_64.zip | head -1)
echo -e "${GREEN}✅ 发布包创建成功: ${ZIP_FILE}${NC}"

# 应用兼容性处理
echo -e "${BLUE}🔧 应用兼容性处理...${NC}"
cd dist

# 移除扩展属性（解决Gatekeeper问题）
echo "移除扩展属性..."
xattr -cr "PDF书签生成器.app"

# 添加Gatekeeper例外
echo "添加Gatekeeper例外..."
spctl --add --label 'Approved' "PDF书签生成器.app" 2>/dev/null || echo "Gatekeeper例外添加失败（可能需要管理员权限）"

cd ..

echo -e "${GREEN}✅ 兼容性处理完成${NC}"

# 显示结果
echo ""
echo -e "${GREEN}🎉 构建完成！${NC}"
echo "=================================="
echo -e "${BLUE}📱 应用位置: dist/PDF书签生成器.app${NC}"
echo -e "${BLUE}📦 发布包: ${ZIP_FILE}${NC}"
echo -e "${BLUE}💾 应用大小: $(du -sh "dist/PDF书签生成器.app" | cut -f1)${NC}"
echo ""
echo -e "${YELLOW}📋 使用说明:${NC}"
echo "1. 双击应用图标运行"
echo "2. 如果提示'无法打开'，请右键选择'打开'"
echo "3. 或在系统偏好设置 > 安全性与隐私中允许运行"
echo ""
echo -e "${GREEN}✅ 构建脚本执行完成${NC}"
