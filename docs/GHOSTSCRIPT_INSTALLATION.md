# Ghostscript 安装指南

## 什么是Ghostscript？

Ghostscript是一个开源的PostScript和PDF解释器，PDF书签生成器使用它来生成带有书签的PDF文件。

## 各平台安装方法

### Windows

#### 方法1：官方安装包（推荐）
1. 访问 [Ghostscript官网](https://www.ghostscript.com/releases/gsdnld.html)
2. 下载适合您系统的版本：
   - 64位系统：`gs1000w64.exe`
   - 32位系统：`gs1000w32.exe`
3. 运行安装程序，按提示完成安装
4. 安装完成后，Ghostscript会自动添加到系统PATH中

#### 方法2：Chocolatey包管理器
```cmd
choco install ghostscript
```

#### 方法3：Scoop包管理器
```cmd
scoop install ghostscript
```

### macOS

#### 方法1：Homebrew（推荐）
```bash
brew install ghostscript
```

#### 方法2：MacPorts
```bash
sudo port install ghostscript
```

#### 方法3：官方安装包
1. 访问 [Ghostscript官网](https://www.ghostscript.com/releases/gsdnld.html)
2. 下载macOS版本
3. 解压并安装

### Linux

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install ghostscript
```

#### CentOS/RHEL/Fedora
```bash
# CentOS/RHEL
sudo yum install ghostscript

# Fedora
sudo dnf install ghostscript
```

#### Arch Linux
```bash
sudo pacman -S ghostscript
```

## 验证安装

安装完成后，在终端中运行以下命令验证：

```bash
gs --version
```

如果显示版本号，说明安装成功。

## 常见问题解决

### 问题1：命令未找到
**症状**: 运行`gs --version`时提示"命令未找到"

**解决方案**:
1. 重新启动终端/命令提示符
2. 检查系统PATH环境变量
3. 手动添加Ghostscript安装目录到PATH

### 问题2：权限不足
**症状**: 运行时提示权限不足

**解决方案**:
1. 使用管理员权限运行
2. 检查文件权限设置
3. 重新安装Ghostscript

### 问题3：版本不兼容
**症状**: 运行时出现版本相关错误

**解决方案**:
1. 卸载旧版本
2. 下载并安装最新版本
3. 确保版本与系统架构匹配

## 手动配置PATH（Windows）

如果Ghostscript没有自动添加到PATH，可以手动配置：

1. 右键"此电脑" → "属性" → "高级系统设置"
2. 点击"环境变量"
3. 在"系统变量"中找到"Path"
4. 点击"编辑"，添加Ghostscript安装目录（通常是`C:\Program Files\gs\gs10.00.0\bin`）
5. 点击"确定"保存

## 打包应用中的Ghostscript

### 方法1：包含Ghostscript可执行文件
1. 将Ghostscript可执行文件复制到应用目录
2. 修改应用代码，优先使用相对路径
3. 重新打包应用

### 方法2：使用系统安装的Ghostscript
1. 确保目标系统已安装Ghostscript
2. 应用会自动检测系统PATH中的Ghostscript
3. 提供安装说明给用户

## 测试Ghostscript功能

在PDF书签生成器中，可以使用"🧪 测试Ghostscript"按钮来验证安装：

1. 点击"🧪 测试Ghostscript"按钮
2. 查看测试结果
3. 如果测试通过，说明Ghostscript配置正确

## 技术支持

如果安装过程中遇到问题：

1. 检查系统要求
2. 查看错误日志
3. 尝试重新安装
4. 联系技术支持

## 系统要求

- **Windows**: Windows 7及以上版本
- **macOS**: macOS 10.12及以上版本
- **Linux**: 大多数现代发行版都支持
- **内存**: 建议至少512MB可用内存
- **磁盘空间**: 安装需要约50MB空间
