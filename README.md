<div align="center">

# 📚 PDF Bookmarker

**A powerful cross-platform PDF bookmark generator using Ghostscript**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/vanabel/pdf-bookmarker)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/vanabel/pdf-bookmarker)

*Generate professional PDF bookmarks with advanced features like dynamic offsets, negative page support, and intelligent error detection*

[🚀 Features](#-features) • [📦 Installation](#-installation) • [🔧 Usage](#-usage) • [📖 Examples](#-examples) • [🛠️ Development](#️-development)

</div>

---

## ✨ Features

### 🎯 Core Functionality
- **Cross-platform support** - Windows, macOS, and Linux
- **Smart TOC parsing** - Multiple format support with automatic detection
- **Dynamic page offsets** - HTML comment-style offset commands
- **Negative page support** - Full support for negative page numbers
- **Ghostscript integration** - Professional PDF processing backend

### 🔍 Advanced Features
- **Bookmark preview** - Preview and validate bookmarks before generation
- **Intelligent error detection** - Automatic problem identification and suggestions
- **Multiple format support** - Standard, dot-line, and custom formats
- **Real-time validation** - Check for issues before PDF generation
- **Debug mode** - Detailed logging and error diagnostics
- **Clear original bookmarks** - Remove existing bookmarks from PDFs using qpdf
- **Comprehensive tool testing** - Test both Ghostscript and qpdf functionality
- **Enhanced UI** - Modern interface with placeholder effects and keyboard shortcuts

### 🎨 Modern UI
- **Beautiful interface** - Modern design with intuitive layout
- **Responsive design** - Adapts to different screen sizes
- **Visual feedback** - Color-coded status indicators and progress updates
- **Accessibility** - Clear labels and helpful tooltips

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+** (with tkinter)
- **Ghostscript** (for PDF processing)

### Installation

```bash
# Clone the repository
git clone https://github.com/vanabel/pdf-bookmarker.git
cd pdf-bookmarker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
# Start the GUI application
python pdf_bookmarker_gs.py

# Or use the provided scripts
./run_app.sh          # macOS/Linux
run_app.bat           # Windows
```

---

## 📖 Usage

### 1. Basic Workflow
1. **Select PDF** - Choose the input PDF file
2. **Set Offset** - Configure page offset (bookmark page 1 → PDF page X)
3. **Input TOC** - Enter your table of contents
4. **Preview** - Review bookmarks and check for issues
5. **Generate** - Create the final PDF with bookmarks

### 2. TOC Format Support

#### Standard Format
```
PREFACE V
Chapter I. INTRODUCTION 1
1. Outline of this book 1
2. Further remarks 4
```

#### Dot-line Format (Auto-detected)
```
Preface ............................................. 7
Chapter I. INTRODUCTION ............................ 1
1. Outline of this book .......................... 1
```

#### Dynamic Offset Commands
```
<!---offset -13--->
PREFACE 5
PREFACE TO REVISED EDITION 7
<!---offset +13 --->
Chapter I. INTRODUCTION
1. Outline of this book 1
```

### 3. Advanced Features

#### Bookmark Preview
- Click "👁️ Preview Bookmarks" to review before generation
- Automatic error detection and warnings
- Visual validation of page numbers and offsets

#### Ghostscript Testing
- Click "🧪 Test Ghostscript" to verify installation
- Comprehensive diagnostics and troubleshooting
- Version and capability verification

#### Debug Mode
- Enable detailed console output
- Step-by-step process logging
- Error trace and diagnostic information

#### Clear Original Bookmarks
- Remove existing bookmarks from PDFs
- Useful for cleaning up before adding new bookmarks
- Preserves PDF content while removing bookmark metadata

#### Tool Testing
- Comprehensive testing of Ghostscript and qpdf
- Detailed diagnostics and installation guidance
- One-click verification of all dependencies

---

## 📦 Application Packaging

### Build Executable
```bash
# macOS
chmod +x build_macos.sh
./build_macos.sh

# Windows
build_windows.bat

# Universal
python build_app.py
```

### Distribution
After building, you'll get:
- **Executable file** - `dist/PDF书签生成器`
- **Launch scripts** - Platform-specific startup scripts
- **User manual** - Complete usage instructions

**Users can run the application without installing Python!**

---

## 🔧 Configuration

### Dependencies Installation

This application requires two external tools for full functionality:

- **Ghostscript** - For PDF bookmark generation
- **qpdf** - For clearing original PDF bookmarks

📖 **Detailed installation guides are available in the [docs/](docs/) directory:**
- [Ghostscript Installation Guide](docs/GHOSTSCRIPT_INSTALLATION.md)
- [qpdf Installation Guide](docs/QPDF_INSTALLATION.md)

#### Quick Installation Commands

**macOS:**
```bash
brew install ghostscript qpdf
```

**Windows:**
1. Download from [Ghostscript](https://www.ghostscript.com/releases/gsdnld.html) and [qpdf](https://github.com/qpdf/qpdf/releases)
2. Install and add to system PATH

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ghostscript qpdf
```

### Environment Variables
```bash
# Optional: Custom tool paths
export GS_PATH="/usr/local/bin/gs"
export QPDF_PATH="/usr/local/bin/qpdf"
```

---

## 📁 Project Structure

```
pdf-bookmarker/
├── 📱 pdf_bookmarker_gs.py      # Main application
├── 🔍 bookmark_validator.py     # Standalone validation tool
├── 🐛 debug_ghostscript.py     # Ghostscript diagnostics
├── 🎯 demo.py                   # Feature demonstration
├── 📦 build_app.py              # Application packaging
├── 🚀 build_macos.sh            # macOS build script
├── 🪟 build_windows.bat         # Windows build script
├── 📚 demo/                      # Example files and samples
│   ├── 📖 full_bookmarks.txt    # Complete academic book TOC
│   ├── 🔢 simple_bookmarks.txt  # Basic chapter structure
│   ├── 📊 dots_format_bookmarks.txt # Dot-line format
│   ├── ⚙️ dynamic_offset_bookmarks.txt # Dynamic offset examples
│   └── 📄 *.pdf                 # Sample PDF files
├── 📋 requirements.txt           # Python dependencies
├── 📖 README.md                 # This file
├── 🚫 .gitignore                # Git ignore rules
└── 📄 LICENSE                   # MIT License
```

---

## 🧪 Examples

### Demo Files
The `demo/` directory contains comprehensive examples:

```bash
cd demo
python load_examples.py                    # List all examples
python load_examples.py simple_bookmarks.txt    # View basic example
python load_examples.py full_bookmarks.txt --copy  # Copy to clipboard
```

### Sample TOC with Dynamic Offsets
```text
<!---offset -13--->
PREFACE 5
PREFACE TO REVISED EDITION 7
<!---offset +13 --->
Chapter I. INTRODUCTION
1. Outline of this book 1
2. Further remarks 4
3. Notation 5
```

---

## 🛠️ Development

### Setup Development Environment
```bash
# Clone and setup
git clone https://github.com/vanabel/pdf-bookmarker.git
cd pdf-bookmarker
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8  # Optional: testing and linting
```

### Code Style
- **Python**: PEP 8 compliant
- **GUI**: Tkinter with ttk widgets
- **Architecture**: Object-oriented with clear separation of concerns

### Testing
```bash
# Run tests
python -m pytest

# Run specific test
python test_app.py
```

---

## 🐛 Troubleshooting

### Common Issues

#### Ghostscript Not Found
```bash
# Check installation
gs --version

# Verify PATH
which gs  # macOS/Linux
where gs  # Windows
```

#### Application Won't Start
- Ensure Python 3.7+ is installed
- Check tkinter availability: `python -c "import tkinter"`
- Verify virtual environment activation

#### PDF Generation Fails
- Check Ghostscript installation
- Verify input PDF is not corrupted
- Review error logs in the application

### Debug Mode
Enable debug mode to get detailed information:
1. Check "🐛 Debug Mode" in the application
2. View console output for detailed logs
3. Use "🧪 Test Ghostscript" for diagnostics

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
- 🐛 **Report bugs** - Use GitHub Issues
- 💡 **Suggest features** - Open feature requests
- 📝 **Improve documentation** - Submit PRs for docs
- 🔧 **Fix issues** - Submit pull requests
- 🌍 **Add translations** - Help with internationalization

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings for new functions
- Include type hints where appropriate
- Write clear commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**MIT License Benefits:**
- ✅ Free for commercial use
- ✅ Modify and distribute
- ✅ Use in proprietary software
- ✅ Minimal restrictions

---

## 🙏 Acknowledgments

- **Ghostscript Team** - For the powerful PDF processing engine
- **Python Community** - For the excellent tkinter GUI framework
- **Open Source Contributors** - For inspiration and feedback

---

## 📚 Documentation

### 📖 Complete Documentation
For detailed guides, troubleshooting, and advanced usage, visit our comprehensive documentation:

- **[📚 Documentation Center](docs/)** - Complete documentation index
- **[🚀 New Features Guide](docs/NEW_FEATURE_SUMMARY.md)** - Latest features and improvements
- **[🔧 Installation Guides](docs/)** - Step-by-step setup instructions
- **[📋 Feature Documentation](docs/)** - Detailed usage and configuration

### 🎯 Quick Reference
- **Debug Mode**: [Debug Mode Explanation](docs/DEBUG_MODE_EXPLANATION.md)
- **Clear Bookmarks**: [Clear Bookmarks Feature](docs/CLEAR_BOOKMARKS_FEATURE.md)
- **Tool Testing**: Use "🧪 Test Tools" button in the application

---

## 📞 Support & Community

### Getting Help
- 📖 **Documentation** - This README and [detailed docs](docs/)
- 🐛 **Issues** - [GitHub Issues](https://github.com/vanabel/pdf-bookmarker/issues)
- 💬 **Discussions** - [GitHub Discussions](https://github.com/vanabel/pdf-bookmarker/discussions)
- 📧 **Email** - Open an issue for direct contact

### Stay Updated
- ⭐ **Star the repo** - Show your support
- 👀 **Watch** - Get notified of updates
- 🔔 **Notifications** - Stay informed about releases

---

<div align="center">

**Made with ❤️ by the PDF Bookmarker Team**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vanabel/pdf-bookmarker)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-FF6F61?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/tkinter.html)

</div> 