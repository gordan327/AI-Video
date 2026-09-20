from time import perf_counter
from typing import Any


class FrameProcessor:
    """執行單一影格的偵測、追蹤與隱私處理流程。"""

    def __init__(
        self,
        *,
        detector: Any,
        tracker: Any,
        renderer: Any,
    ):
        self.detector = detector
        self.tracker = tracker
        self.renderer = renderer

        self.detector_time = 0.0
        self.tracker_time = 0.0
        self.renderer_time = 0.0

    def process(
        self,
        frame: Any,
    ) -> tuple[Any, list[Any]]:
        """處理單一影格並記錄各階段耗時。"""

        detector_start = perf_counter()
        detections = self.detector.detect(frame)
        self.detector_time = (
            perf_counter() - detector_start
        )

        tracker_start = perf_counter()
        tracked_faces = self.tracker.track(detections)
        self.tracker_time = (
            perf_counter() - tracker_start
        )

        renderer_start = perf_counter()
        processed_frame = self.renderer.draw(
            frame,
            tracked_faces,
        )
        self.renderer_time = (
            perf_counter() - renderer_start
        )

        return processed_frame, tracked_faces
