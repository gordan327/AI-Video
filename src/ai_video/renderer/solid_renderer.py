from ai_video.renderer.base_renderer import BaseRenderer


class SolidRenderer(BaseRenderer):
    """以純黑色填滿指定區域。"""

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