from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ProcessingQueueStatus(Enum):
    """影片在處理佇列中的狀態。"""

    WAITING = "waiting"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class ProcessingQueueItem:
    """描述批次處理佇列中的一支影片。"""

    input_path: Path
    output_path: Path
    status: ProcessingQueueStatus = (
        ProcessingQueueStatus.WAITING
    )
    error_message: str | None = None


class ProcessingQueue:
    """管理批次影片處理佇列。"""

    def __init__(self):
        self._items: list[ProcessingQueueItem] = []

    @property
    def items(self) -> tuple[ProcessingQueueItem, ...]:
        """依照加入順序傳回所有項目。"""

        return tuple(self._items)

    def add(
        self,
        input_path: Path,
        output_path: Path,
    ) -> ProcessingQueueItem | None:
        """加入影片；若輸入影片已存在則不重複加入。"""

        normalized_input = input_path.resolve()

        if any(
            item.input_path.resolve() == normalized_input
            for item in self._items
        ):
            return None

        item = ProcessingQueueItem(
            input_path=input_path,
            output_path=output_path,
        )

        self._items.append(item)

        return item

    def next_waiting(
        self,
    ) -> ProcessingQueueItem | None:
        """取得下一支等待影片並標記為處理中。"""

        for item in self._items:
            if (
                item.status
                is ProcessingQueueStatus.WAITING
            ):
                item.status = (
                    ProcessingQueueStatus.PROCESSING
                )
                return item

        return None

    def mark_completed(
        self,
        item: ProcessingQueueItem,
    ) -> bool:
        """將處理中的項目標記為完成。"""

        if (
            item not in self._items
            or item.status
            is not ProcessingQueueStatus.PROCESSING
        ):
            return False

        item.status = ProcessingQueueStatus.COMPLETED
        item.error_message = None

        return True

    def mark_failed(
        self,
        item: ProcessingQueueItem,
        error_message: str,
    ) -> bool:
        """將處理中的項目標記為失敗並記錄原因。"""

        if (
            item not in self._items
            or item.status
            is not ProcessingQueueStatus.PROCESSING
        ):
            return False

        item.status = ProcessingQueueStatus.FAILED
        item.error_message = error_message

        return True

    def cancel(
        self,
        item: ProcessingQueueItem,
    ) -> bool:
        """取消仍在等待中的項目。"""

        if (
            item not in self._items
            or item.status
            is not ProcessingQueueStatus.WAITING
        ):
            return False

        item.status = ProcessingQueueStatus.CANCELLED
        item.error_message = None

        return True

    def requeue(
        self,
        item: ProcessingQueueItem,
    ) -> bool:
        """將失敗或已取消的項目重新排入等待佇列。"""

        if (
            item not in self._items
            or item.status
            not in {
                ProcessingQueueStatus.FAILED,
                ProcessingQueueStatus.CANCELLED,
            }
        ):
            return False

        item.status = ProcessingQueueStatus.WAITING
        item.error_message = None

        return True

    def remove(
        self,
        item: ProcessingQueueItem,
    ) -> bool:
        """移除等待中的項目。"""

        if (
            item not in self._items
            or item.status
            is not ProcessingQueueStatus.WAITING
        ):
            return False

        self._items.remove(item)

        return True