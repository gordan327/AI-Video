import numpy as np

from ai_video.face import Face
from ai_video.matching import Matcher
from ai_video.track import Track


def create_face(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    embedding: np.ndarray,
) -> Face:
    return Face(
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        confidence=0.9,
        embedding=embedding,
    )


def test_no_tracks_returns_all_faces_unmatched():
    matcher = Matcher()

    face = create_face(
        0,
        0,
        100,
        100,
        np.array([1.0, 0.0, 0.0], dtype=np.float32),
    )

    matched, unmatched_tracks, unmatched_faces = matcher.match(
        [],
        [face],
    )

    assert matched == []
    assert unmatched_tracks == []
    assert unmatched_faces == [face]


def test_no_faces_returns_all_tracks_unmatched():
    matcher = Matcher()

    face = create_face(
        0,
        0,
        100,
        100,
        np.array([1.0, 0.0, 0.0], dtype=np.float32),
    )

    track = Track(
        track_id=1,
        face=face,
    )

    matched, unmatched_tracks, unmatched_faces = matcher.match(
        [track],
        [],
    )

    assert matched == []
    assert unmatched_tracks == [track]
    assert unmatched_faces == []


def test_single_track_matches_same_face():
    matcher = Matcher()

    embedding = np.array(
        [1.0, 0.0, 0.0],
        dtype=np.float32,
    )

    track_face = create_face(
        0,
        0,
        100,
        100,
        embedding,
    )

    detected_face = create_face(
        2,
        2,
        102,
        102,
        embedding,
    )

    track = Track(
        track_id=1,
        face=track_face,
    )

    matched, unmatched_tracks, unmatched_faces = matcher.match(
        [track],
        [detected_face],
    )

    assert matched == [(track, detected_face)]
    assert unmatched_tracks == []
    assert unmatched_faces == []


def test_low_score_pair_remains_unmatched():
    matcher = Matcher(
        minimum_score=0.90,
    )

    track_face = create_face(
        0,
        0,
        100,
        100,
        np.array([1.0, 0.0, 0.0], dtype=np.float32),
    )

    far_face = create_face(
        500,
        500,
        600,
        600,
        np.array([0.0, 1.0, 0.0], dtype=np.float32),
    )

    track = Track(
        track_id=1,
        face=track_face,
    )

    matched, unmatched_tracks, unmatched_faces = matcher.match(
        [track],
        [far_face],
    )

    assert matched == []
    assert unmatched_tracks == [track]
    assert unmatched_faces == [far_face]


def test_two_tracks_match_correct_faces():
    matcher = Matcher()

    embedding1 = np.array(
        [1.0, 0.0, 0.0],
        dtype=np.float32,
    )

    embedding2 = np.array(
        [0.0, 1.0, 0.0],
        dtype=np.float32,
    )

    track1 = Track(
        track_id=1,
        face=create_face(
            0,
            0,
            100,
            100,
            embedding1,
        ),
    )

    track2 = Track(
        track_id=2,
        face=create_face(
            200,
            200,
            300,
            300,
            embedding2,
        ),
    )

    face1 = create_face(
        3,
        3,
        103,
        103,
        embedding1,
    )

    face2 = create_face(
        203,
        203,
        303,
        303,
        embedding2,
    )

    matched, unmatched_tracks, unmatched_faces = matcher.match(
        [track1, track2],
        [face2, face1],
    )

    assert set(
        (track.track_id, face is face1, face is face2)
        for track, face in matched
    ) == {
        (1, True, False),
        (2, False, True),
    }

    assert unmatched_tracks == []
    assert unmatched_faces == []