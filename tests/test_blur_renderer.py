import numpy as np

from ai_video.renderer.blur_renderer import BlurRenderer


def test_blur_changes_target_region():
    renderer = BlurRenderer(
        blur_strength=11,
    )

    frame = np.zeros(
        (40, 40, 3),
        dtype=np.uint8,
    )

    # 在中央建立高反差圖案
    frame[10:30, 10:20] = 255
    frame[10:30, 20:30] = 0

    original_region = frame[
        10:30,
        10:30,
    ].copy()

    renderer.render(
        frame,
        (10, 10, 30, 30),
    )

    blurred_region = frame[
        10:30,
        10:30,
    ]

    assert not np.array_equal(
        original_region,
        blurred_region,
    )


def test_blur_does_not_change_outside_region():
    renderer = BlurRenderer(
        blur_strength=11,
    )

    frame = np.zeros(
        (40, 40, 3),
        dtype=np.uint8,
    )

    frame[10:30, 10:20] = 255
    frame[10:30, 20:30] = 0

    original_frame = frame.copy()

    renderer.render(
        frame,
        (10, 10, 30, 30),
    )

    # 上方區域不應改變
    assert np.array_equal(
        frame[0:10, :],
        original_frame[0:10, :],
    )

    # 下方區域不應改變
    assert np.array_equal(
        frame[30:40, :],
        original_frame[30:40, :],
    )

    # 左側區域不應改變
    assert np.array_equal(
        frame[:, 0:10],
        original_frame[:, 0:10],
    )

    # 右側區域不應改變
    assert np.array_equal(
        frame[:, 30:40],
        original_frame[:, 30:40],
    )


def test_blur_clips_box_to_frame():
    renderer = BlurRenderer(
        blur_strength=11,
    )

    frame = np.zeros(
        (20, 20, 3),
        dtype=np.uint8,
    )

    frame[0:10, 0:5] = 255

    renderer.render(
        frame,
        (-10, -10, 15, 15),
    )

    assert frame.shape == (
        20,
        20,
        3,
    )


def test_blur_ignores_invalid_box():
    renderer = BlurRenderer(
        blur_strength=11,
    )

    frame = np.zeros(
        (20, 20, 3),
        dtype=np.uint8,
    )

    original_frame = frame.copy()

    renderer.render(
        frame,
        (10, 10, 10, 10),
    )

    assert np.array_equal(
        frame,
        original_frame,
    )