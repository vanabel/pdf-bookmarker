# 🏠 本地构建指南

## 📋 概述

本指南将帮助您在本地构建PDF书签生成器，避免GitHub Actions的macOS安全限制问题。

## 🎯 为什么需要本地构建？

### **GitHub Actions的限制**：
- ❌ 无法交互输入管理员密码
- ❌ 无法访问macOS系统偏好设置
- ❌ 无法绕过Gatekeeper安全机制
- ❌ 构建的应用可能无法直接运行

### **本地构建的优势**：
- ✅ 完全控制构建环境
- ✅ 自动处理macOS兼容性
- ✅ 解决Gatekeeper问题
- ✅ 生成可直接运行的应用

## 🚀 快速开始

### **1. 克隆仓库**
```bash
git clone https://github.com/vanabel/pdf-bookmarker.git
cd pdf-bookmarker
```

### **2. 运行构建脚本**
```bash
# 给脚本执行权限
chmod +x build_macos_optimized.sh

# 运行构建脚本
./build_macos_optimized.sh
```

### **3. 等待构建完成**
脚本将自动：
- 检查系统环境
- 安装依赖
- 构建应用
- 处理兼容性问题
- 创建发布包

## 🔧 详细步骤

### **步骤1：环境准备**

#### **检查系统要求**：
- macOS 10.15 (Catalina) 或更高版本
- Python 3.8+
- 至少2GB可用磁盘空间

#### **检查Python环境**：
```bash
python3 --version
which python3
```

#### **激活虚拟环境（推荐）**：
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

### **步骤2：依赖安装**

#### **自动安装（推荐）**：
构建脚本会自动安装所有依赖：
- pip升级
- requirements.txt中的包
- PyInstaller

#### **手动安装（如果需要）**：
```bash
# 升级pip
python3 -m pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 安装PyInstaller
pip install pyinstaller
```

### **步骤3：构建应用**

#### **使用优化脚本（推荐）**：
```bash
./build_macos_optimized.sh
```

#### **手动构建**：
```bash
# 清理之前的构建
rm -rf build dist __pycache__

# 使用PyInstaller构建
pyinstaller "PDF书签生成器.spec"
```

### **步骤4：兼容性处理**

构建脚本会自动处理：
- 移除扩展属性
- 添加Gatekeeper例外
- 验证应用架构

## 🐛 常见问题解决

### **问题1：SOCKS代理错误**
```
ERROR: Could not install packages due to an OSError: Missing dependencies for SOCKS support.
```

**解决方案**：
```bash
# 临时禁用代理
unset all_proxy http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY

# 然后重新运行构建脚本
./build_macos_optimized.sh
```

### **问题2：权限不足**
```
Permission denied: './build_macos_optimized.sh'
```

**解决方案**：
```bash
chmod +x build_macos_optimized.sh
```

### **问题3：Python路径问题**
```
python3: command not found
```

**解决方案**：
```bash
# 使用完整路径
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3

# 或添加到PATH
export PATH="/Library/Frameworks/Python.framework/Versions/3.11/bin:$PATH"
```

### **问题4：依赖安装失败**
```
ERROR: Could not find a version that satisfies the requirement
```

**解决方案**：
```bash
# 升级pip
python3 -m pip install --upgrade pip

# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
```

## 📱 构建结果

### **成功构建后，您将得到**：

1. **应用包**：`dist/PDF书签生成器.app`
2. **发布包**：`dist/PDF书签生成器_YYYYMMDD_HHMMSS_macOS_x86_64.zip`
3. **应用大小**：约50-100MB

### **验证构建结果**：
```bash
# 检查应用架构
file "dist/PDF书签生成器.app/Contents/MacOS/PDF书签生成器"

# 检查应用包结构
ls -la "dist/PDF书签生成器.app/Contents/"

# 检查应用大小
du -sh "dist/PDF书签生成器.app"
```

## 🚀 运行应用

### **方法1：直接运行**
```bash
open "dist/PDF书签生成器.app"
```

### **方法2：命令行运行**
```bash
"dist/PDF书签生成器.app/Contents/MacOS/PDF书签生成器"
```

### **如果遇到"无法打开"错误**：

1. **右键选择"打开"**
2. **系统偏好设置 > 安全性与隐私 > 通用**
3. **点击"仍要打开"**

## 📦 发布应用

### **创建发布包**：
```bash
cd dist
zip -r "PDF书签生成器_v1.3.4_macOS_x86_64.zip" "PDF书签生成器.app"
cd ..
```

### **验证发布包**：
```bash
# 检查zip文件
ls -la dist/*.zip

# 验证zip内容
unzip -l "dist/PDF书签生成器_v1.3.4_macOS_x86_64.zip"
```

## 🔍 故障排除

### **构建失败**：
1. 检查Python版本和路径
2. 确认虚拟环境已激活
3. 检查磁盘空间
4. 查看构建日志

### **应用无法运行**：
1. 检查应用架构（应为x86_64）
2. 确认Gatekeeper设置
3. 检查系统版本兼容性

### **性能问题**：
1. 关闭不必要的应用
2. 确保有足够内存
3. 使用SSD存储

## 📚 相关文档

- [安装指南](INSTALLATION_GUIDE.md) - 系统依赖安装
- [构建指南](BUILD_GUIDE.md) - 通用构建说明
- [新功能总结](NEW_FEATURE_SUMMARY.md) - 功能特性说明

## 🆘 获取帮助

如果遇到问题：
1. 查看构建日志输出
2. 检查系统要求
3. 参考故障排除部分
4. 提交GitHub Issue

---

**💡 提示**：本地构建是获得最佳兼容性的推荐方法！
