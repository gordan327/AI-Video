import numpy as np

from ai_video.renderer.base_renderer import BaseRenderer


class DummyRenderer(BaseRenderer):
    def render(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        pass


def test_extract_roi_clips_box_to_frame():
    renderer = DummyRenderer()

    frame = np.zeros(
        (20, 20, 3),
        dtype=np.uint8,
    )

    roi = renderer.extract_roi(
        frame,
        (-10, -10, 15, 15),
    )

    assert roi.shape == (
        15,
        15,
        3,
    )

def test_extract_roi_returns_none_for_invalid_box():
    renderer = DummyRenderer()

    frame = np.zeros(
        (20, 20, 3),
        dtype=np.uint8,
    )

    roi = renderer.extract_roi(
        frame,
        (10, 10, 10, 10),
    )

    assert roi is None