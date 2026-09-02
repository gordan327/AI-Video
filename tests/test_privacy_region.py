from ai_video.face import Face
from ai_video.privacy_region import PrivacyRegion


def test_create_privacy_box():
    region = PrivacyRegion(
        padding_ratio=0.35,
        top_multiplier=1.7,
        bottom_multiplier=0.8,
    )

    face = Face(
        x1=100,
        y1=100,
        x2=200,
        y2=200,
        confidence=0.9,
    )

    box = region.create(
        face=face,
        frame_width=640,
        frame_height=480,
    )

    assert box is not None

    assert box.x1 == 65
    assert box.y1 == 41
    assert box.x2 == 235
    assert box.y2 == 228


def test_privacy_box_is_clipped_to_frame():
    region = PrivacyRegion(
        padding_ratio=0.50,
    )

    face = Face(
        x1=10,
        y1=10,
        x2=60,
        y2=60,
        confidence=0.9,
    )

    box = region.create(
        face=face,
        frame_width=100,
        frame_height=100,
    )

    assert box is not None

    assert box.x1 == 0
    assert box.y1 == 0
    assert box.x2 <= 100
    assert box.y2 <= 100


def test_invalid_face_box_returns_none():
    region = PrivacyRegion()

    face = Face(
        x1=100,
        y1=100,
        x2=100,
        y2=100,
        confidence=0.9,
    )

    box = region.create(
        face=face,
        frame_width=640,
        frame_height=480,
    )

    assert box is None


def test_privacy_box_dimensions():
    region = PrivacyRegion(
        padding_ratio=0.20,
    )

    face = Face(
        x1=100,
        y1=100,
        x2=200,
        y2=200,
        confidence=0.9,
    )

    box = region.create(
        face=face,
        frame_width=640,
        frame_height=480,
    )

    assert box is not None
    assert box.width > 100
    assert box.height > 100
    assert box.is_valid