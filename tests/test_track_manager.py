import numpy as np

from ai_video.face import Face
from ai_video.matching import Matcher
from ai_video.track_manager import TrackManager
from ai_video.track_state import TrackState


def create_face(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    embedding: np.ndarray | None = None,
) -> Face:
    return Face(
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        confidence=0.9,
        embedding=embedding,
    )


def test_create_track_assigns_id_and_active_state():
    manager = TrackManager()

    face = create_face(
        0,
        0,
        100,
        100,
    )

    track = manager.create_track(face)

    assert track.track_id == 1
    assert face.track_id == 1
    assert track.state == TrackState.ACTIVE
    assert manager.get_tracks() == [track]


def test_create_multiple_tracks_uses_incrementing_ids():
    manager = TrackManager()

    track1 = manager.create_track(
        create_face(0, 0, 100, 100)
    )

    track2 = manager.create_track(
        create_face(200, 200, 300, 300)
    )

    assert track1.track_id == 1
    assert track2.track_id == 2


def test_update_track_keeps_same_id_and_resets_state():
    manager = TrackManager()

    original_face = create_face(
        0,
        0,
        100,
        100,
        np.array([1.0, 0.0], dtype=np.float32),
    )

    track = manager.create_track(original_face)

    track.state = TrackState.LOST
    track.missed = 5

    new_face = create_face(
        5,
        5,
        105,
        105,
        np.array([1.0, 0.0], dtype=np.float32),
    )

    manager.update_track(
        track,
        new_face,
    )

    assert new_face.track_id == track.track_id
    assert track.face is new_face
    assert track.state == TrackState.ACTIVE
    assert track.missed == 0
    assert track.age == 1


def test_mark_lost_track_changes_state_to_lost():
    manager = TrackManager()

    track = manager.create_track(
        create_face(0, 0, 100, 100)
    )

    manager.mark_lost_track(track)

    assert track.missed == 1
    assert track.state == TrackState.LOST


def test_mark_lost_track_removes_after_30_frames():
    manager = TrackManager()

    track = manager.create_track(
        create_face(0, 0, 100, 100)
    )

    track.missed = 29

    manager.mark_lost_track(track)

    assert track.missed == 30
    assert track.state == TrackState.REMOVED


def test_remove_removed_tracks():
    manager = TrackManager()

    active_track = manager.create_track(
        create_face(0, 0, 100, 100)
    )

    removed_track = manager.create_track(
        create_face(200, 200, 300, 300)
    )

    removed_track.state = TrackState.REMOVED

    manager.remove_removed_tracks()

    assert manager.get_tracks() == [active_track]


def test_update_tracks_creates_track_for_new_face():
    manager = TrackManager()
    matcher = Matcher()

    face = create_face(
        0,
        0,
        100,
        100,
        np.array([1.0, 0.0], dtype=np.float32),
    )

    result = manager.update_tracks(
        matcher,
        [face],
    )

    assert result == [face]
    assert face.track_id == 1
    assert len(manager.get_tracks()) == 1


def test_update_tracks_reuses_existing_track():
    manager = TrackManager()
    matcher = Matcher()

    embedding = np.array(
        [1.0, 0.0],
        dtype=np.float32,
    )

    first_face = create_face(
        0,
        0,
        100,
        100,
        embedding,
    )

    manager.update_tracks(
        matcher,
        [first_face],
    )

    second_face = create_face(
        3,
        3,
        103,
        103,
        embedding,
    )

    manager.update_tracks(
        matcher,
        [second_face],
    )

    assert second_face.track_id == 1
    assert len(manager.get_tracks()) == 1


def test_reset_clears_tracks_and_restarts_ids():
    manager = TrackManager()

    manager.create_track(
        create_face(0, 0, 100, 100)
    )

    manager.reset()

    assert manager.get_tracks() == []

    new_track = manager.create_track(
        create_face(200, 200, 300, 300)
    )

    assert new_track.track_id == 1