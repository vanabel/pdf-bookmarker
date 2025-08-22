# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['pdf_bookmarker_gs.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/icons', 'assets/icons'),  # 包含所有图标文件
        ('demo', 'demo'),                  # 包含示例文件
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'pathlib',
        'subprocess',
        'tempfile',
        're',
        'threading',
        'time',
        'os',
        'sys',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF书签生成器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 无控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS特定的应用包配置
app = BUNDLE(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='PDF书签生成器.app',
    icon='assets/icons/icon.icns',  # 使用.icns格式图标（macOS专用）
    bundle_identifier='com.pdfbookmarker.app',
    version='1.0.0',
    info_plist={
        'CFBundleName': 'PDF书签生成器',
        'CFBundleDisplayName': 'PDF书签生成器',
        'CFBundleIdentifier': 'com.pdfbookmarker.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'CFBundleExecutable': 'PDF书签生成器',
        'CFBundleIconFile': 'icon_256.png',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'PDF Document',
                'CFBundleTypeExtensions': ['pdf'],
                'CFBundleTypeRole': 'Viewer',
                'CFBundleTypeIconFile': 'icon_256.png',
            }
        ],
        'NSHighResolutionCapable': True,  # 支持高分辨率显示
        'LSMinimumSystemVersion': '10.10.0',  # 最低系统要求
        'LSApplicationCategoryType': 'public.app-category.productivity',
        'NSPrincipalClass': 'NSApplication',
    },
)
