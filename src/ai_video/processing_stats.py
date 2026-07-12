from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessingStats:
    """影片處理期間的即時統計資料。"""

    progress: int
    frame_index: int
    total_frames: int
    fps: float
    faces: int
    elapsed_seconds: float
    eta_seconds: float