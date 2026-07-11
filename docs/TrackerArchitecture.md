# AI-Video Tracker Architecture

Version: 1.0

---

# 1. 目標

AI-Video 的 Tracker 負責：

- 為每張人臉建立 Track
- 維持 Track ID 穩定
- 即使短暫遮擋仍維持同一個 ID
- 支援多人同時追蹤
- 提供 Renderer 使用

---

# 2. 系統架構

Video
    │
    ▼
Face Detector
    │
    ▼
Face
    │
    ▼
Matcher
    │
    ▼
TrackManager
    │
    ▼
Track
    │
    ├── Face
    ├── Kalman Filter
    ├── Track ID
    ├── Age
    ├── Missed
    └── (Future) Embedding

---

# 3. 類別職責

## Face

代表單一 Frame 偵測到的人臉。

包含：

- Bounding Box
- Score
- Landmark
- Embedding（Future）
- Track ID

---

## Track

代表持續存在的人。

包含：

- Track ID
- 最新 Face
- Kalman Filter
- Age
- Missed Count

---

## Matcher

負責：

Track ↔ Face

配對。

目前：

- IoU
- Center Distance

未來：

- Hungarian Assignment
- ReID

---

## TrackManager

負責：

- Create Track
- Update Track
- Remove Track
- Track Lifecycle

---

## Kalman Filter

負責：

- Predict
- Update

不負責：

- 配對
- 建立 Track
- Renderer

---

# 4. Data Flow

Frame

↓

Detector

↓

Face

↓

Matcher

↓

TrackManager

↓

Renderer

---

# 5. Future Roadmap

Milestone 14
Kalman Prediction

Milestone 15
Face Embedding (ReID)

Milestone 16
Hungarian Assignment

Milestone 17
Face Blur

Milestone 18
GUI