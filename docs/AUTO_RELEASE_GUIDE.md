# 🚀 自动发布指南

本指南介绍如何使用GitHub Actions自动发布PDF书签生成器的新版本。

## 📋 概述

当您推送新的版本标签时，GitHub Actions会自动：
1. 构建macOS应用
2. 创建Release
3. 上传构建的zip文件
4. 使用对应的发布说明

## 🔧 设置

### 1. 文件结构
```
.github/
  workflows/
    auto-release.yml          # GitHub Actions工作流
scripts/
  create_release.sh          # 自动发布脚本
RELEASE_NOTES_TEMPLATE.md    # 发布说明模板
RELEASE_NOTES_v1.2.0.md     # 具体版本发布说明
```

### 2. 权限要求
- 确保GitHub仓库启用了Actions
- 确保有推送标签的权限
- 确保`GITHUB_TOKEN`有创建Release的权限

## 🚀 使用方法

### 方法1: 使用自动发布脚本（推荐）

#### 基本用法
```bash
# 创建新版本发布
./scripts/create_release.sh v1.3.0

# 使用自定义发布说明文件
./scripts/create_release.sh v1.3.0 RELEASE_NOTES_v1.3.0.md
```

#### 脚本功能
- ✅ 验证版本号格式
- ✅ 检查Git状态
- ✅ 自动生成发布说明（从模板）
- ✅ 创建Git标签
- ✅ 推送代码和标签
- ✅ 触发GitHub Actions

### 方法2: 手动创建标签

```bash
# 1. 创建发布说明文件
cp RELEASE_NOTES_TEMPLATE.md RELEASE_NOTES_v1.3.0.md
# 编辑发布说明文件

# 2. 提交发布说明
git add RELEASE_NOTES_v1.3.0.md
git commit -m "📝 添加 v1.3.0 版本发布说明"

# 3. 创建标签
git tag -a v1.3.0 -m "Release v1.3.0"

# 4. 推送
git push origin main
git push origin v1.3.0
```

## 📝 发布说明文件

### 命名规则
- 格式: `RELEASE_NOTES_v<版本号>.md`
- 示例: `RELEASE_NOTES_v1.3.0.md`

### 模板变量
发布说明模板支持以下变量：
- `{{VERSION}}`: 版本号（如 v1.3.0）
- `{{DATE}}`: 当前日期

### 自动生成
如果没有找到对应的发布说明文件，脚本会自动从模板生成：
```bash
# 自动生成 v1.3.0 的发布说明
./scripts/create_release.sh v1.3.0
```

## 🔄 工作流程

### 1. 触发条件
- 推送以`v`开头的标签（如 `v1.3.0`）
- 标签格式: `v<主版本>.<次版本>.<修订版本>`

### 2. 执行步骤
```yaml
1. 检出代码
2. 设置Python环境
3. 安装依赖
4. 构建应用 (PyInstaller)
5. 创建zip文件
6. 读取发布说明
7. 创建GitHub Release
8. 上传构建文件
9. 清理临时文件
```

### 3. 输出结果
- GitHub Release页面
- 可下载的zip文件
- 完整的发布说明

## 📱 查看状态

### GitHub Actions
```
https://github.com/<用户名>/<仓库名>/actions
```

### Releases页面
```
https://github.com/<用户名>/<仓库名>/releases
```

## 🐛 故障排除

### 常见问题

#### 1. Actions未触发
- 检查标签格式是否正确
- 确保推送了标签（不只是代码）
- 检查`.github/workflows/auto-release.yml`文件

#### 2. 构建失败
- 检查`requirements.txt`中的依赖
- 确保`PDF书签生成器.spec`文件正确
- 查看Actions日志获取详细错误信息

#### 3. Release创建失败
- 检查`GITHUB_TOKEN`权限
- 确保标签名称唯一
- 检查网络连接

### 调试步骤
```bash
# 1. 检查工作流文件语法
# 在GitHub上查看Actions页面

# 2. 本地测试构建
pyinstaller PDF书签生成器.spec

# 3. 检查发布说明文件
cat RELEASE_NOTES_v1.3.0.md

# 4. 验证标签
git tag -l | grep v1.3.0
```

## 📚 最佳实践

### 1. 版本管理
- 使用语义化版本号
- 每次发布都创建新标签
- 保持发布说明的完整性

### 2. 发布流程
- 在main分支上发布
- 先测试构建再发布
- 检查发布说明的准确性

### 3. 文档维护
- 及时更新发布说明模板
- 记录重要的功能变更
- 保持文档的一致性

## 🎯 示例

### 发布v1.3.0版本
```bash
# 1. 运行发布脚本
./scripts/create_release.sh v1.3.0

# 2. 确认发布
确认发布版本 v1.3.0? (y/N): y

# 3. 等待Actions完成
# 4. 在GitHub上查看Release
```

### 发布说明示例
```markdown
# PDF书签生成器 v1.3.0 发布说明

## 🎉 新版本发布
**版本**: v1.3.0  
**发布日期**: 2024年8月22日

## ✨ 主要新功能
- 新增自动发布功能
- 优化构建流程
- 改进用户体验

...
```

## 🔗 相关链接

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [PyInstaller文档](https://pyinstaller.org/)
- [语义化版本](https://semver.org/lang/zh-CN/)

---

**享受自动发布的便利！** 🎉
