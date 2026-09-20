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
        roi = self.extract_roi(
            frame,
            box,
        )

        if roi is None:
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