# qpdf 安装指南

## 什么是qpdf？

qpdf是一个开源的PDF处理工具，专门用于PDF文件的转换、修改和优化。PDF书签生成器使用它来清除PDF中的原始书签，为添加新书签做准备。

## 各平台安装方法

### Windows

#### 方法1：官方安装包（推荐）
1. 访问 [qpdf官网](https://qpdf.sourceforge.io/)
2. 下载适合您系统的版本：
   - 64位系统：`qpdf-11.6.3-windows-x64-installer.exe`
   - 32位系统：`qpdf-11.6.3-windows-x86-installer.exe`
3. 运行安装程序，按提示完成安装
4. 安装完成后，qpdf会自动添加到系统PATH中

#### 方法2：Chocolatey包管理器
```cmd
choco install qpdf
```

#### 方法3：Scoop包管理器
```cmd
scoop install qpdf
```

#### 方法4：MSYS2/MinGW
```bash
pacman -S mingw-w64-x86_64-qpdf
```

### macOS

#### 方法1：Homebrew（推荐）
```bash
brew install qpdf
```

#### 方法2：MacPorts
```bash
sudo port install qpdf
```

#### 方法3：官方安装包
1. 访问 [qpdf官网](https://qpdf.sourceforge.io/)
2. 下载macOS版本
3. 解压并安装

### Linux

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install qpdf
```

#### CentOS/RHEL/Fedora
```bash
# CentOS/RHEL 7
sudo yum install epel-release
sudo yum install qpdf

# CentOS/RHEL 8+
sudo dnf install epel-release
sudo dnf install qpdf

# Fedora
sudo dnf install qpdf
```

#### Arch Linux
```bash
sudo pacman -S qpdf
```

#### openSUSE
```bash
sudo zypper install qpdf
```

## 验证安装

安装完成后，在终端中运行以下命令验证：

```bash
qpdf --version
```

如果显示版本号，说明安装成功。例如：
```
qpdf version 11.6.3
```

## 功能测试

安装完成后，可以测试qpdf的基本功能：

### 1. 查看PDF信息
```bash
qpdf --show-pages input.pdf
```

### 2. 清除书签（测试命令）
```bash
qpdf --empty --pages input.pdf 1-z -- output.pdf
```

### 3. 查看帮助信息
```bash
qpdf --help
```

## 常见问题解决

### 问题1：命令未找到
**症状**: 运行`qpdf --version`时提示"命令未找到"

**解决方案**:
1. 重新启动终端/命令提示符
2. 检查系统PATH环境变量
3. 手动添加qpdf安装目录到PATH

### 问题2：权限不足
**症状**: 运行时提示权限不足

**解决方案**:
1. 使用管理员权限运行
2. 检查文件权限设置
3. 重新安装qpdf

### 问题3：版本不兼容
**症状**: 运行时出现版本相关错误

**解决方案**:
1. 卸载旧版本
2. 下载并安装最新版本
3. 确保版本与系统架构匹配

### 问题4：依赖库缺失
**症状**: 运行时提示缺少某些库文件

**解决方案**:
1. 安装缺失的依赖库
2. 使用包管理器安装完整版本
3. 检查系统库文件

## 手动配置PATH（Windows）

如果qpdf没有自动添加到PATH，可以手动配置：

1. 右键"此电脑" → "属性" → "高级系统设置"
2. 点击"环境变量"
3. 在"系统变量"中找到"Path"
4. 点击"编辑"，添加qpdf安装目录（通常是`C:\Program Files\qpdf\bin`）
5. 点击"确定"保存

## 高级配置

### 1. 配置文件
qpdf支持配置文件来自定义行为：
```bash
# 创建配置文件
mkdir ~/.qpdf
touch ~/.qpdf/qpdf.config

# 编辑配置文件
echo "deterministic-id" >> ~/.qpdf/qpdf.config
```

### 2. 环境变量
可以设置环境变量来配置qpdf：
```bash
# 设置临时目录
export QPDF_TMPDIR=/tmp/qpdf

# 设置日志级别
export QPDF_LOG_LEVEL=info
```

### 3. 性能优化
对于大文件处理，可以调整参数：
```bash
# 使用更多内存
qpdf --linearize --optimize-images --input input.pdf --output output.pdf

# 并行处理
qpdf --linearize --optimize-images --input input.pdf --output output.pdf --job-json jobs.json
```

## 在PDF书签生成器中使用

### 1. 功能集成
qpdf安装完成后，PDF书签生成器会自动检测并使用：

- **自动检测**: 应用启动时自动检查qpdf是否可用
- **状态显示**: 在状态栏显示qpdf版本信息
- **错误处理**: 如果qpdf不可用，会显示详细的安装指导

### 2. 使用流程
1. 选择包含原始书签的PDF文件
2. 点击"🧹 清除原始书签"按钮
3. 系统自动调用qpdf清除书签
4. 生成无书签的PDF文件
5. 可选择更新输入路径为清理后的文件

### 3. 调试信息
启用调试模式后，可以看到详细的qpdf执行信息：
```
清除书签信息:
  输入PDF: /path/to/input.pdf
  输出PDF: /path/to/input_no_bookmarks.pdf
  使用qpdf: 11.6.3

执行命令: qpdf --empty --pages /path/to/input.pdf 1-z -- /path/to/output.pdf
工作目录: /current/working/directory
```

## 系统要求

### 最低要求
- **Windows**: Windows 7及以上版本
- **macOS**: macOS 10.12及以上版本
- **Linux**: 大多数现代发行版都支持
- **内存**: 建议至少256MB可用内存
- **磁盘空间**: 安装需要约50MB空间

### 推荐配置
- **内存**: 1GB或更多可用内存
- **磁盘空间**: 100MB或更多可用空间
- **处理器**: 支持SSE2的现代处理器
- **操作系统**: 最新版本的稳定发行版

## 技术支持

### 官方资源
- **官网**: [https://qpdf.sourceforge.io/](https://qpdf.sourceforge.io/)
- **文档**: [https://qpdf.sourceforge.io/qpdf-manual.html](https://qpdf.sourceforge.io/qpdf-manual.html)
- **源码**: [https://github.com/qpdf/qpdf](https://github.com/qpdf/qpdf)

### 社区支持
- **GitHub Issues**: [https://github.com/qpdf/qpdf/issues](https://github.com/qpdf/qpdf/issues)
- **邮件列表**: [qpdf-users@lists.sourceforge.net](mailto:qpdf-users@lists.sourceforge.net)

### 故障排除
如果安装过程中遇到问题：

1. 检查系统要求
2. 查看错误日志
3. 尝试重新安装
4. 联系技术支持或社区

## 总结

qpdf是一个功能强大、稳定可靠的PDF处理工具，为PDF书签生成器提供了清除原始书签的核心能力。通过正确的安装和配置，用户可以：

1. **清除原始书签**: 为添加新书签做准备
2. **优化PDF文件**: 使用qpdf的其他功能优化PDF
3. **批量处理**: 处理大量PDF文件
4. **专业工具**: 使用企业级的PDF处理能力

安装qpdf后，PDF书签生成器将成为一个功能完整的PDF书签处理解决方案。
