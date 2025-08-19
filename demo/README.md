# Demo 目录

这个目录包含了PDF书签生成器的演示文件和示例。

## 📁 文件说明

### 📚 书签示例文件

#### 1. `full_bookmarks.txt` - 完整书签示例
- **特点**：包含15个章节的完整学术书籍目录
- **功能演示**：
  - 负页码支持（Preface -7, Preface to Revised Edition -5）
  - 多级标题结构（章节、小节、注释、练习）
  - 动态偏移指令（`<!---offset -1--->`）
  - 复杂的页码分布（-7 到 445）

#### 2. `simple_bookmarks.txt` - 简单书签示例
- **特点**：基础的章节结构，适合初学者
- **功能演示**：
  - 基本标题和页码格式
  - 多级标题缩进
  - 无特殊格式的纯文本目录

#### 3. `dots_format_bookmarks.txt` - 点线格式示例
- **特点**：使用点线分隔标题和页码的格式
- **功能演示**：
  - 自动识别点线格式
  - 处理不同长度的点线
  - 保持标题和页码的正确对应

#### 4. `dynamic_offset_bookmarks.txt` - 动态偏移示例
- **特点**：演示HTML注释风格的偏移指令
- **功能演示**：
  - `<!---offset -13--->` 设置负偏移
  - `<!---offset +13 --->` 恢复正偏移
  - 动态调整页码偏移值

### 📄 PDF文件

#### 1. `Lieberman_1996_Second order parabolic differential equations.pdf`
- **原始PDF**：Lieberman的《二阶抛物型偏微分方程》教材
- **用途**：测试书签生成功能
- **特点**：学术教材，适合测试复杂的书签结构

#### 2. `Lieberman_1996_Second order parabolic differential equations_with_bookmarks.pdf`
- **带书签的PDF**：使用完整书签生成的最终结果
- **用途**：展示书签生成的效果
- **特点**：包含完整的15章节书签结构

## 🚀 使用方法

### 1. 测试基本功能
```bash
# 使用简单示例
python pdf_bookmarker_gs.py
# 加载 demo/simple_bookmarks.txt
# 设置页面偏移为12
# 点击"预览书签"检查结果
```

### 2. 测试高级功能
```bash
# 使用完整示例
python pdf_bookmarker_gs.py
# 加载 demo/full_bookmarks.txt
# 设置页面偏移为1
# 点击"预览书签"查看复杂的书签结构
```

### 3. 测试动态偏移
```bash
# 使用动态偏移示例
python pdf_bookmarker_gs.py
# 加载 demo/dynamic_offset_bookmarks.txt
# 设置页面偏移为10
# 观察偏移指令如何影响页码计算
```

### 4. 测试点线格式
```bash
# 使用点线格式示例
python pdf_bookmarker_gs.py
# 加载 demo/dots_format_bookmarks.txt
# 验证点线格式的自动识别
```

## 🔍 功能验证

### 负页码处理
- **输入**：`Preface -7`
- **偏移**：12
- **预期结果**：PDF第5页（-7 + 12 - 1 = 4，但Ghostscript从0开始计数）

### 动态偏移指令
- **指令**：`<!---offset -13--->`
- **效果**：后续所有页码减去13
- **恢复**：`<!---offset +13 --->` 将偏移恢复到0

### 多级标题
- **章节**：`Chapter I. INTRODUCTION 1`
- **小节**：`  1. Outline of this book 1`
- **支持**：自动识别缩进和层级结构

## 📝 注意事项

1. **页码格式**：支持正数、负数和零
2. **偏移指令**：使用HTML注释风格 `<!---offset +/-数字--->`
3. **特殊字符**：自动转义 `(`, `)`, `\` 等PostScript特殊字符
4. **文件编码**：使用UTF-8编码，支持中文和特殊符号
5. **Ghostscript**：确保系统已正确安装Ghostscript

## 🎯 测试建议

1. **从简单开始**：先测试 `simple_bookmarks.txt`
2. **逐步复杂**：再测试 `dots_format_bookmarks.txt`
3. **高级功能**：最后测试 `dynamic_offset_bookmarks.txt`
4. **完整测试**：使用 `full_bookmarks.txt` 验证所有功能

这些示例文件展示了PDF书签生成器的所有核心功能，是学习和测试的最佳资源！ 