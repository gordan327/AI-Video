from dataclasses import dataclass


@dataclass
class PerformanceStatistics:
    """記錄影片處理各模組的累積執行時間。"""

    detector_time: float = 0.0
    tracker_time: float = 0.0
    renderer_time: float = 0.0
    writer_time: float = 0.0

    def add_detector_time(
        self,
        elapsed_time: float,
    ):
        """累加人臉偵測耗時。"""

        self.detector_time += elapsed_time

    def add_tracker_time(
        self,
        elapsed_time: float,
    ):
        """累加人臉追蹤耗時。"""

        self.tracker_time += elapsed_time

    def add_renderer_time(
        self,
        elapsed_time: float,
    ):
        """累加畫面遮蔽處理耗時。"""

        self.renderer_time += elapsed_time

    def add_writer_time(
        self,
        elapsed_time: float,
    ):
        """累加影片寫入耗時。"""

        self.writer_time += elapsed_time

    def reset(self):
        """將所有效能統計資料歸零。"""

        self.detector_time = 0.0
        self.tracker_time = 0.0
        self.renderer_time = 0.0
        self.writer_time = 0.0