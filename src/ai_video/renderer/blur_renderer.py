import cv2

from ai_video.renderer.base_renderer import BaseRenderer

class BlurRenderer(BaseRenderer):
    """負責 Gaussian Blur。"""

    def __init__(
        self,
        blur_strength: int,
    ):
        self.blur_strength = blur_strength

    @staticmethod
    def normalize_kernel_size(
        value: int,
    ) -> int:

        value = max(
            3,
            int(value),
        )

        if value % 2 == 0:
            value += 1

        return value

    def render(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        x1, y1, x2, y2 = box

        frame_height, frame_width = frame.shape[:2]

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

        kernel = min(
            self.blur_strength,
            roi.shape[0],
            roi.shape[1],
        )

        kernel = self.normalize_kernel_size(
            kernel
        )

        roi[:] = cv2.GaussianBlur(
            roi,
            (
                kernel,
                kernel,
            ),
            0,
        )