class ProcessingStateManager:
    """管理影片處理期間的 GUI 元件狀態。"""

    @staticmethod
    def apply(window, processing: bool) -> None:
        """依照處理狀態啟用或停用畫面元件。"""

        enabled_when_idle = not processing

        window.start_button.setEnabled(
            enabled_when_idle
        )

        window.stop_button.setEnabled(
            processing
        )

        window.input_button.setEnabled(
            enabled_when_idle
        )

        window.output_button.setEnabled(
            enabled_when_idle
        )

        window.input_edit.setEnabled(
            enabled_when_idle
        )

        window.output_edit.setEnabled(
            enabled_when_idle
        )

        window.detector_combo.setEnabled(
            enabled_when_idle
        )

        window.tracker_combo.setEnabled(
            enabled_when_idle
        )

        window.renderer_combo.setEnabled(
            enabled_when_idle
        )

        window.quit_button.setEnabled(
            enabled_when_idle
        )