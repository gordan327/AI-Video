# -*- mode: python ; coding: utf-8 -*-

import os
import shutil
from PyInstaller.utils.hooks import collect_all, collect_data_files

block_cipher = None

# 使用 collect_all 一次性完整收錄 ai_video 與其他 AI 套件的所有子模組與二進位檔
ai_video_data = collect_all('ai_video')
insightface_data = collect_all('insightface')
onnxruntime_data = collect_all('onnxruntime')
cv2_data = collect_all('cv2')

datas = (
    ai_video_data[0] + 
    insightface_data[0] + 
    onnxruntime_data[0] + 
    cv2_data[0] + 
    [('src/ai_video/config', 'ai_video/config'), ('LICENSE', '.')]
)

binaries = (
    ai_video_data[1] + 
    insightface_data[1] + 
    onnxruntime_data[1] + 
    cv2_data[1]
)

hiddenimports = (
    ai_video_data[2] + 
    insightface_data[2] + 
    onnxruntime_data[2] + 
    cv2_data[2] + 
    ['scipy', 'yaml', 'PySide6']
)

ffmpeg_path = shutil.which("ffmpeg")
extra_binaries = []
if ffmpeg_path:
    extra_binaries.append((ffmpeg_path, '.'))

a = Analysis(
    ['run.py'],
    pathex=['src'],
    binaries=binaries + extra_binaries,
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