# AI-Video Architecture

## 1. 專案目標

AI-Video 是一套桌面影片處理工具，主要目標是：

- 自動偵測影片中的人臉
- 持續追蹤人臉
- 對人臉進行模糊化或其他隱私處理
- 保留原始影片音訊
- 提供一般使用者可操作的圖形介面
- 未來可擴充不同偵測器、追蹤器與影像處理方式

目前主要執行平台為 macOS，未來規劃支援 Windows。

---

## 2. 系統主要架構

AI-Video 目前分為以下幾個主要部分：

```text
MainWindow
    │
    ▼
Controller
    │
    ▼
Worker / QThread
    │
    ▼
VideoProcessor
    │
    ├── VideoReader
    ├── FaceDetector
    ├── FaceTracker
    ├── FaceRenderer
    ├── VideoWriter
    └── FFmpegProcessor