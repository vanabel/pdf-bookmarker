#!/bin/bash

# PDF书签生成器自动发布脚本
# 用法: ./scripts/create_release.sh <版本号> [发布说明文件]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查参数
if [ $# -lt 1 ]; then
    echo -e "${RED}错误: 请提供版本号${NC}"
    echo "用法: $0 <版本号> [发布说明文件]"
    echo "示例: $0 v1.3.0"
    echo "示例: $0 v1.3.0 RELEASE_NOTES_v1.3.0.md"
    exit 1
fi

VERSION=$1
RELEASE_NOTES_FILE=$2

# 验证版本号格式
if [[ ! $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}错误: 版本号格式不正确${NC}"
    echo "正确格式: v<主版本>.<次版本>.<修订版本>"
    echo "示例: v1.3.0, v2.0.1"
    exit 1
fi

echo -e "${BLUE}🚀 开始创建版本 $VERSION 的发布...${NC}"

# 检查当前分支
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${YELLOW}警告: 当前不在main分支，建议在main分支上发布${NC}"
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}错误: 有未提交的更改，请先提交或暂存${NC}"
    git status --short
    exit 1
fi

# 检查是否已经存在该版本标签
if git tag -l | grep -q "^$VERSION$"; then
    echo -e "${RED}错误: 版本 $VERSION 已经存在${NC}"
    exit 1
fi

# 生成发布说明
if [ -z "$RELEASE_NOTES_FILE" ]; then
    RELEASE_NOTES_FILE="RELEASE_NOTES_${VERSION}.md"
    
    if [ ! -f "$RELEASE_NOTES_FILE" ]; then
        echo -e "${YELLOW}未找到发布说明文件，从模板生成...${NC}"
        
        # 从模板生成发布说明
        if [ -f "docs/releases/RELEASE_NOTES_TEMPLATE.md" ]; then
            CURRENT_DATE=$(date +"%Y年%m月%d日")
            sed "s/{{VERSION}}/$VERSION/g; s/{{DATE}}/$CURRENT_DATE/g" docs/releases/RELEASE_NOTES_TEMPLATE.md > "$RELEASE_NOTES_FILE"
            echo -e "${GREEN}✓ 已生成发布说明文件: $RELEASE_NOTES_FILE${NC}"
        else
            echo -e "${RED}错误: 未找到模板文件 docs/releases/RELEASE_NOTES_TEMPLATE.md${NC}"
            exit 1
        fi
    fi
fi

# 检查发布说明文件是否存在
if [ ! -f "$RELEASE_NOTES_FILE" ]; then
    echo -e "${RED}错误: 发布说明文件不存在: $RELEASE_NOTES_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 使用发布说明文件: $RELEASE_NOTES_FILE${NC}"

# 显示发布说明预览
echo -e "${BLUE}📋 发布说明预览:${NC}"
echo "----------------------------------------"
head -20 "$RELEASE_NOTES_FILE"
if [ $(wc -l < "$RELEASE_NOTES_FILE") -gt 20 ]; then
    echo "..."
    echo "----------------------------------------"
    echo "完整内容请查看: $RELEASE_NOTES_FILE"
fi
echo "----------------------------------------"

# 确认发布
read -p "确认发布版本 $VERSION? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}已取消发布${NC}"
    exit 1
fi

# 添加发布说明文件
git add "$RELEASE_NOTES_FILE"

# 提交发布说明
git commit -m "📝 添加 $VERSION 版本发布说明

- 版本: $VERSION
- 发布说明: $RELEASE_NOTES_FILE
- 自动生成发布说明"

echo -e "${GREEN}✓ 已提交发布说明${NC}"

# 创建标签
git tag -a "$VERSION" -m "Release $VERSION

$(head -10 "$RELEASE_NOTES_FILE" | tail -9)"

echo -e "${GREEN}✓ 已创建标签 $VERSION${NC}"

# 推送更改和标签
echo -e "${BLUE}📤 推送更改到远程仓库...${NC}"
git push origin main
git push origin "$VERSION"

echo -e "${GREEN}🎉 版本 $VERSION 发布成功！${NC}"
echo ""
echo -e "${BLUE}下一步:${NC}"
echo "1. GitHub Actions 将自动构建应用"
echo "2. 自动创建 Release 并上传构建文件"
echo "3. 您可以在 GitHub 仓库的 Releases 页面查看"
echo ""
echo -e "${BLUE}查看状态:${NC}"
echo "https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^/]*\/[^/]*\).*/\1/')/actions"
echo ""
echo -e "${BLUE}查看发布:${NC}"
echo "https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^/]*\/[^/]*\).*/\1/')/releases"
