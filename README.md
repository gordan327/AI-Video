# AI-Video

AI-Video 是一套開放且可擴充的影片隱私保護引擎。

> AI-powered video privacy toolkit for educational activities.

## 專案目標

AI-Video 是一套專為教育活動設計的 AI 影片處理工具。

第一階段目標：

- 自動偵測影片中的人臉
- 自動追蹤人臉
- 自動模糊人臉
- 保留原始畫質
- 保留原始音訊
- 一鍵完成處理

---

## 專案狀態

目前版本：

Version 0.1（Planning）

---

## 開發環境

- macOS (Apple Silicon)
- Python 3
- OpenCV
- YOLO
- FFmpeg

---

## 專案作者

謝國清

# AI-Video

AI-Video 是一套以 Python 開發的影片隱私保護工具，專注於自動偵測、追蹤與匿名化影片中的人臉。

目前支援高品質人臉模糊（Blur）與馬賽克（Pixelate），並採用可擴充（Plugin）的 Renderer 架構，方便未來加入更多隱私保護方式。

---

## 主要功能

- 🎯 SCRFD 人臉偵測
- 🎯 ByteTrack 人臉追蹤
- 🎯 Gaussian Blur 人臉模糊
- 🎯 Pixelate（馬賽克）
- 🎯 Smart Privacy Region
- 🎯 Temporal Hold（短暫漏偵測仍持續保護）
- 🎯 Prediction Freeze
- 🎯 GUI 操作介面
- 🎯 即時處理資訊
- 🎯 可設定偏好設定
- 🎯 Plugin Renderer Architecture
- 🎯 自動測試（pytest）

---

## 系統需求

- Python 3.12+
- macOS
- Windows（預計支援）

---

## 安裝

建立虛擬環境：

```bash
python -m venv .venv
```

啟動：

macOS / Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

安裝套件：

```bash
pip install -e .
```

---

## 執行 GUI

```bash
PYTHONPATH=src python -m ai_video.gui.app
```

---

## 執行測試

```bash
PYTHONPATH=src pytest
```

---

## 專案架構

```text
src/
└── ai_video/
    ├── detector/
    ├── tracker/
    ├── renderer/
    ├── gui/
    ├── config/
    ├── processor.py
    └── ...
```

---

## Renderer Plugin

目前支援：

- Blur
- Pixelate

未來規劃：

- Solid Color
- Emoji
- Mosaic
- AI Replace

---

## Roadmap

### Version 0.6 Beta

- Renderer Plugin
- Pixelate Renderer
- 自動測試
- 中文 GUI

### Version 0.7

- Detector Factory
- Tracker Factory
- Plugin Registry

### Version 0.8

- 更多 Renderer
- 更完整 Preferences

### Version 1.0

- Plugin SDK
- 自動載入 Renderer
- 正式版發布

---

## License

MIT License

---

## Author

KuoChing Hsieh

AI-Video Project