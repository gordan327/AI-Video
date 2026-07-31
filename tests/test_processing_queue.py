from pathlib import Path

from ai_video.gui.processing_queue import (
    ProcessingQueue,
    ProcessingQueueItem,
    ProcessingQueueStatus,
)


def test_processing_queue_item_starts_waiting():
    item = ProcessingQueueItem(
        input_path=Path("/videos/input.mp4"),
        output_path=Path("/exports/output.mp4"),
    )

    assert item.input_path == Path(
        "/videos/input.mp4"
    )
    assert item.output_path == Path(
        "/exports/output.mp4"
    )
    assert (
        item.status
        is ProcessingQueueStatus.WAITING
    )
    assert item.error_message is None


def test_processing_queue_item_status_can_change():
    item = ProcessingQueueItem(
        input_path=Path("/videos/input.mp4"),
        output_path=Path("/exports/output.mp4"),
    )

    item.status = ProcessingQueueStatus.PROCESSING

    assert (
        item.status
        is ProcessingQueueStatus.PROCESSING
    )


def test_processing_queue_item_records_failure():
    item = ProcessingQueueItem(
        input_path=Path("/videos/input.mp4"),
        output_path=Path("/exports/output.mp4"),
    )

    item.status = ProcessingQueueStatus.FAILED
    item.error_message = "無法讀取影片"

    assert (
        item.status
        is ProcessingQueueStatus.FAILED
    )
    assert item.error_message == "無法讀取影片"


def test_processing_queue_adds_items_in_order():
    queue = ProcessingQueue()

    first = queue.add(
        Path("/videos/first.mp4"),
        Path("/exports/first.mp4"),
    )
    second = queue.add(
        Path("/videos/second.mp4"),
        Path("/exports/second.mp4"),
    )

    assert first is not None
    assert second is not None
    assert queue.items == (
        first,
        second,
    )


def test_processing_queue_rejects_duplicate_input():
    queue = ProcessingQueue()

    first = queue.add(
        Path("/videos/input.mp4"),
        Path("/exports/input.mp4"),
    )
    duplicate = queue.add(
        Path("/videos/input.mp4"),
        Path("/exports/another-output.mp4"),
    )

    assert first is not None
    assert duplicate is None
    assert queue.items == (first,)


def test_processing_queue_returns_next_waiting_item():
    queue = ProcessingQueue()

    first = queue.add(
        Path("/videos/first.mp4"),
        Path("/exports/first.mp4"),
    )
    second = queue.add(
        Path("/videos/second.mp4"),
        Path("/exports/second.mp4"),
    )

    assert first is not None
    assert second is not None

    first.status = ProcessingQueueStatus.COMPLETED

    assert queue.next_waiting() is second


def test_processing_queue_returns_none_when_empty():
    queue = ProcessingQueue()

    assert queue.next_waiting() is None


def test_processing_queue_marks_next_item_processing():
    queue = ProcessingQueue()

    item = queue.add(
        Path("/videos/input.mp4"),
        Path("/exports/input.mp4"),
    )

    assert item is not None
    assert (
        item.status
        is ProcessingQueueStatus.WAITING
    )

    selected = queue.next_waiting()

    assert selected is item
    assert (
        item.status
        is ProcessingQueueStatus.PROCESSING
    )


def test_processing_queue_skips_processing_item():
    queue = ProcessingQueue()

    first = queue.add(
        Path("/videos/first.mp4"),
        Path("/exports/first.mp4"),
    )
    second = queue.add(
        Path("/videos/second.mp4"),
        Path("/exports/second.mp4"),
    )

    assert first is not None
    assert second is not None

    assert queue.next_waiting() is first
    assert queue.next_waiting() is second
    assert (
        first.status
        is ProcessingQueueStatus.PROCESSING
    )
    assert (
        second.status
        is ProcessingQueueStatus.PROCESSING
    )


def test_processing_queue_removes_waiting_item():
    queue = ProcessingQueue()

    first = queue.add(
        Path("/videos/first.mp4"),
        Path("/exports/first.mp4"),
    )
    second = queue.add(
        Path("/videos/second.mp4"),
        Path("/exports/second.mp4"),
    )

    assert first is not None
    assert second is not None
    assert queue.remove(first) is True
    assert queue.items == (second,)


def test_processing_queue_does_not_remove_processed_item():
    queue = ProcessingQueue()

    item = queue.add(
        Path("/videos/input.mp4"),
        Path("/exports/input.mp4"),
    )

    assert item is not None

    item.status = ProcessingQueueStatus.COMPLETED

    assert queue.remove(item) is False
    assert queue.items == (item,)