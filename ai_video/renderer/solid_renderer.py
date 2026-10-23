from ai_video.renderer.base_renderer import BaseRenderer


class SolidRenderer(BaseRenderer):
    """以純黑色填滿指定區域。"""

    def __init__(self, *args, **kwargs):
        """使用 *args 與 **kwargs 接收所有傳入參數，避免發生引數過多錯誤。"""
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