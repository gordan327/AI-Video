from ai_video.processing.frame_processor import (
    FrameProcessor,
)


class DummyDetector:
    def __init__(self):
        self.received_frame = None

    def detect(self, frame):
        self.received_frame = frame

        return ["detection-1"]


class DummyTracker:
    def __init__(self):
        self.received_detections = None

    def track(self, detections):
        self.received_detections = detections

        return ["tracked-face-1"]


class DummyRenderer:
    def __init__(self):
        self.received_frame = None
        self.received_faces = None

    def draw(self, frame, faces):
        self.received_frame = frame
        self.received_faces = faces

        return "processed-frame"


def test_frame_processor_runs_pipeline():
    """應依序執行偵測、追蹤與繪製流程。"""

    detector = DummyDetector()
    tracker = DummyTracker()
    renderer = DummyRenderer()

    processor = FrameProcessor(
        detector=detector,
        tracker=tracker,
        renderer=renderer,
    )

    processed_frame, tracked_faces = processor.process(
        "original-frame"
    )

    assert detector.received_frame == "original-frame"

    assert tracker.received_detections == [
        "detection-1"
    ]

    assert renderer.received_frame == "original-frame"
    assert renderer.received_faces == [
        "tracked-face-1"
    ]

    assert processed_frame == "processed-frame"
    assert tracked_faces == ["tracked-face-1"]


def test_frame_processor_keeps_components():
    """應保留傳入的偵測器、追蹤器與繪製器。"""

    detector = DummyDetector()
    tracker = DummyTracker()
    renderer = DummyRenderer()

    processor = FrameProcessor(
        detector=detector,
        tracker=tracker,
        renderer=renderer,
    )

    assert processor.detector is detector
    assert processor.tracker is tracker
    assert processor.renderer is renderer
