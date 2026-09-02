from ai_video.renderer.base_renderer import BaseRenderer
from ai_video.renderer.blur_renderer import BlurRenderer
from ai_video.renderer.debug_renderer import DebugRenderer
from ai_video.renderer.pixelate_renderer import PixelateRenderer
from ai_video.renderer.solid_renderer import SolidRenderer


_RENDERERS = {
    "blur": BlurRenderer,
    "pixelate": PixelateRenderer,
    "solid": SolidRenderer,
    "debug": DebugRenderer,
}


class RendererFactory:
    """建立 Renderer。"""

    @staticmethod
    def create(
        renderer_type: str,
        **kwargs,
    ) -> BaseRenderer:

        renderer_type = renderer_type.lower()

        renderer_class = _RENDERERS.get(
            renderer_type
        )

        if renderer_class is None:
            raise ValueError(
                f"未知 Renderer：{renderer_type}"
            )

        if renderer_type == "blur":
            return renderer_class(
                blur_strength=kwargs.get(
                    "blur_strength",
                    51,
                ),
            )

        if renderer_type == "pixelate":
            return renderer_class(
                pixel_size=kwargs.get(
                    "pixel_size",
                    12,
                ),
            )

        if renderer_type == "solid":
            return renderer_class()

        if renderer_type == "debug":
            return renderer_class(
                line_thickness=kwargs.get(
                    "line_thickness",
                    2,
                ),
            )

        raise ValueError(
            f"未知 Renderer：{renderer_type}"
        )