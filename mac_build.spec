# -*- mode: python ; coding: utf-8 -*-

import os
import shutil
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# 完整收集所有子模組
hiddenimports = (
    collect_submodules('ai_video') +
    collect_submodules('insightface') +
    collect_submodules('onnxruntime') +
    collect_submodules('cv2') +
    ['scipy', 'yaml', 'PySide6']
)

# 收集必要的資料檔
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
    ['src/ai_video/gui/app.py'],
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