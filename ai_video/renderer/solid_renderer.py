from ai_video.renderer.base_renderer import BaseRenderer


class SolidRenderer(BaseRenderer):
    """以純黑色填滿指定區域。"""

    def __init__(self, **kwargs):
        """使用 **kwargs 接收所有初始參數，避免發生 takes no arguments 錯誤。"""
        super().__init__()

    def render(
        self,
        frame,
        box,
    ):
        roi = self.extract_roi(
            frame,
            box,
        )

        if roi is None:
            return

        roi[:] = 0