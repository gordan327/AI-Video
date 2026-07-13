import cv2

from ai_video.renderer.base_renderer import BaseRenderer


class PixelateRenderer(BaseRenderer):
    """使用馬賽克效果保護指定區域。"""

    def __init__(
        self,
        pixel_size: int = 12,
    ):
        self.pixel_size = max(
            2,
            int(pixel_size),
        )

    def render(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        """對指定矩形區域套用馬賽克。"""

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
            return

        roi = frame[
            y1:y2,
            x1:x2,
        ]

        if roi.size == 0:
            return

        region_height, region_width = roi.shape[:2]

        small_width = max(
            1,
            region_width // self.pixel_size,
        )

        small_height = max(
            1,
            region_height // self.pixel_size,
        )

        reduced = cv2.resize(
            roi,
            (
                small_width,
                small_height,
            ),
            interpolation=cv2.INTER_LINEAR,
        )

        pixelated = cv2.resize(
            reduced,
            (
                region_width,
                region_height,
            ),
            interpolation=cv2.INTER_NEAREST,
        )

        roi[:] = pixelated