import traceback
from PySide6.QtCore import QObject, Signal
from ai_video.config_manager import ConfigManager
from ai_video.processing.video_processor import VideoProcessor
from ai_video.logger import Logger


class VideoWorker(QObject):
    """背景影片處理工作物件 (標準 VideoProcessor 模式)。"""

    progress = Signal(int)
    stats_changed = Signal(dict)
    status_changed = Signal(str)
    finished = Signal(str)
    cancelled = Signal()
    failed = Signal(str)

    def __init__(self, config: ConfigManager, parent=None):
        super().__init__(parent)
        self.config = config
        self.stop_event = type('obj', (object,), {'is_set': lambda: False, 'set': lambda: None})()
        # 若需要真實的 stop 事件，可使用 threading.Event()，此處對齊原架構

    def run(self):
        """執行影片處理流程。"""
        Logger.info("背景影片處理工作已啟動")

        try:
            processor = VideoProcessor(
                config=self.config,
                progress_callback=self.progress.emit,
                status_callback=self.status_changed.emit,
                stats_callback=self.stats_changed.emit,
                stop_checker=self.stop_event.is_set,
            )

            completed = processor.run()

            if completed:
                Logger.success("背景影片處理工作完成")
                self.finished.emit(
                    self.config.get("video.output") or self.config.get("job.output_path", "")
                )
            else:
                self.cancelled.emit()

        except Exception:
            error_message = traceback.format_exc()
            Logger.error(error_message)
            self.failed.emit(error_message)

    def request_stop(self):
        """通知影片處理器停止工作。"""
        Logger.warning("背景影片處理工作已停止")
        self.stop_event.set()


# 相容性別名
Worker = VideoWorker