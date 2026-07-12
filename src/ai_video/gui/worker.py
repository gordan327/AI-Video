from threading import Event

from PySide6.QtCore import QObject, Signal, Slot

from ai_video.processor import VideoProcessor


class Worker(QObject):
    """在背景執行影片處理工作。"""

    finished = Signal(str)
    cancelled = Signal()
    failed = Signal(str)

    progress = Signal(int)
    status_changed = Signal(str)

    def __init__(self, config):
        super().__init__()

        self.config = config
        self.stop_event = Event()

    @Slot()
    def run(self):
        """執行影片處理流程。"""

        try:
            processor = VideoProcessor(
                config=self.config,
                progress_callback=self.progress.emit,
                status_callback=self.status_changed.emit,
                stop_checker=self.stop_event.is_set,
            )

            completed = processor.run()

            if completed:
                self.finished.emit(
                    self.config.get("video.output")
                )
            else:
                self.cancelled.emit()

        except Exception as error:
            self.failed.emit(
                f"{type(error).__name__}: {error}"
            )

    def request_stop(self):
        """通知影片處理器停止工作。"""

        self.stop_event.set()