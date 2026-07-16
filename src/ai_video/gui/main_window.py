from pathlib import Path
from ai_video import __version__

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """AI-Video 主視窗。"""

    video_dropped = Signal(str)
    open_video_requested = Signal()
    preferences_requested = Signal()

    SUPPORTED_VIDEO_SUFFIXES = {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".m4v",
    }

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"AI-Video {__version__}")
        self.resize(900, 650)
        self.setAcceptDrops(True)

        self.setup_ui()
        self.setup_menu()

    def setup_ui(self):
        """建立主視窗介面。"""

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel(
            "AI-Video 影片隱私保護處理"
        )
        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
        )
        layout.addWidget(title)

        # 輸入影片
        input_row = QHBoxLayout()

        input_label = QLabel("輸入影片")
        input_label.setFixedWidth(80)

        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText(
            "請選擇影片，或直接拖曳影片到視窗"
        )

        self.input_button = QPushButton("瀏覽")

        input_row.addWidget(input_label)
        input_row.addWidget(self.input_edit)
        input_row.addWidget(self.input_button)

        layout.addLayout(input_row)

        # 輸出影片
        output_row = QHBoxLayout()

        output_label = QLabel("輸出影片")
        output_label.setFixedWidth(80)

        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText(
            "請指定輸出影片的位置"
        )

        self.output_button = QPushButton("瀏覽")

        output_row.addWidget(output_label)
        output_row.addWidget(self.output_edit)
        output_row.addWidget(self.output_button)

        layout.addLayout(output_row)

        # 處理設定
        settings_title = QLabel("處理設定")
        settings_title.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            """
        )
        layout.addWidget(settings_title)

        settings_row = QHBoxLayout()

        detector_label = QLabel("偵測器")
        detector_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.detector_combo = QComboBox()
        self.detector_combo.addItem(
            "SCRFD（推薦）",
            "scrfd",
        )
        self.detector_combo.setMinimumWidth(150)

        tracker_label = QLabel("追蹤器")
        tracker_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.tracker_combo = QComboBox()
        self.tracker_combo.addItem(
            "AI 追蹤器",
            "bytetrack",
        )
        self.tracker_combo.setMinimumWidth(150)

        renderer_label = QLabel("處理方式")
        renderer_label.setStyleSheet(
            "font-weight: bold;"
        )

        self.renderer_combo = QComboBox()
        self.renderer_combo.addItem(
            "模糊",
            "blur",
        )
        self.renderer_combo.addItem(
            "馬賽克",
            "pixelate",
        )
        self.renderer_combo.setMinimumWidth(120)

        settings_row.addWidget(detector_label)
        settings_row.addWidget(self.detector_combo)

        settings_row.addSpacing(24)

        settings_row.addWidget(tracker_label)
        settings_row.addWidget(self.tracker_combo)

        settings_row.addSpacing(24)

        settings_row.addWidget(renderer_label)
        settings_row.addWidget(self.renderer_combo)

        settings_row.addStretch()

        layout.addLayout(settings_row)

        # 處理進度
        progress_title = QLabel("處理進度")
        progress_title.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            """
        )
        layout.addWidget(progress_title)

        self.status_label = QLabel("準備就緒")
        self.status_label.setStyleSheet(
            "font-size: 14px;"
        )
        layout.addWidget(self.status_label)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)

        layout.addWidget(self.progress)

        # 即時處理資訊
        stats_row = QHBoxLayout()

        frame_title = QLabel("影格")
        frame_title.setStyleSheet(
            "font-weight: bold;"
        )

        self.frame_value_label = QLabel("0 / 0")
        self.frame_value_label.setMinimumWidth(140)

        fps_title = QLabel("處理速度")
        fps_title.setStyleSheet(
            "font-weight: bold;"
        )

        self.fps_value_label = QLabel("0.00 FPS")
        self.fps_value_label.setMinimumWidth(120)

        faces_title = QLabel("人臉")
        faces_title.setStyleSheet(
            "font-weight: bold;"
        )

        self.faces_value_label = QLabel("0")
        self.faces_value_label.setMinimumWidth(50)

        eta_title = QLabel("剩餘時間")
        eta_title.setStyleSheet(
            "font-weight: bold;"
        )

        self.eta_value_label = QLabel("--:--:--")
        self.eta_value_label.setMinimumWidth(90)

        stats_row.addWidget(frame_title)
        stats_row.addWidget(self.frame_value_label)

        stats_row.addSpacing(24)

        stats_row.addWidget(fps_title)
        stats_row.addWidget(self.fps_value_label)

        stats_row.addSpacing(24)

        stats_row.addWidget(faces_title)
        stats_row.addWidget(self.faces_value_label)

        stats_row.addSpacing(24)

        stats_row.addWidget(eta_title)
        stats_row.addWidget(self.eta_value_label)

        stats_row.addStretch()

        layout.addLayout(stats_row)

        # 執行紀錄
        log_label = QLabel("執行紀錄")
        log_label.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            """
        )
        layout.addWidget(log_label)

        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setPlaceholderText(
            "影片處理訊息會顯示在這裡"
        )
        self.log_edit.setMinimumHeight(110)
        self.log_edit.setMaximumHeight(160)

        layout.addWidget(self.log_edit)

        layout.addStretch()

        # 操作按鈕
        button_row = QHBoxLayout()
        button_row.addStretch()

        self.start_button = QPushButton("開始處理")
        self.start_button.setMinimumWidth(120)

        self.stop_button = QPushButton("停止")
        self.stop_button.setMinimumWidth(120)
        self.stop_button.setEnabled(False)

        button_row.addWidget(self.start_button)
        button_row.addWidget(self.stop_button)

        layout.addLayout(button_row)

    def setup_menu(self):
        """建立應用程式選單列。"""

        file_menu = self.menuBar().addMenu("檔案")

        open_action = QAction(
            "開啟影片…",
            self,
        )
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(
            self.open_video_requested.emit
        )

        preferences_action = QAction(
            "偏好設定…",
            self,
        )
        preferences_action.setShortcut("Ctrl+,")
        preferences_action.triggered.connect(
            self.preferences_requested.emit
        )

        quit_action = QAction(
            "結束",
            self,
        )
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(
            self.close
        )

        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(preferences_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

    def append_log(self, message: str):
        """在 GUI 執行紀錄中加入訊息。"""

        self.log_edit.append(message)

        scrollbar = self.log_edit.verticalScrollBar()
        scrollbar.setValue(
            scrollbar.maximum()
        )

    def update_processing_stats(self, stats):
        """更新影片處理即時資訊。"""

        self.frame_value_label.setText(
            f"{stats.frame_index:,} / "
            f"{stats.total_frames:,}"
        )

        self.fps_value_label.setText(
            f"{stats.fps:.2f} FPS"
        )

        self.faces_value_label.setText(
            str(stats.faces)
        )

        self.eta_value_label.setText(
            self.format_duration(
                stats.eta_seconds
            )
        )

    def reset_processing_stats(self):
        """清除上一支影片的處理資訊。"""

        self.frame_value_label.setText("0 / 0")
        self.fps_value_label.setText("0.00 FPS")
        self.faces_value_label.setText("0")
        self.eta_value_label.setText("--:--:--")

    @staticmethod
    def format_duration(
        seconds: float,
    ) -> str:
        """將秒數格式化為 HH:MM:SS。"""

        total_seconds = max(
            0,
            int(seconds),
        )

        hours, remainder = divmod(
            total_seconds,
            3600,
        )

        minutes, seconds = divmod(
            remainder,
            60,
        )

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    def dragEnterEvent(self, event):
        """判斷拖入的檔案是否為支援的影片。"""

        mime_data = event.mimeData()

        if not mime_data.hasUrls():
            event.ignore()
            return

        urls = mime_data.urls()

        if not urls:
            event.ignore()
            return

        path = Path(
            urls[0].toLocalFile()
        )

        if (
            path.is_file()
            and path.suffix.lower()
            in self.SUPPORTED_VIDEO_SUFFIXES
        ):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """處理放入視窗的影片檔案。"""

        urls = event.mimeData().urls()

        if not urls:
            event.ignore()
            return

        path = Path(
            urls[0].toLocalFile()
        )

        if (
            not path.is_file()
            or path.suffix.lower()
            not in self.SUPPORTED_VIDEO_SUFFIXES
        ):
            event.ignore()
            return

        self.video_dropped.emit(
            str(path)
        )

        event.acceptProposedAction()