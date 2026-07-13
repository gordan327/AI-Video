import pytest

from ai_video.renderer.base_renderer import BaseRenderer
from ai_video.renderer.blur_renderer import BlurRenderer
from ai_video.renderer.renderer_factory import RendererFactory
from ai_video.renderer.pixelate_renderer import (
    PixelateRenderer,
)

def test_create_blur_renderer():
    renderer = RendererFactory.create(
        renderer_type="blur",
        blur_strength=51,
    )

    assert isinstance(
        renderer,
        BlurRenderer,
    )

    assert isinstance(
        renderer,
        BaseRenderer,
    )


def test_renderer_type_is_case_insensitive():
    renderer = RendererFactory.create(
        renderer_type="BLUR",
        blur_strength=51,
    )

    assert isinstance(
        renderer,
        BlurRenderer,
    )


def test_unknown_renderer_raises_error():
    with pytest.raises(
        ValueError,
        match="未知 Renderer",
    ):
        RendererFactory.create(
            renderer_type="unknown",
            blur_strength=51,
        )

def test_create_pixelate_renderer():
    renderer = RendererFactory.create(
        renderer_type="pixelate",
        blur_strength=51,
    )

    assert isinstance(
        renderer,
        PixelateRenderer,
    )

    assert isinstance(
        renderer,
        BaseRenderer,
    )