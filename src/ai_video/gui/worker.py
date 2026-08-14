import traceback
from PySide6.QtCore import QObject, Signal
from ai_video.config_manager import ConfigManager
from ai_video.processor import VideoProcessor  # 使用正確的 VideoProcessor
from ai_video.logger import Logger


class VideoWorker(QObject):
    """背景影片處理工作物件 (對齊專案原本的 VideoProcessor 架構)。"""

    progress = Signal(int)
    stats_changed = Signal(dict)
    status_changed = Signal(str)
    finished = Signal(str)
    cancelled = Signal()
    failed = Signal(str)

    def __init__(self, config: ConfigManager, parent=None):
        super().__init__(parent)
        self.config = config
        self._stop_requested = False

    def request_stop(self):
        """通知影片處理器停止工作。"""
        Logger.warning("背景影片處理工作已停止")
        self._stop_requested = True

    def run(self):
        """執行影片處理流程。"""
        Logger.info("背景影片處理工作已啟動")

        try:
            # 建立專案原生的 VideoProcessor，並將 GUI 的訊號回報對應進去
            processor = VideoProcessor(
                config=self.config,
                progress_callback=self.progress.emit,
                status_callback=self.status_changed.emit,
                stats_callback=self.stats_changed.emit,
                stop_checker=lambda: self._stop_requested,
            )

            completed = processor.run()

            if completed:
                Logger.success("背景影片處理工作完成")
                output_path = self.config.get("video.output") or self.config.get("job.output_path", "")
                self.finished.emit(str(output_path))
            else:
                self.cancelled.emit()

        except Exception:
            error_message = traceback.format_exc()
            Logger.error(error_message)
            self.failed.emit(error_message)


# 相容性別名
Worker = VideoWorker