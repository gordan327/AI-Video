# -*- mode: python ; coding: utf-8 -*-

import os
import shutil
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# 顯式宣告所有內部模組與依賴套件，徹底杜絕 PyInstaller 漏掉子模組
hiddenimports = [
    'ai_video',
    'ai_video.detector',
    'ai_video.detector.scrfd',
    'ai_video.renderer',
    'ai_video.renderer.blur',
    'ai_video.renderer.pixelate',
    'ai_video.renderer.solid',
    'ai_video.image',
    'ai_video.image.image_processor',
    'ai_video.gui',
    'ai_video.gui.app',
    'ai_video.gui.controller',
    'ai_video.gui.main_window',
    'insightface',
    'onnxruntime',
    'cv2',
    'scipy',
    'yaml',
    'PySide6',
]

# 收集必要的設定檔與授權檔案
datas = (
    collect_data_files('insightface') +
    collect_data_files('onnxruntime') +
    [('src/ai_video/config', 'ai_video/config'), ('LICENSE', '.')]
)

ffmpeg_path = shutil.which("ffmpeg")
extra_binaries = []
if ffmpeg_path:
    extra_binaries.append((ffmpeg_path, '.'))

a = Analysis(
    ['run.py'],
    pathex=['src'],
    binaries=extra_binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='AI-Video',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AI-Video',
)

app = BUNDLE(
    coll,
    name='AI-Video.app',
    icon='resources/icon.ico' if os.path.exists('resources/icon.ico') else None,
    bundle_identifier='com.xieguoqing.aivideo',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'LSEnvironment': {'PATH': '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'},
    },
)