# AI-Video API Reference

> Version: 0.7

本文件整理 AI-Video 目前主要的公開介面與擴充點。

---

## 1. Domain Model

### `Face`

檔案：

```text
src/ai_video/face.py
```

代表一張偵測或追蹤到的人臉。

```python
@dataclass
class Face:
    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float
    track_id: int | None = None
    embedding: np.ndarray | None = None
```

主要欄位：

- `x1`, `y1`：左上角座標
- `x2`, `y2`：右下角座標
- `confidence`：偵測信心值
- `track_id`：追蹤編號
- `embedding`：人臉特徵向量

---

## 2. Detector API

### `FaceDetector`

檔案：

```text
src/ai_video/detector/face_detector.py
```

所有人臉偵測器的共同介面。

```python
class FaceDetector(ABC):

    @abstractmethod
    def detect(
        self,
        frame,
    ) -> list[Face]:
        ...
```

#### `detect(frame)`

輸入：

- OpenCV 影格
- 通常為 `numpy.ndarray`

輸出：

```python
list[Face]
```

目前實作：

- `SCRFDFaceDetector`
- `YOLOFaceDetector`
- `DummyFaceDetector`

---

### `DetectorFactory`

檔案：

```text
src/ai_video/detector/detector_factory.py
```

依照內部識別碼建立 Detector。

```python
detector = DetectorFactory.create(
    detector_type="scrfd",
    model_manager=model_manager,
    config=config,
)
```

目前支援：

```text
scrfd
```

若類型不存在，會拋出：

```python
ValueError
```

---

## 3. Tracker API

### `FaceTracker`

檔案：

```text
src/ai_video/tracker/face_tracker.py
```

所有人臉追蹤器的共同介面。

```python
class FaceTracker(ABC):

    @abstractmethod
    def track(
        self,
        faces: list[Face],
    ) -> list[Face]:
        ...
```

#### `track(faces)`

輸入：

```python
list[Face]
```

輸出：

```python
list[Face]
```

輸出的 `Face` 通常會包含：

```python
track_id
```

目前實作：

- `ByteTrackFaceTracker`
- `DummyFaceTracker`

---

### `ByteTrackFaceTracker`

檔案：

```text
src/ai_video/tracker/bytetrack_face_tracker.py
```

建構方式：

```python
tracker = ByteTrackFaceTracker(
    privacy_hold_frames=15,
    prediction_frames=3,
    freeze_expansion_per_frame=0.03,
)
```

參數：

- `privacy_hold_frames`：漏偵測後持續保護的影格數
- `prediction_frames`：使用 Kalman 預測的影格數
- `freeze_expansion_per_frame`：凍結期間每幀擴張比例

---

### `TrackerFactory`

檔案：

```text
src/ai_video/tracker/tracker_factory.py
```

建立 Tracker：

```python
tracker = TrackerFactory.create(
    tracker_type="bytetrack",
    privacy_hold_frames=15,
    prediction_frames=3,
    freeze_expansion_per_frame=0.03,
)
```

目前支援：

```text
bytetrack
```

---

## 4. Renderer API

### `BaseRenderer`

檔案：

```text
src/ai_video/renderer/base_renderer.py
```

所有隱私呈現方式的共同介面。

```python
class BaseRenderer(ABC):

    @abstractmethod
    def render(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        ...
```

#### `render(frame, box)`

輸入：

- `frame`：OpenCV 影格
- `box`：矩形座標

```python
(
    x1,
    y1,
    x2,
    y2,
)
```

Renderer 直接修改傳入的影格，不需要回傳新的影格。

目前實作：

- `BlurRenderer`
- `PixelateRenderer`

---

### `BlurRenderer`

檔案：

```text
src/ai_video/renderer/blur_renderer.py
```

建立方式：

```python
renderer = BlurRenderer(
    blur_strength=51,
)
```

參數：

- `blur_strength`：Gaussian Blur 核心大小
- 偶數會自動調整成奇數
- 最小值為 3

使用：

```python
renderer.render(
    frame,
    (x1, y1, x2, y2),
)
```

---

### `PixelateRenderer`

檔案：

```text
src/ai_video/renderer/pixelate_renderer.py
```

建立方式：

```python
renderer = PixelateRenderer(
    pixel_size=12,
)
```

參數：

- `pixel_size`：馬賽克區塊大小
- 數值越大，馬賽克越粗

---

### `RendererFactory`

檔案：

```text
src/ai_video/renderer/renderer_factory.py
```

建立 Blur：

```python
renderer = RendererFactory.create(
    renderer_type="blur",
    blur_strength=51,
)
```

建立 Pixelate：

```python
renderer = RendererFactory.create(
    renderer_type="pixelate",
    pixel_size=12,
)
```

目前支援：

```text
blur
pixelate
```

---

## 5. Privacy Region API

### `PrivacyBox`

檔案：

```text
src/ai_video/privacy_region.py
```

代表需要進行隱私處理的矩形區域。

```python
@dataclass(frozen=True)
class PrivacyBox:
    x1: int
    y1: int
    x2: int
    y2: int
```

提供：

```python
box.width
box.height
box.is_valid
box.as_tuple()
```

---

### `PrivacyRegion`

負責將人臉框擴張成頭部隱私區域。

```python
region = PrivacyRegion(
    padding_ratio=0.35,
    top_multiplier=1.7,
    bottom_multiplier=0.8,
)
```

建立隱私區域：

```python
privacy_box = region.create(
    face=face,
    frame_width=1920,
    frame_height=1080,
)
```

回傳：

```python
PrivacyBox | None
```

---

## 6. Face Renderer API

### `FaceRenderer`

檔案：

```text
src/ai_video/face_renderer.py
```

`FaceRenderer` 負責協調：

- PrivacyRegion
- Temporal Hold
- RendererFactory
- Blur 或 Pixelate 效果

建立方式：

```python
renderer = FaceRenderer(
    renderer_type="blur",
    blur_strength=51,
    pixel_size=12,
    padding_ratio=0.35,
    temporal_hold_frames=5,
)
```

使用：

```python
frame = renderer.draw(
    frame,
    faces,
)
```

清除歷史快取：

```python
renderer.reset()
```

---

## 7. Configuration API

### `ConfigManager`

檔案：

```text
src/ai_video/config_manager.py
```

建立：

```python
config = ConfigManager()
```

讀取設定：

```python
value = config.get(
    "renderer.type",
    "blur",
)
```

修改設定：

```python
config.set(
    "renderer.type",
    "pixelate",
)
```

儲存：

```python
config.save()
```

重新載入：

```python
config.reload()
```

常用設定：

```text
video.input
video.output
video.temp_output

detector.type
detector.model
detector.det_size
detector.confidence

tracker.type
tracker.privacy_hold_frames
tracker.prediction_frames
tracker.freeze_expansion_per_frame

renderer.type
renderer.blur_strength
renderer.pixel_size
renderer.padding_ratio
renderer.temporal_hold_frames

runtime.provider
```

---

## 8. Video API

### `VideoReader`

檔案：

```text
src/ai_video/video/video_reader.py
```

建立：

```python
reader = VideoReader(
    video_path,
)
```

主要方法：

```python
reader.open()
success, frame = reader.read()
reader.close()
```

主要屬性：

```python
reader.fps
reader.width
reader.height
reader.frame_count
reader.duration
```

---

### `VideoWriter`

檔案：

```text
src/ai_video/video/video_writer.py
```

建立：

```python
writer = VideoWriter(
    output_path=output_path,
    fps=30.0,
    width=1920,
    height=1080,
)
```

使用：

```python
writer.open()
writer.write(frame)
writer.close()
```

---

### `FFmpegProcessor`

檔案：

```text
src/ai_video/video/ffmpeg_processor.py
```

合併原始音訊：

```python
ffmpeg.merge_audio(
    original_video=input_path,
    processed_video=temp_path,
    output_video=output_path,
)
```

需要系統已安裝：

```text
ffmpeg
```

---

## 9. Processing API

### `VideoProcessor`

檔案：

```text
src/ai_video/processor.py
```

建立：

```python
processor = VideoProcessor(
    config=config,
    progress_callback=progress_callback,
    status_callback=status_callback,
    stats_callback=stats_callback,
    stop_checker=stop_checker,
)
```

執行：

```python
completed = processor.run()
```

回傳：

```python
True
```

代表正常完成。

```python
False
```

代表使用者中途停止。

---

### Callback

進度：

```python
progress_callback(
    progress: int,
)
```

狀態：

```python
status_callback(
    message: str,
)
```

即時統計：

```python
stats_callback(
    stats: ProcessingStats,
)
```

停止檢查：

```python
stop_checker() -> bool
```

---

## 10. Processing Statistics

### `ProcessingStats`

檔案：

```text
src/ai_video/processing_stats.py
```

用於回報即時處理資訊。

主要欄位：

```text
progress
frame_index
total_frames
fps
faces
elapsed_seconds
eta_seconds
```

---

## 11. Logger API

### `Logger`

檔案：

```text
src/ai_video/logger.py
```

使用：

```python
Logger.info(
    "開始處理影片"
)

Logger.success(
    "影片處理完成"
)

Logger.warning(
    "影片處理已停止"
)

Logger.error(
    "影片處理失敗"
)
```

訂閱 Log：

```python
Logger.subscribe(
    listener,
)
```

取消訂閱：

```python
Logger.unsubscribe(
    listener,
)
```

---

## 12. API Stability

目前 AI-Video 尚在 Beta 階段。

下列介面可視為主要擴充點：

```text
FaceDetector.detect()
FaceTracker.track()
BaseRenderer.render()
DetectorFactory.create()
TrackerFactory.create()
RendererFactory.create()
```

內部 tracking 演算法目前不保證 API 穩定：

```text
tracking.assignment
tracking.cost_matrix
tracking.kalman_filter
tracking.matching
tracking.track_manager
```

這些模組可能在未來版本調整。