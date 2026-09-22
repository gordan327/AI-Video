# -*- mode: python ; coding: utf-8 -*-
import sys

# 根據不同作業系統自動調整 ffmpeg 路徑
if sys.platform == 'win32':
    ffmpeg_path = 'ffmpeg.exe' # 如果 Windows 有透過 pip 或其他方式安裝，或放在專案根目錄
else:
    ffmpeg_path = '/opt/homebrew/bin/ffmpeg'

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[(ffmpeg_path, '.')],
    datas=[('ai_video/config', 'ai_video/config')],
    hiddenimports=['numpy', 'insightface', 'onnxruntime', 'cv2', 'torch', 'torchvision'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

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
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AI-Video',
)

# Mac 專用的 BUNDLE，Windows 執行時會自動跳過或不作用
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='AI-Video.app',
        icon=None,
        bundle_identifier=None,
    )