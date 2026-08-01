from pathlib import Path
from types import SimpleNamespace

from ai_video.gui.controller import Controller


class FakeWidget:
    def __init__(self):
        self.value = None
        self.text = None

    def setValue(self, value):
        self.value = value

    def setText(self, text):
        self.text = text


class FakeQueueList:
    def __init__(self):
        self.widgets = [FakeWidget()]

    def item(self, index):
        return self.widgets[index]


class FakeProcessingQueue:
    def __init__(self, item):
        self.items = [item]
        self.completed_item = None
        self.cancelled_item = None
        self.failed_item = None
        self.failure_message = None

    def mark_completed(self, item):
        self.completed_item = item
        return True

    def mark_cancelled(self, item):
        self.cancelled_item = item
        return True

    def mark_failed(self, item, message):
        self.failed_item = item
        self.failure_message = message
        return True


def test_processing_finished_marks_queue_item_completed(
    monkeypatch,
):
    controller = Controller.__new__(Controller)

    queue_item = SimpleNamespace(
        input_path=Path("demo.mp4"),
    )

    controller.window = SimpleNamespace(
        progress=FakeWidget(),
        status_label=FakeWidget(),
        queue_list=FakeQueueList(),
    )
    controller.processing_queue = FakeProcessingQueue(
        queue_item
    )
    controller.current_queue_item = queue_item
    controller.continue_queue_after_cleanup = False

    controller.add_log = lambda *args, **kwargs: None
    controller.log_processing_session_end = (
        lambda *args, **kwargs: None
    )

    information_calls = []

    monkeypatch.setattr(
        "ai_video.gui.controller.QMessageBox.information",
        lambda *args, **kwargs: information_calls.append(
            (args, kwargs)
        ),
    )

    controller.processing_finished(
        "/tmp/demo_blurred.mp4"
    )

    assert controller.window.progress.value == 100
    assert (
        controller.window.status_label.text
        == "影片處理完成"
    )
    assert (
        controller.processing_queue.completed_item
        is queue_item
    )
    assert (
        controller.window.queue_list.widgets[0].text
        == "已完成｜demo.mp4"
    )
    assert (
        controller.continue_queue_after_cleanup
        is True
    )
    assert information_calls == []

def test_processing_cancelled_marks_queue_item_cancelled(
    monkeypatch,
):
    controller = Controller.__new__(Controller)

    queue_item = SimpleNamespace(
        input_path=Path("demo.mp4"),
    )

    controller.window = SimpleNamespace(
        progress=FakeWidget(),
        status_label=FakeWidget(),
        queue_list=FakeQueueList(),
    )
    controller.processing_queue = FakeProcessingQueue(
        queue_item
    )
    controller.current_queue_item = queue_item
    controller.continue_queue_after_cleanup = True

    controller.add_log = lambda *args, **kwargs: None
    controller.log_processing_session_end = (
        lambda *args, **kwargs: None
    )

    information_calls = []

    monkeypatch.setattr(
        "ai_video.gui.controller.QMessageBox.information",
        lambda *args, **kwargs: information_calls.append(
            (args, kwargs)
        ),
    )

    controller.processing_cancelled()

    assert controller.window.progress.value == 0
    assert (
        controller.window.status_label.text
        == "影片處理已停止"
    )
    assert (
        controller.processing_queue.cancelled_item
        is queue_item
    )
    assert (
        controller.window.queue_list.widgets[0].text
        == "已停止｜demo.mp4"
    )
    assert (
        controller.continue_queue_after_cleanup
        is False
    )
    assert len(information_calls) == 1

def test_processing_failed_marks_queue_item_failed(
    monkeypatch,
):
    controller = Controller.__new__(Controller)

    queue_item = SimpleNamespace(
        input_path=Path("broken.mp4"),
    )

    controller.window = SimpleNamespace(
        progress=FakeWidget(),
        status_label=FakeWidget(),
        queue_list=FakeQueueList(),
    )
    controller.processing_queue = FakeProcessingQueue(
        queue_item
    )
    controller.current_queue_item = queue_item
    controller.continue_queue_after_cleanup = False

    controller.add_log = lambda *args, **kwargs: None
    controller.log_processing_session_end = (
        lambda *args, **kwargs: None
    )

    critical_calls = []

    monkeypatch.setattr(
        "ai_video.gui.controller.QMessageBox.critical",
        lambda *args, **kwargs: critical_calls.append(
            (args, kwargs)
        ),
    )

    error_message = "Unable to open input video."

    controller.processing_failed(error_message)

    assert controller.window.progress.value == 0
    assert (
        controller.window.status_label.text
        == "影片處理失敗"
    )
    assert (
        controller.processing_queue.failed_item
        is queue_item
    )
    assert (
        controller.processing_queue.failure_message
        == error_message
    )
    assert (
        controller.window.queue_list.widgets[0].text
        == "處理失敗｜broken.mp4"
    )
    assert (
        controller.continue_queue_after_cleanup
        is True
    )
    assert len(critical_calls) == 1

    displayed_message = critical_calls[0][0][2]

    assert "broken.mp4" in displayed_message
    assert "詳細資訊已保留在執行紀錄中" in displayed_message
    assert error_message not in displayed_message

from ai_video.gui.processing_queue import (
    ProcessingQueueStatus,
)


def test_cleanup_worker_continues_with_waiting_item(
    monkeypatch,
):
    controller = Controller.__new__(Controller)

    waiting_item = SimpleNamespace(
        status=ProcessingQueueStatus.WAITING,
    )

    controller.worker = None
    controller.thread = None
    controller.processing_queue = SimpleNamespace(
        items=[waiting_item],
    )
    controller.current_queue_item = SimpleNamespace()
    controller.continue_queue_after_cleanup = True
    controller.set_processing_state = (
        lambda processing: None
    )

    start_calls = []
    controller.start_processing = (
        lambda: start_calls.append(True)
    )

    monkeypatch.setattr(
        "ai_video.gui.controller.QTimer.singleShot",
        lambda delay, callback: callback(),
    )

    controller.cleanup_worker()

    assert controller.worker is None
    assert controller.thread is None
    assert controller.current_queue_item is None
    assert (
        controller.continue_queue_after_cleanup
        is False
    )
    assert start_calls == [True]

def test_cleanup_worker_shows_queue_summary(
    monkeypatch,
):
    controller = Controller.__new__(Controller)

    completed_item = SimpleNamespace(
        status=ProcessingQueueStatus.COMPLETED,
    )
    failed_item = SimpleNamespace(
        status=ProcessingQueueStatus.FAILED,
    )

    controller.worker = None
    controller.thread = None
    controller.window = SimpleNamespace()
    controller.processing_queue = SimpleNamespace(
        items=[completed_item, failed_item],
    )
    controller.current_queue_item = SimpleNamespace()
    controller.continue_queue_after_cleanup = True
    controller.set_processing_state = (
        lambda processing: None
    )

    information_calls = []

    monkeypatch.setattr(
        "ai_video.gui.controller.QMessageBox.information",
        lambda *args, **kwargs: information_calls.append(
            (args, kwargs)
        ),
    )

    controller.cleanup_worker()

    assert controller.current_queue_item is None
    assert (
        controller.continue_queue_after_cleanup
        is False
    )
    assert len(information_calls) == 1

    title = information_calls[0][0][1]
    displayed_message = information_calls[0][0][2]

    assert title == "佇列處理結束"
    assert "完成：1 支" in displayed_message
    assert "失敗：1 支" in displayed_message