import numpy as np

from ai_video.renderer.pixelate_renderer import PixelateRenderer


def test_pixelate_changes_region():
    """Pixelate 應修改指定區域的畫面。"""

    frame = np.random.randint(
        0,
        255,
        (100, 100, 3),
        dtype=np.uint8,
    )

    original = frame.copy()

    renderer = PixelateRenderer(
        pixel_size=10,
    )

    renderer.render(
        frame,
        (20, 20, 80, 80),
    )

    assert not np.array_equal(
        original[20:80, 20:80],
        frame[20:80, 20:80],
    )


def test_pixelate_keeps_outside_region():
    """Pixelate 不應修改指定區域外的畫面。"""

    frame = np.random.randint(
        0,
        255,
        (100, 100, 3),
        dtype=np.uint8,
    )

    original = frame.copy()

    renderer = PixelateRenderer()

    renderer.render(
        frame,
        (20, 20, 80, 80),
    )

    assert np.array_equal(
        original[:20, :20],
        frame[:20, :20],
    )


def test_pixelate_invalid_box():
    """無效區域不應拋出例外。"""

    frame = np.zeros(
        (100, 100, 3),
        dtype=np.uint8,
    )

    renderer = PixelateRenderer()

    renderer.render(
        frame,
        (50, 50, 50, 50),
    )


def test_pixelate_clips_out_of_bounds():
    """超出畫面的座標應安全裁切。"""

    frame = np.zeros(
        (100, 100, 3),
        dtype=np.uint8,
    )

    renderer = PixelateRenderer()

    renderer.render(
        frame,
        (-20, -20, 150, 150),
    )