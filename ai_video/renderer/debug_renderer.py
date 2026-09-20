from __future__ import annotations

import cv2

from ai_video.renderer.base_renderer import BaseRenderer


class DebugRenderer(BaseRenderer):
    """以矩形外框標示指定區域，供偵錯與視覺驗證使用。"""

    def __init__(
        self,
        line_thickness: int = 2,
    ):
        if line_thickness <= 0:
            raise ValueError(
                "line_thickness must be greater than zero."
            )

        self.line_thickness = line_thickness

    def render(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        """在指定矩形區域周圍繪製偵錯外框。"""

        if frame is None:
            raise ValueError(
                "frame must not be None."
            )

        frame_height, frame_width = frame.shape[:2]

        x1, y1, x2, y2 = box

        x1 = max(
            0,
            min(frame_width - 1, int(x1)),
        )

        y1 = max(
            0,
            min(frame_height - 1, int(y1)),
        )

        x2 = max(
            0,
            min(frame_width - 1, int(x2)),
        )

        y2 = max(
            0,
            min(frame_height - 1, int(y2)),
        )

        if x2 <= x1 or y2 <= y1:
            return frame

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            self.line_thickness,
        )

        return frame