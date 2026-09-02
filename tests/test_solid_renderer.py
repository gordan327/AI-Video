import numpy as np

from ai_video.renderer.solid_renderer import SolidRenderer


def test_solid_renderer_fills_region():
    renderer = SolidRenderer()

    frame = np.full(
        (20, 20, 3),
        255,
        dtype=np.uint8,
    )

    renderer.render(
        frame,
        (5, 5, 15, 15),
    )

    roi = frame[
        5:15,
        5:15,
    ]

    assert np.all(roi == 0)
    assert np.all(frame[0:5, 0:5] == 255)