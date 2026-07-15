from pathlib import Path

from ai_video.processor import VideoProcessor


class DummyConfig:
    """提供 VideoProcessor 初始化所需的最小設定。"""

    def __init__(self):
        self.values = {
            "video.input": str(
                Path("tests/data/dummy.mp4")
            ),
            "detector.type": "scrfd",
            "tracker.type": "bytetrack",
            "renderer.type": "blur",
            "tracker.privacy_hold_frames": 15,
            "tracker.prediction_frames": 3,
            "tracker.freeze_expansion_per_frame": 0.03,
            "renderer.blur_strength": 51,
            "renderer.pixel_size": 12,
            "renderer.padding_ratio": 0.35,
            "renderer.temporal_hold_frames": 5,
        }

    def get(
        self,
        key,
        default=None,
    ):
        return self.values.get(
            key,
            default,
        )


class DummyModelManager:
    """避免測試期間載入真實 AI 模型。"""

    def __init__(self, config):
        self.config = config
        self.face_analysis = object()


def test_processor_create(
    monkeypatch,
):
    """VideoProcessor 應能完成初始化。"""

    monkeypatch.setattr(
        "ai_video.processor.ModelManager",
        DummyModelManager,
    )

    processor = VideoProcessor(
        config=DummyConfig(),
    )

    assert processor is not None


def test_processor_components(
    monkeypatch,
):
    """Processor 應建立主要處理元件。"""

    monkeypatch.setattr(
        "ai_video.processor.ModelManager",
        DummyModelManager,
    )

    processor = VideoProcessor(
        config=DummyConfig(),
    )

    assert processor.reader is not None
    assert processor.detector is not None
    assert processor.tracker is not None
    assert processor.renderer is not None
    assert processor.ffmpeg is not None


def test_processor_callbacks_are_preserved(
    monkeypatch,
):
    """傳入的 Callback 應保存在 Processor 中。"""

    monkeypatch.setattr(
        "ai_video.processor.ModelManager",
        DummyModelManager,
    )

    progress_callback = lambda value: None
    status_callback = lambda message: None
    stats_callback = lambda stats: None
    stop_checker = lambda: False

    processor = VideoProcessor(
        config=DummyConfig(),
        progress_callback=progress_callback,
        status_callback=status_callback,
        stats_callback=stats_callback,
        stop_checker=stop_checker,
    )

    assert (
        processor.progress_callback
        is progress_callback
    )

    assert (
        processor.status_callback
        is status_callback
    )

    assert (
        processor.stats_callback
        is stats_callback
    )

    assert (
        processor.stop_checker
        is stop_checker
    )


def test_processor_initial_timing_values(
    monkeypatch,
):
    """處理時間統計初始值應為零。"""

    monkeypatch.setattr(
        "ai_video.processor.ModelManager",
        DummyModelManager,
    )

    processor = VideoProcessor(
        config=DummyConfig(),
    )

    assert processor.detector_time == 0.0
    assert processor.tracker_time == 0.0
    assert processor.renderer_time == 0.0
    assert processor.writer_time == 0.0
    assert processor.current_faces == []