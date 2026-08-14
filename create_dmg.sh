#!/bin/bash
set -e

APP_NAME="app"
DMG_NAME="AI-Video-Mac-x64.dmg"
DIST_DIR="dist"
STAGING_DIR="dist/dmg_staging"

echo "🚀 開始製作 macOS DMG 安裝檔..."

rm -rf "$STAGING_DIR" "$DIST_DIR/$DMG_NAME"
mkdir -p "$STAGING_DIR"

echo "📦 複製 $APP_NAME.app..."
cp -R "$DIST_DIR/$APP_NAME.app" "$STAGING_DIR/"

echo "🔗 建立 Applications 資料夾捷徑..."
ln -s /Applications "$STAGING_DIR/Applications"

echo "💿 正在生成 DMG 映像檔..."
hdiutil create -volname "$APP_NAME Installer" -srcfolder "$STAGING_DIR" -ov -format UDZO "$DIST_DIR/$DMG_NAME"

rm -rf "$STAGING_DIR"

echo "✅ DMG 安裝檔製作成功！檔案位置: $DIST_DIR/$DMG_NAME"
