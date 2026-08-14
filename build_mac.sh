#!/bin/bash
set -e

echo "🚀 開始執行 AI-Video macOS 應用程式打包流程..."

# 1. 啟用虛擬環境
source .venv/bin/activate

# 2. 確定系統中的 ffmpeg 路徑
FFMPEG_PATH=$(which ffmpeg)
echo "🔍 找到 FFmpeg 路徑: $FFMPEG_PATH"

# 3. 執行 Nuitka 打包
PYTHONUTF8=1 python -m nuitka \
  --standalone \
  --macos-create-app-bundle \
  --macos-app-name="AI-Video" \
  --macos-app-mode=gui \
  --macos-app-icon=none \
  --enable-plugin=pyside6 \
  --include-package=scipy \
  --include-data-dir=src/ai_video/config=ai_video/config \
  --include-data-files="$FFMPEG_PATH=ffmpeg" \
  --output-dir=dist \
  --nofollow-import-to=torch \
  --nofollow-import-to=torchvision \
  --nofollow-import-to=pytest \
  --nofollow-import-to=matplotlib \
  --nofollow-import-to=fonttools \
  --nofollow-import-to=contourpy \
  --nofollow-import-to=kiwisolver \
  --nofollow-import-to=cycler \
  --nofollow-import-to=nvidia_ml_py \
  --nofollow-import-to=IPython \
  --nofollow-import-to=notebook \
  src/ai_video/gui/app.py

# 4. 清除 macOS 下載隔離標記
xattr -cr dist/app.app

echo "✅ 打包完成！應用程式位置: dist/app.app"