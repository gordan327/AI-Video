import numpy as np

from ai_video.face import Face
from ai_video.face_renderer import FaceRenderer


def create_test_frame():
    """建立具有高反差區塊的測試影像。"""

    frame = np.zeros(
        (80, 80, 3),
        dtype=np.uint8,
    )

    frame[20:60, 20:40] = 255
    frame[20:60, 40:60] = 0

    return frame


def test_face_renderer_blurs_detected_face():
    renderer = FaceRenderer(
        blur_strength=11,
        padding_ratio=0.0,
        temporal_hold_frames=3,
    )

    frame = create_test_frame()
    original = frame.copy()

    face = Face(
        x1=20,
        y1=20,
        x2=60,
        y2=60,
        confidence=0.9,
        track_id=1,
    )

    renderer.draw(
        frame,
        [face],
    )

    assert not np.array_equal(
        frame[20:60, 20:60],
        original[20:60, 20:60],
    )


def test_temporal_cache_keeps_blur_after_face_disappears():
    renderer = FaceRenderer(
        blur_strength=11,
        padding_ratio=0.0,
        temporal_hold_frames=3,
    )

    face = Face(
        x1=20,
        y1=20,
        x2=60,
        y2=60,
        confidence=0.9,
        track_id=1,
    )

    # 第一幀：偵測到人臉，建立快取
    first_frame = create_test_frame()

    renderer.draw(
        first_frame,
        [face],
    )

    # 第二幀：人臉暫時消失，但應繼續模糊
    second_frame = create_test_frame()
    original_second = second_frame.copy()

    renderer.draw(
        second_frame,
        [],
    )

    assert not np.array_equal(
        second_frame[20:60, 20:60],
        original_second[20:60, 20:60],
    )


def test_temporal_cache_expires():
    renderer = FaceRenderer(
        blur_strength=11,
        padding_ratio=0.0,
        temporal_hold_frames=2,
    )

    face = Face(
        x1=20,
        y1=20,
        x2=60,
        y2=60,
        confidence=0.9,
        track_id=1,
    )

    renderer.draw(
        create_test_frame(),
        [face],
    )

    # 保留第 1 幀
    renderer.draw(
        create_test_frame(),
        [],
    )

    # 保留第 2 幀
    renderer.draw(
        create_test_frame(),
        [],
    )

    # 第 3 幀應已過期
    final_frame = create_test_frame()
    original_final = final_frame.copy()

    renderer.draw(
        final_frame,
        [],
    )

    assert np.array_equal(
        final_frame,
        original_final,
    )


def test_reset_clears_temporal_cache():
    renderer = FaceRenderer(
        blur_strength=11,
        padding_ratio=0.0,
        temporal_hold_frames=5,
    )

    face = Face(
        x1=20,
        y1=20,
        x2=60,
        y2=60,
        confidence=0.9,
        track_id=1,
    )

    renderer.draw(
        create_test_frame(),
        [face],
    )

    renderer.reset()

    frame = create_test_frame()
    original = frame.copy()

    renderer.draw(
        frame,
        [],
    )

    assert np.array_equal(
        frame,
        original,
    )