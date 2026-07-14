# AI-Video Architecture

AI-Video 是一套以 Python 開發的影片隱私保護引擎（Privacy Protection Engine）。

系統採用模組化（Modular）、可擴充（Extensible）以及 Plugin 架構設計，將人臉偵測、追蹤、隱私區域計算與影像處理彼此分離，使每個元件都可以獨立演進與測試。

---

# Overall Architecture

```text
                        GUI
                         │
                    Controller
                         │
                  VideoProcessor
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   FaceDetector     FaceTracker     FaceRenderer
        │                │                │
        ▼                ▼                ▼
      SCRFD         ByteTrack      RendererFactory
                                              │
                           ┌──────────────────┴──────────────────┐
                           ▼                                     ▼
                    BlurRenderer                       PixelateRenderer
```

---

# Processing Pipeline

每一支影片都依照下列流程處理：

```text
Video
  │
  ▼
Read Frame
  │
  ▼
Face Detection
  │
  ▼
Face Tracking
  │
  ▼
Privacy Region
  │
  ▼
Renderer
  │
  ▼
Write Frame
  │
  ▼
Output Video
```

---

# Core Components

## FaceDetector

負責：

- 人臉偵測
- 輸出 Face 物件
- 不負責追蹤

目前支援：

- SCRFD

未來規劃：

- RetinaFace
- YOLO Face

---

## FaceTracker

負責：

- Track ID 管理
- Kalman Prediction
- IoU Matching
- Embedding Matching
- Temporal Hold

目前支援：

- ByteTrack

未來規劃：

- DeepSORT
- StrongSORT

---

## PrivacyRegion

PrivacyRegion 負責將 Detector 回傳的人臉框擴張成真正需要保護的頭部區域。

例如：

```text
Detector Box

+--------+

↓

Privacy Region

+--------------+
|              |
|    Head      |
|              |
+--------------+
```

主要考量：

- 頭髮
- 耳朵
- 側臉
- 下巴

---

## Renderer

Renderer 只負責：

> 如何保護指定區域。

目前 Renderer 完全不知道：

- Detector
- Tracker
- GUI

只需要：

```python
render(frame, box)
```

即可。

目前支援：

- Blur
- Pixelate

未來規劃：

- Solid Color
- Emoji
- Mosaic
- AI Replace

---

# Renderer Plugin Architecture

```text
BaseRenderer
      ▲
      │
 ┌────┴────────────┐
 │                 │
 ▼                 ▼
BlurRenderer   PixelateRenderer
```

RendererFactory 負責建立 Renderer。

```text
Config

↓

RendererFactory

↓

Renderer
```

因此新增新的 Renderer 時：

1. 新增 Renderer 類別
2. 註冊到 Factory

即可完成擴充。

---

# Configuration

所有元件都透過 ConfigManager 取得設定。

例如：

```yaml
renderer:
  type: blur
  blur_strength: 51
  pixel_size: 12
```

GUI 不直接控制 Renderer，而是修改設定。

---

# GUI Architecture

```text
MainWindow
      │
      ▼
Controller
      │
      ▼
Worker Thread
      │
      ▼
VideoProcessor
```

GUI 不直接操作任何演算法。

所有影片處理皆在背景執行。

---

# Testing

目前已建立 pytest 自動測試。

包含：

- RendererFactory
- BlurRenderer
- FaceRenderer
- PrivacyRegion

目的：

- 防止重構造成 Regression
- 提升程式可靠性
- 縮短測試時間

---

# Design Principles

AI-Video 遵循下列設計原則：

- Single Responsibility Principle (SRP)
- Open / Closed Principle (OCP)
- Composition over Inheritance
- Plugin Architecture
- Config-driven Design
- Testable Components

---

# Future Roadmap

## Version 0.7

- DetectorFactory
- TrackerFactory

---

## Version 0.8

- Plugin Registry
- 更多 Renderer

---

## Version 1.0

- Plugin SDK
- 自動載入 Renderer
- Third-party Renderer Support
- 正式版發布