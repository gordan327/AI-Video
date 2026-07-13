from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class PreferencesDialog(QDialog):
    """AI-Video 偏好設定視窗。"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("AI-Video 偏好設定")
        self.setModal(True)
        self.resize(520, 420)

        self.setup_ui()

    def setup_ui(self):
        """建立偏好設定介面。"""

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(18)

        title = QLabel("偏好設定")
        title.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            """
        )
        main_layout.addWidget(title)

        description = QLabel(
            "調整人臉偵測、影片處理與執行環境設定。"
        )
        description.setWordWrap(True)
        main_layout.addWidget(description)

        # 人臉偵測設定
        detector_group = QGroupBox("人臉偵測")
        detector_form = QFormLayout(detector_group)

        self.model_combo = QComboBox()
        self.model_combo.addItems(
            [
                "buffalo_sc",
            ]
        )

        self.det_size_spin = QSpinBox()
        self.det_size_spin.setRange(160, 1280)
        self.det_size_spin.setSingleStep(32)
        self.det_size_spin.setValue(640)
        self.det_size_spin.setSuffix(" px")

        self.confidence_spin = QDoubleSpinBox()
        self.confidence_spin.setRange(0.01, 1.00)
        self.confidence_spin.setSingleStep(0.05)
        self.confidence_spin.setDecimals(2)
        self.confidence_spin.setValue(0.50)

        detector_form.addRow(
            "模型",
            self.model_combo,
        )
        detector_form.addRow(
            "偵測尺寸",
            self.det_size_spin,
        )
        detector_form.addRow(
            "信心門檻",
            self.confidence_spin,
        )

        main_layout.addWidget(detector_group)

        # 隱私保護設定
        privacy_group = QGroupBox("隱私保護")
        privacy_form = QFormLayout(privacy_group)

        self.privacy_hold_spin = QSpinBox()
        self.privacy_hold_spin.setRange(0, 60)
        self.privacy_hold_spin.setValue(15)
        self.privacy_hold_spin.setSuffix(" 幀")

        self.prediction_frames_spin = QSpinBox()
        self.prediction_frames_spin.setRange(0, 15)
        self.prediction_frames_spin.setValue(3)
        self.prediction_frames_spin.setSuffix(" 幀")

        self.temporal_hold_spin = QSpinBox()
        self.temporal_hold_spin.setRange(0, 30)
        self.temporal_hold_spin.setValue(5)
        self.temporal_hold_spin.setSuffix(" 幀")

        self.padding_ratio_spin = QDoubleSpinBox()
        self.padding_ratio_spin.setRange(0.0, 1.5)
        self.padding_ratio_spin.setSingleStep(0.05)
        self.padding_ratio_spin.setDecimals(2)
        self.padding_ratio_spin.setValue(0.35)

        privacy_form.addRow(
            "追蹤保留",
            self.privacy_hold_spin,
        )
        privacy_form.addRow(
            "預測幀數",
            self.prediction_frames_spin,
        )
        privacy_form.addRow(
            "模糊保留",
            self.temporal_hold_spin,
        )
        privacy_form.addRow(
            "頭部擴張比例",
            self.padding_ratio_spin,
        )

        main_layout.addWidget(privacy_group)

        # 執行環境設定
        runtime_group = QGroupBox("執行環境")
        runtime_form = QFormLayout(runtime_group)

        self.provider_combo = QComboBox()
        self.provider_combo.addItem(
            "自動選擇",
            "auto",
        )
        self.provider_combo.addItem(
            "CPU",
            "CPUExecutionProvider",
        )

        runtime_form.addRow(
            "運算裝置",
            self.provider_combo,
        )

        main_layout.addWidget(runtime_group)

        # 顯示設定
        display_group = QGroupBox("顯示")
        display_form = QFormLayout(display_group)

        self.language_combo = QComboBox()
        self.language_combo.addItem(
            "繁體中文",
            "zh_TW",
        )

        display_form.addRow(
            "介面語言",
            self.language_combo,
        )

        main_layout.addWidget(display_group)

        main_layout.addStretch()

        # 確定與取消按鈕
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.button_box.button(
            QDialogButtonBox.StandardButton.Ok
        ).setText("儲存")

        self.button_box.button(
            QDialogButtonBox.StandardButton.Cancel
        ).setText("取消")

        self.button_box.accepted.connect(
            self.accept
        )
        self.button_box.rejected.connect(
            self.reject
        )

        main_layout.addWidget(self.button_box)

    def get_values(self) -> dict:
        """取得目前視窗中的設定值。"""

        return {
            "detector.model": (
                self.model_combo.currentText()
            ),
            "detector.det_size": (
                self.det_size_spin.value()
            ),
            "detector.confidence": (
                self.confidence_spin.value()
            ),
            "runtime.provider": (
                self.provider_combo.currentData()
            ),
            "ui.language": (
                self.language_combo.currentData()
            ),
            "tracker.privacy_hold_frames": (
                self.privacy_hold_spin.value()
            ),
            "tracker.prediction_frames": (
                self.prediction_frames_spin.value()
            ),
            "renderer.temporal_hold_frames": (
                self.temporal_hold_spin.value()
            ),
            "renderer.padding_ratio": (
                self.padding_ratio_spin.value()
            ),
        }

    def set_values(self, values: dict):
        """將既有設定載入視窗。"""

        model_name = values.get(
            "detector.model",
            "buffalo_sc",
        )

        model_index = self.model_combo.findText(
            model_name
        )

        if model_index >= 0:
            self.model_combo.setCurrentIndex(
                model_index
            )

        self.det_size_spin.setValue(
            int(
                values.get(
                    "detector.det_size",
                    640,
                )
            )
        )

        self.confidence_spin.setValue(
            float(
                values.get(
                    "detector.confidence",
                    0.50,
                )
            )
        )

        provider = values.get(
            "runtime.provider",
            "auto",
        )

        provider_index = (
            self.provider_combo.findData(
                provider
            )
        )

        if provider_index >= 0:
            self.provider_combo.setCurrentIndex(
                provider_index
            )

        self.privacy_hold_spin.setValue(
            int(
                values.get(
                    "tracker.privacy_hold_frames",
                    15,
                )
            )
        )

        self.prediction_frames_spin.setValue(
            int(
                values.get(
                    "tracker.prediction_frames",
                    3,
                )
            )
        )

        self.temporal_hold_spin.setValue(
            int(
                values.get(
                    "renderer.temporal_hold_frames",
                    5,
                )
            )
        )

        self.padding_ratio_spin.setValue(
            float(
                values.get(
                    "renderer.padding_ratio",
                    0.35,
                )
            )
        )