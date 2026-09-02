from ai_video.gui.processing_state_manager import (
    ProcessingStateManager,
)


class FakeWidget:
    def __init__(self):
        self.enabled = None

    def setEnabled(self, enabled):
        self.enabled = enabled


class FakeWindow:
    def __init__(self):
        self.start_button = FakeWidget()
        self.stop_button = FakeWidget()
        self.input_button = FakeWidget()
        self.output_button = FakeWidget()
        self.input_edit = FakeWidget()
        self.output_edit = FakeWidget()
        self.detector_combo = FakeWidget()
        self.tracker_combo = FakeWidget()
        self.renderer_combo = FakeWidget()
        self.quit_button = FakeWidget()


def test_apply_processing_state():
    window = FakeWindow()

    ProcessingStateManager.apply(
        window=window,
        processing=True,
    )

    assert window.start_button.enabled is False
    assert window.stop_button.enabled is True
    assert window.input_button.enabled is False
    assert window.output_button.enabled is False
    assert window.input_edit.enabled is False
    assert window.output_edit.enabled is False
    assert window.detector_combo.enabled is False
    assert window.tracker_combo.enabled is False
    assert window.renderer_combo.enabled is False
    assert window.quit_button.enabled is False


def test_apply_idle_state():
    window = FakeWindow()

    ProcessingStateManager.apply(
        window=window,
        processing=False,
    )

    assert window.start_button.enabled is True
    assert window.stop_button.enabled is False
    assert window.input_button.enabled is True
    assert window.output_button.enabled is True
    assert window.input_edit.enabled is True
    assert window.output_edit.enabled is True
    assert window.detector_combo.enabled is True
    assert window.tracker_combo.enabled is True
    assert window.renderer_combo.enabled is True
    assert window.quit_button.enabled is True