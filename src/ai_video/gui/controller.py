from pathlib import Path

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QFileDialog, QMessageBox

from ai_video.gui.worker import Worker


class GuiConfig:
    """
    提供 VideoProcessor 所需的簡易設定介面。

    介面與原本 ConfigManager 的 get() 方法相容。
    """

    def __init__(self, values):
        self.values = values

    def get(self, key, default=None):
        return self.values.get(key, default)


class Controller:
    """處理 GUI 操作與影片處理流程。"""

    VIDEO_FILTER = (
        "影片檔案 (*.mp4 *.mov *.avi *.mkv *.m4v);;"
        "MP4 影片 (*.mp4);;"
        "所有檔案 (*)"
    )

    def __init__(self, window):
        self.window = window

        self.thread = None
        self.worker = None

        self.connect_signals()

    def connect_signals(self):
        """連接畫面元件與控制函式。"""

        self.window.input_button.clicked.connect(
            self.select_input_video
        )

        self.window.output_button.clicked.connect(
            self.select_output_video
        )

        self.window.start_button.clicked.connect(
            self.start_processing
        )

        self.window.stop_button.clicked.connect(
            self.stop_processing
        )

    def select_input_video(self):
        """選擇輸入影片。"""

        filename, _ = QFileDialog.getOpenFileName(
            self.window,
            "選擇輸入影片",
            "",
            self.VIDEO_FILTER,
        )

        if not filename:
            return

        input_path = Path(filename)

        self.window.input_edit.setText(str(input_path))

        output_path = input_path.with_name(
            f"{input_path.stem}_blurred.mp4"
        )

        self.window.output_edit.setText(str(output_path))
        self.window.status_label.setText("已選擇輸入影片")

    def select_output_video(self):
        """指定輸出影片的位置。"""

        current_output = self.window.output_edit.text().strip()

        filename, _ = QFileDialog.getSaveFileName(
            self.window,
            "指定輸出影片",
            current_output,
            "MP4 影片 (*.mp4);;所有檔案 (*)",
        )

        if not filename:
            return

        output_path = Path(filename)

        if not output_path.suffix:
            output_path = output_path.with_suffix(".mp4")

        self.window.output_edit.setText(str(output_path))
        self.window.status_label.setText("已指定輸出影片")

    def start_processing(self):
        """檢查設定並啟動背景影片處理。"""

        if self.thread is not None:
            QMessageBox.information(
                self.window,
                "影片正在處理",
                "目前已有一項影片處理工作正在執行。",
            )
            return

        input_text = self.window.input_edit.text().strip()
        output_text = self.window.output_edit.text().strip()

        if not input_text:
            QMessageBox.warning(
                self.window,
                "缺少輸入影片",
                "請先選擇要處理的影片。",
            )
            return

        input_path = Path(input_text)

        if not input_path.is_file():
            QMessageBox.warning(
                self.window,
                "找不到輸入影片",
                f"找不到指定的影片：\n{input_path}",
            )
            return

        if not output_text:
            QMessageBox.warning(
                self.window,
                "缺少輸出位置",
                "請指定輸出影片的位置。",
            )
            return

        output_path = Path(output_text)

        if input_path.resolve() == output_path.resolve():
            QMessageBox.warning(
                self.window,
                "輸出位置錯誤",
                "輸入影片與輸出影片不能是同一個檔案。",
            )
            return

        try:
            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
        except OSError as error:
            QMessageBox.critical(
                self.window,
                "無法建立輸出目錄",
                str(error),
            )
            return

        detector = self.window.detector_combo.currentText()

        if detector != "SCRFD":
            QMessageBox.warning(
                self.window,
                "尚未支援",
                "目前 GUI 版本只支援 SCRFD 偵測器。",
            )
            return

        temp_output = output_path.with_name(
            f"{output_path.stem}_video_only.mp4"
        )

        config = GuiConfig(
            {
                "video.input": str(input_path),
                "video.temp_output": str(temp_output),
                "video.output": str(output_path),

                # SCRFD 模型會繼續從原有設定取得其他參數。
                # 若 ModelManager 需要更多設定，下一步再整合
                # 原本的 config.yaml。
            }
        )

        self.start_worker(config)

    def start_worker(self, config):
        """建立背景執行緒與 Worker。"""

        self.thread = QThread()
        self.worker = Worker(config)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.progress.connect(
            self.window.progress.setValue
        )

        self.worker.status_changed.connect(
            self.window.status_label.setText
        )

        self.worker.finished.connect(
            self.processing_finished
        )

        self.worker.cancelled.connect(
            self.processing_cancelled
        )

        self.worker.failed.connect(
            self.processing_failed
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.cancelled.connect(
            self.thread.quit
        )

        self.worker.failed.connect(
            self.thread.quit
        )

        self.thread.finished.connect(
            self.cleanup_worker
        )

        self.set_processing_state(True)

        self.window.progress.setValue(0)
        self.window.status_label.setText("正在準備影片處理……")

        self.thread.start()

    def stop_processing(self):
        """要求背景工作停止。"""

        if self.worker is None:
            return

        self.window.stop_button.setEnabled(False)
        self.window.status_label.setText("正在停止處理……")

        self.worker.request_stop()

    def processing_finished(self, output_path):
        """影片處理完成。"""

        self.window.progress.setValue(100)
        self.window.status_label.setText("影片處理完成")

        QMessageBox.information(
            self.window,
            "處理完成",
            f"影片已輸出至：\n{output_path}",
        )

    def processing_cancelled(self):
        """影片處理被使用者中止。"""

        self.window.progress.setValue(0)
        self.window.status_label.setText("影片處理已停止")

        QMessageBox.information(
            self.window,
            "處理已停止",
            "影片處理工作已停止，暫存檔案已清除。",
        )

    def processing_failed(self, message):
        """影片處理發生錯誤。"""

        self.window.progress.setValue(0)
        self.window.status_label.setText("影片處理失敗")

        QMessageBox.critical(
            self.window,
            "影片處理失敗",
            message,
        )

    def cleanup_worker(self):
        """背景執行緒結束後清理物件。"""

        if self.worker is not None:
            self.worker.deleteLater()

        if self.thread is not None:
            self.thread.deleteLater()

        self.worker = None
        self.thread = None

        self.set_processing_state(False)

    def set_processing_state(self, processing):
        """切換處理期間的按鈕及輸入欄位狀態。"""

        self.window.start_button.setEnabled(
            not processing
        )

        self.window.stop_button.setEnabled(
            processing
        )

        self.window.input_button.setEnabled(
            not processing
        )

        self.window.output_button.setEnabled(
            not processing
        )

        self.window.input_edit.setEnabled(
            not processing
        )

        self.window.output_edit.setEnabled(
            not processing
        )

        self.window.detector_combo.setEnabled(
            not processing
        )

        self.window.tracker_combo.setEnabled(
            not processing
        )

        self.window.renderer_combo.setEnabled(
            not processing
        )