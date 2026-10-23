import cv2

from ai_video.renderer.base_renderer import BaseRenderer


class PixelateRenderer(BaseRenderer):
    """使用馬賽克效果保護指定區域。"""

    def __init__(
        self,
        pixel_size=12,
    ):
        # 加上型態防護：如果傳入的不是數字或字串（例如不小心帶入 ConfigManager 物件），則安全預設為 12
        if not isinstance(pixel_size, (int, float, str)):
            pixel_size = 12

        try:
            parsed_size = int(pixel_size)
        except (TypeError, ValueError):
            parsed_size = 12

        self.pixel_size = max(
            2,
            parsed_size,
        )

    def render(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        """對指定矩形區域套用馬賽克。"""

        roi = self.extract_roi(
            frame,
            box,
        )

        if roi is None:
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