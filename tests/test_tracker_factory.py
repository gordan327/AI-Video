import pytest

from ai_video.tracker.bytetrack_face_tracker import (
    ByteTrackFaceTracker,
)
from ai_video.tracker.face_tracker import FaceTracker
from ai_video.tracker.tracker_factory import TrackerFactory


def test_create_bytetrack_tracker():
    tracker = TrackerFactory.create(
        tracker_type="bytetrack",
        privacy_hold_frames=20,
        prediction_frames=4,
        freeze_expansion_per_frame=0.05,
    )

    assert isinstance(
        tracker,
        ByteTrackFaceTracker,
    )

    assert isinstance(
        tracker,
        FaceTracker,
    )

    assert tracker.privacy_hold_frames == 20
    assert tracker.prediction_frames == 4

    assert (
        tracker.freeze_expansion_per_frame
        == pytest.approx(0.05)
    )


def test_tracker_type_is_case_insensitive():
    tracker = TrackerFactory.create(
        tracker_type="BYTETRACK",
    )

    assert isinstance(
        tracker,
        ByteTrackFaceTracker,
    )


def test_unknown_tracker_raises_error():
    with pytest.raises(
        ValueError,
        match="未知人臉追蹤器",
    ):
        TrackerFactory.create(
            tracker_type="unknown",
        )