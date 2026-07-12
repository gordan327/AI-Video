from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """AI-Video 主視窗。"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI-Video 0.4 Alpha")
        self.resize(900, 500)

        self.setup_ui()

    def setup_ui(self):
        """建立主視窗介面。"""

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("AI-Video 影片人臉模糊處理")
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
        self.input_edit.setPlaceholderText("請選擇要處理的影片")

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
        self.output_edit.setPlaceholderText("請指定輸出影片的位置")

        self.output_button = QPushButton("瀏覽")

        output_row.addWidget(output_label)
        output_row.addWidget(self.output_edit)
        output_row.addWidget(self.output_button)

        layout.addLayout(output_row)

        # 偵測器
        detector_row = QHBoxLayout()

        detector_label = QLabel("偵測器")
        detector_label.setFixedWidth(80)

        self.detector_combo = QComboBox()
        self.detector_combo.addItems(
            [
                "SCRFD",
            ]
        )

        detector_row.addWidget(detector_label)
        detector_row.addWidget(self.detector_combo)
        detector_row.addStretch()

        layout.addLayout(detector_row)

        # 追蹤器
        tracker_row = QHBoxLayout()

        tracker_label = QLabel("追蹤器")
        tracker_label.setFixedWidth(80)

        self.tracker_combo = QComboBox()
        self.tracker_combo.addItems(
            [
                "AI-Tracker",
            ]
        )

        tracker_row.addWidget(tracker_label)
        tracker_row.addWidget(self.tracker_combo)
        tracker_row.addStretch()

        layout.addLayout(tracker_row)

        # 影像處理方式
        renderer_row = QHBoxLayout()

        renderer_label = QLabel("處理方式")
        renderer_label.setFixedWidth(80)

        self.renderer_combo = QComboBox()
        self.renderer_combo.addItems(
            [
                "Blur",
            ]
        )

        renderer_row.addWidget(renderer_label)
        renderer_row.addWidget(self.renderer_combo)
        renderer_row.addStretch()

        layout.addLayout(renderer_row)

        layout.addStretch()

        # 狀態
        self.status_label = QLabel("準備就緒")
        layout.addWidget(self.status_label)

        # 進度條
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        layout.addWidget(self.progress)

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