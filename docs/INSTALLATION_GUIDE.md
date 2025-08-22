# 🔧 安装指南 - Ghostscript & qpdf

本指南将帮助您在各个平台上安装PDF书签生成器所需的依赖工具。

## 📋 依赖工具概览

PDF书签生成器需要两个外部工具来提供完整功能：

- **🔧 Ghostscript** - 用于PDF书签生成和PDF处理
- **🔧 qpdf** - 用于清除PDF原始书签和PDF操作

## 🚀 快速安装命令

### macOS (推荐使用Homebrew)
```bash
# 安装Homebrew (如果尚未安装)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装依赖工具
brew install ghostscript qpdf

# 验证安装
gs --version
qpdf --version
```

### Linux (Ubuntu/Debian)
```bash
# 更新包管理器
sudo apt-get update

# 安装依赖工具
sudo apt-get install ghostscript qpdf

# 验证安装
gs --version
qpdf --version
```

### Linux (CentOS/RHEL/Fedora)
```bash
# CentOS/RHEL
sudo yum install ghostscript qpdf

# Fedora
sudo dnf install ghostscript qpdf

# 验证安装
gs --version
qpdf --version
```

### Windows
1. **Ghostscript安装**：
   - 访问 [Ghostscript官网](https://www.ghostscript.com/releases/gsdnld.html)
   - 下载适合您系统的安装包（推荐64位版本）
   - 运行安装程序，确保勾选"Add to PATH"选项

2. **qpdf安装**：
   - 访问 [qpdf GitHub Releases](https://github.com/qpdf/qpdf/releases)
   - 下载最新的Windows版本
   - 解压到 `C:\Program Files\qpdf\` 目录
   - 将 `C:\Program Files\qpdf\bin\` 添加到系统PATH环境变量

## 🔍 详细安装步骤

### Ghostscript 详细安装

#### macOS 详细步骤
```bash
# 使用Homebrew安装
brew install ghostscript

# 验证安装
gs --version

# 检查pdfwrite设备支持
gs -h | grep pdfwrite
```

#### Linux 详细步骤
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ghostscript

# 验证安装
gs --version

# 检查设备支持
gs -h
```

#### Windows 详细步骤
1. 下载安装包：
   - 访问 [Ghostscript下载页面](https://www.ghostscript.com/releases/gsdnld.html)
   - 选择适合您Windows版本的安装包
   - 推荐下载64位版本以获得最佳性能

2. 安装过程：
   - 双击下载的安装包
   - 选择安装目录（建议使用默认路径）
   - **重要**：确保勾选"Add Ghostscript to the system PATH"选项
   - 完成安装

3. 验证安装：
   - 打开新的命令提示符或PowerShell
   - 运行 `gs --version`
   - 如果显示版本信息，说明安装成功

### qpdf 详细安装

#### macOS 详细步骤
```bash
# 使用Homebrew安装
brew install qpdf

# 验证安装
qpdf --version

# 检查帮助信息
qpdf --help
```

#### Linux 详细步骤
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install qpdf

# 验证安装
qpdf --version

# 检查功能
qpdf --help
```

#### Windows 详细步骤
1. 下载qpdf：
   - 访问 [qpdf GitHub Releases](https://github.com/qpdf/qpdf/releases)
   - 下载最新的Windows版本（通常是zip文件）

2. 安装步骤：
   - 解压下载的zip文件
   - 将解压后的文件夹重命名为 `qpdf`
   - 将整个 `qpdf` 文件夹移动到 `C:\Program Files\`
   - 最终路径应该是：`C:\Program Files\qpdf\`

3. 添加到PATH：
   - 右键"此电脑" → "属性" → "高级系统设置"
   - 点击"环境变量"
   - 在"系统变量"中找到"Path"，点击"编辑"
   - 点击"新建"，添加 `C:\Program Files\qpdf\bin`
   - 点击"确定"保存所有更改

4. 验证安装：
   - 打开新的命令提示符
   - 运行 `qpdf --version`
   - 如果显示版本信息，说明安装成功

## ✅ 安装验证

安装完成后，请按以下步骤验证：

### 1. 基本验证
```bash
# 检查Ghostscript
gs --version

# 检查qpdf
qpdf --version
```

### 2. 功能验证
```bash
# 测试Ghostscript PDF处理能力
gs -h | grep pdfwrite

# 测试qpdf基本功能
qpdf --help
```

### 3. 在应用中验证
1. 启动PDF书签生成器
2. 点击"🧪 测试工具"按钮
3. 查看测试报告，确认两个工具都显示"✓ 可用"

## 🐛 常见问题解决

### Ghostscript 相关问题

#### 问题：命令未找到
**症状**：运行 `gs --version` 时提示"命令未找到"

**解决方案**：
- **Windows**：检查PATH环境变量是否正确设置
- **macOS/Linux**：重新安装或检查安装路径

#### 问题：pdfwrite设备不支持
**症状**：测试时显示"pdfwrite设备: ✗ 不支持"

**解决方案**：
- 重新安装Ghostscript
- 确保安装的是完整版本，不是精简版

### qpdf 相关问题

#### 问题：命令未找到
**症状**：运行 `qpdf --version` 时提示"命令未找到"

**解决方案**：
- **Windows**：检查PATH环境变量和安装路径
- **macOS/Linux**：重新安装或检查包管理器

#### 问题：权限不足
**症状**：运行时提示权限错误

**解决方案**：
- **Linux**：使用 `sudo` 运行安装命令
- **Windows**：以管理员身份运行安装程序

## 🔧 高级配置

### 自定义工具路径
如果您的工具安装在非标准位置，可以在环境变量中指定：

```bash
# macOS/Linux
export GS_PATH="/usr/local/bin/gs"
export QPDF_PATH="/usr/local/bin/qpdf"

# Windows (在系统环境变量中设置)
GS_PATH=C:\Program Files\gs\gs10.01.1\bin\gswin64c.exe
QPDF_PATH=C:\Program Files\qpdf\bin\qpdf.exe
```

### 版本兼容性
- **Ghostscript**: 推荐使用9.50或更高版本
- **qpdf**: 推荐使用10.0或更高版本

## 📞 获取帮助

如果在安装过程中遇到问题：

1. **查看应用内的测试报告**：使用"🧪 测试工具"功能
2. **检查系统PATH**：确保工具在系统PATH中
3. **查看错误日志**：启用调试模式获取详细信息
4. **提交Issue**：在GitHub上报告问题

## 🔗 相关链接

- [Ghostscript官网](https://www.ghostscript.com/)
- [qpdf GitHub](https://github.com/qpdf/qpdf)
- [PDF书签生成器文档](../README.md)
- [功能测试说明](DEBUG_MODE_EXPLANATION.md)

---

*最后更新：2024年8月22日*
