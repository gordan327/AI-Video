from datetime import datetime
from pathlib import Path
from time import perf_counter

from PySide6.QtCore import QObject, QSettings, QThread, Signal, QTimer, Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox

from ai_video.config_manager import ConfigManager
from ai_video.gui.preferences_dialog import PreferencesDialog
from ai_video.gui.processing_configuration import ProcessingConfiguration
from ai_video.gui.processing_job import ProcessingJob
from ai_video.gui.processing_queue import (
    ProcessingQueue,
    ProcessingQueueStatus,
)
from ai_video.gui.processing_state_manager import ProcessingStateManager
from ai_video.gui.video_path_manager import VideoPathManager
from ai_video.gui.worker import VideoWorker
from ai_video.logger import Logger


class Controller(QObject):
    """處理 GUI 操作與影片處理流程。"""

    log_received = Signal(str)

    VIDEO_FILTER = (
        "影片檔案 (*.mp4 *.mov *.avi *.mkv *.m4v);;"
        "MP4 影片 (*.mp4);;"
        "所有檔案 (*)"
    )

    SESSION_SEPARATOR = "=" * 50
    SESSION_DETAIL_SEPARATOR = "-" * 50

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.settings = QSettings("AI-Video", "AI-Video")

        self.thread = None
        self.worker = None
        self.config = ConfigManager()
        self.processing_queue = ProcessingQueue()
        self.processing_started_at = None
        self.current_queue_item = None
        self.continue_queue_after_cleanup = False
        
        self.connect_signals()
        self.log_received.connect(self.window.append_log)
        Logger.subscribe(self.log_received.emit)
        Logger.info("AI-Video 已啟動")

    def add_log(self, message: str, level: str = "INFO"):
        log_methods = {
            "INFO": Logger.info,
            "SUCCESS": Logger.success,
            "WARNING": Logger.warning,
            "ERROR": Logger.error,
        }
        log_methods.get(level.upper(), Logger.info)(message)

    def connect_signals(self):
        self.window.input_button.clicked.connect(self.select_input_video)
        self.window.output_button.clicked.connect(self.select_output_video)
        self.window.add_queue_button.clicked.connect(self.add_video_to_queue)
        self.window.start_button.clicked.connect(self.start_processing)
        self.window.stop_button.clicked.connect(self.stop_processing)
        self.window.video_dropped.connect(self.handle_video_dropped)
        self.window.open_video_requested.connect(self.select_input_video)
        self.window.preferences_requested.connect(self.show_preferences)

    def set_input_video(self, filename: str):
        input_path = Path(filename)
        self.window.input_edit.setText(str(input_path))
        output_directory = self.settings.value("paths/output_directory", str(input_path.parent))
        output_path = VideoPathManager.build_default_output_path(input_path, output_directory)
        self.window.output_edit.setText(str(output_path))
        self.window.status_label.setText("已選擇輸入影片")
        self.add_log(f"已選擇輸入影片：{input_path}")
        self.window.add_queue_button.setEnabled(True)        
        self.add_log(f"預設輸出影片：{output_path}")

    @Slot(str)
    def handle_video_dropped(self, filename: str):
        if self.thread is not None:
            QMessageBox.information(self.window, "影片正在處理", "請等待目前的影片處理完成後，再拖入另一支影片。")
            return
        self.set_input_video(filename)
        self.add_log("影片已透過拖放方式加入")

    def select_input_video(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.window, "選擇輸入影片", self.settings.value("paths/input_directory", ""), self.VIDEO_FILTER
        )
        if not filename: return
        self.settings.setValue("paths/input_directory", str(Path(filename).parent))
        self.set_input_video(filename)

    def add_video_to_queue(self):
        input_text = self.window.input_edit.text().strip()
        output_text = self.window.output_edit.text().strip()
        if not input_text or not output_text:
            QMessageBox.warning(self.window, "無法加入佇列", "請先選擇輸入影片並指定輸出位置。")
            return
        item = self.processing_queue.add(Path(input_text), Path(output_text))
        if item is None:
            QMessageBox.information(self.window, "影片已在佇列中", "這支影片已經加入處理佇列。")
            return
        self.window.queue_list.addItem(f"等待處理｜{Path(input_text).name}")
        self.window.add_queue_button.setEnabled(False)
        self.window.status_label.setText("影片已加入處理佇列")
        self.add_log(f"已加入處理佇列：{input_text}")

    def select_output_video(self):
        current_output = self.window.output_edit.text().strip()
        output_directory = self.settings.value("paths/output_directory", "")
        output_name = Path(current_output).name if current_output else "output.mp4"
        initial_output = str(Path(output_directory) / output_name)
        filename, _ = QFileDialog.getSaveFileName(
            self.window, "指定輸出影片", initial_output, "MP4 影片 (*.mp4);;所有檔案 (*)",
            options=QFileDialog.Option.DontUseNativeDialog
        )
        if not filename: return
        self.settings.setValue("paths/output_directory", str(Path(filename).parent))
        output_path = VideoPathManager.build_output_path(filename)
        self.window.output_edit.setText(str(output_path))
        self.window.status_label.setText("已指定輸出影片")
        self.add_log(f"已指定輸出影片：{output_path}")

    def show_preferences(self):
        dialog = PreferencesDialog(self.window)
        dialog.set_values({
            "detector.model": self.config.get("detector.model", "buffalo_sc"),
            "detector.det_size": self.config.get("detector.det_size", 640),
            "detector.confidence": self.config.get("detector.confidence", 0.50),
            "runtime.provider": self.config.get("runtime.provider", "auto"),
        })
        if not dialog.exec(): return
        values = dialog.get_values()
        try:
            for key, value in values.items(): self.config.set(key, value)
            self.config.save()
        except OSError as error:
            QMessageBox.critical(self.window, "儲存偏好設定失敗", f"無法寫入設定檔：\n{error}")
            self.add_log(f"偏好設定儲存失敗：{error}", "ERROR")
            return
        self.add_log("偏好設定已儲存", "SUCCESS")

    def start_processing(self):
        if self.thread is not None:
            QMessageBox.information(self.window, "影片正在處理", "目前已有一項影片處理工作正在執行。")
            return

        queue_item = self.processing_queue.next_waiting()
        if queue_item:
            self.current_queue_item = queue_item
            input_text, output_text = str(queue_item.input_path), str(queue_item.output_path)
            try:
                queue_index = self.processing_queue.items.index(queue_item)
                self.window.queue_list.item(queue_index).setText(f"處理中｜{queue_item.input_path.name}")
            except (AttributeError, ValueError):
                pass
        else:
            input_text, output_text = self.window.input_edit.text().strip(), self.window.output_edit.text().strip()

        if not input_text or not Path(input_text).is_file():
            QMessageBox.warning(self.window, "錯誤", "請確認輸入影片路徑正確。")
            return
        
        output_path = Path(output_text)
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            QMessageBox.critical(self.window, "目錄建立失敗", str(e))
            return

        job = ProcessingJob(
            input_path=Path(input_text),
            output_path=output_path,
            temp_output_path=VideoPathManager.build_temp_output_path(output_path),
            detector=self.window.detector_combo.currentData(),
            tracker=self.window.tracker_combo.currentData(),
            renderer=self.window.renderer_combo.currentData(),
        )

        ProcessingConfiguration.apply(config=self.config, job=job)
        self.processing_started_at = perf_counter()
        self.log_processing_session_start(job.input_path, job.output_path)
        self.start_worker(job)

    def log_processing_session_start(self, input_path, output_path):
        started_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.add_log("")
        self.add_log(self.SESSION_SEPARATOR)
        self.add_log("AI-Video 影片處理工作")
        self.add_log(self.SESSION_SEPARATOR)
        self.add_log(f"開始時間：{started_time}")
        self.add_log(f"輸入影片：{input_path}")
        self.add_log(f"輸出影片：{output_path}")
        self.add_log(self.SESSION_DETAIL_SEPARATOR)

    def log_processing_session_end(self, result, level):
        elapsed = perf_counter() - self.processing_started_at if self.processing_started_at else 0
        self.add_log(self.SESSION_DETAIL_SEPARATOR)
        self.add_log(f"處理結果：{result}", level)
        self.add_log(f"總耗時：{elapsed:.2f} 秒")
        self.add_log(self.SESSION_SEPARATOR)
        self.processing_started_at = None

    def start_worker(self, job):
        """建立背景執行緒與 Worker (正確傳入 config)。"""
        self.thread = QThread()
        # 修正：VideoWorker 標準只接收 config，路徑已經透過 ProcessingConfiguration 寫入 config
        self.worker = VideoWorker(self.config)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.window.progress.setValue)
        self.worker.stats_changed.connect(self.window.update_processing_stats)
        self.worker.status_changed.connect(self.window.status_label.setText)
        self.worker.finished.connect(self.processing_finished)
        self.worker.cancelled.connect(self.processing_cancelled)
        self.worker.failed.connect(self.processing_failed)
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.cancelled.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)
        self.thread.finished.connect(self.cleanup_worker)

        self.set_processing_state(True)
        self.window.reset_processing_stats()
        self.window.progress.setValue(0)
        self.window.status_label.setText("正在準備影片處理……")
        self.thread.start()

    def stop_processing(self):
        if self.worker: self.worker.request_stop()

    def cleanup_worker(self):
        if self.worker: self.worker.deleteLater()
        if self.thread: self.thread.deleteLater()
        self.worker = None
        self.thread = None
        self.set_processing_state(False)

        should_continue = self.continue_queue_after_cleanup
        self.continue_queue_after_cleanup = False
        self.current_queue_item = None

        has_waiting_item = any(
            getattr(item, "status", None) is ProcessingQueueStatus.WAITING
            for item in getattr(self.processing_queue, "items", [])
        )

        if should_continue and has_waiting_item:
            QTimer.singleShot(0, self.start_processing)
        elif should_continue:
            completed_count = sum(
                getattr(item, "status", None) is ProcessingQueueStatus.COMPLETED
                for item in getattr(self.processing_queue, "items", [])
            )
            failed_count = sum(
                getattr(item, "status", None) is ProcessingQueueStatus.FAILED
                for item in getattr(self.processing_queue, "items", [])
            )
            QMessageBox.information(
                self.window,
                "佇列處理結束",
                f"所有等待中的影片均已處理。\n\n完成：{completed_count} 支\n失敗：{failed_count} 支",
            )

    @Slot(str)
    def processing_finished(self, output_path):
        self.window.progress.setValue(100)
        self.window.status_label.setText("影片處理完成")
        self.add_log(f"影片處理完成：{output_path}", "SUCCESS")
        self.log_processing_session_end("完成", "SUCCESS")

        if self.current_queue_item is not None:
            self.processing_queue.mark_completed(self.current_queue_item)
            try:
                queue_index = self.processing_queue.items.index(self.current_queue_item)
                self.window.queue_list.item(queue_index).setText(f"已完成｜{self.current_queue_item.input_path.name}")
            except (AttributeError, ValueError, IndexError):
                pass
            self.continue_queue_after_cleanup = True
        else:
            QMessageBox.information(self.window, "處理完成", f"影片已輸出至：\n{output_path}")

    @Slot()
    def processing_cancelled(self):
        self.window.progress.setValue(0)
        self.window.status_label.setText("影片處理已停止")
        self.add_log("使用者已停止影片處理", "WARNING")
        self.log_processing_session_end("使用者停止", "WARNING")

        if self.current_queue_item is not None:
            self.processing_queue.mark_cancelled(self.current_queue_item)
            try:
                queue_index = self.processing_queue.items.index(self.current_queue_item)
                self.window.queue_list.item(queue_index).setText(f"已停止｜{self.current_queue_item.input_path.name}")
            except (AttributeError, ValueError, IndexError):
                pass
            self.continue_queue_after_cleanup = False

        QMessageBox.information(self.window, "處理已停止", "影片處理工作已停止，暫存檔案已清除。")

    @Slot(str)
    def processing_failed(self, message):
        self.window.progress.setValue(0)
        self.window.status_label.setText("影片處理失敗")
        self.add_log(message, "ERROR")
        self.log_processing_session_end("失敗", "ERROR")

        if self.current_queue_item is not None:
            self.processing_queue.mark_failed(self.current_queue_item, message)
            try:
                queue_index = self.processing_queue.items.index(self.current_queue_item)
                self.window.queue_list.item(queue_index).setText(f"處理失敗｜{self.current_queue_item.input_path.name}")
            except (AttributeError, ValueError, IndexError):
                pass
            self.continue_queue_after_cleanup = True

        if self.current_queue_item is not None and hasattr(self.current_queue_item, "input_path"):
            failed_name = self.current_queue_item.input_path.name
            user_message = f"無法處理影片：{failed_name}\n\n請確認檔案格式及內容是否正常。\n詳細資訊已保留在執行紀錄中。"
        else:
            user_message = "影片處理失敗。\n\n請確認檔案格式及內容是否正常。\n詳細資訊已保留在執行紀錄中。"

        QMessageBox.critical(self.window, "影片處理失敗", user_message)

    def set_processing_state(self, processing):
        ProcessingStateManager.apply(window=self.window, processing=processing)