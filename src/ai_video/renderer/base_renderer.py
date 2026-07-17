from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    """所有隱私呈現方式的共同介面。"""

    @staticmethod
    def extract_roi(
        frame,
        box: tuple[int, int, int, int],
    ):
        """裁切並取得有效的影像區域。"""

        frame_height, frame_width = frame.shape[:2]

        x1, y1, x2, y2 = box

        x1 = max(
            0,
            min(frame_width, int(x1)),
        )

        y1 = max(
            0,
            min(frame_height, int(y1)),
        )

        x2 = max(
            0,
            min(frame_width, int(x2)),
        )

        y2 = max(
            0,
            min(frame_height, int(y2)),
        )

        if x2 <= x1 or y2 <= y1:
            return None

        roi = frame[
            y1:y2,
            x1:x2,
        ]

        if roi.size == 0:
            return None

        return roi

    @abstractmethod
    def render(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        """對指定矩形區域進行隱私處理。"""

        raise NotImplementedError