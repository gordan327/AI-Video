import numpy as np
import pytest

from ai_video.tracking.cost_matrix import CostMatrix
from ai_video.face import Face
from ai_video.tracking.track import Track


def create_face(
    x1,
    y1,
    x2,
    y2,
):
    return Face(
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        confidence=0.9,
        embedding=np.array(
            [1.0, 0.0, 0.0],
            dtype=np.float32,
        ),
    )


def test_single_track_single_face():

    face = create_face(
        0,
        0,
        100,
        100,
    )

    track = Track(
        track_id=1,
        face=face,
    )

    matrix = CostMatrix().build(
        [track],
        [face],
    )

    assert len(matrix) == 1
    assert len(matrix[0]) == 1

    assert matrix[0][0] > 0.9


def test_far_face_has_lower_score():

    track = Track(
        track_id=1,
        face=create_face(
            0,
            0,
            100,
            100,
        ),
    )

    far_face = create_face(
        500,
        500,
        600,
        600,
    )

    matrix = CostMatrix().build(
        [track],
        [far_face],
    )

    assert matrix[0][0] == pytest.approx(0.6)


def test_two_tracks_two_faces():

    face1 = create_face(
        0,
        0,
        100,
        100,
    )

    face2 = create_face(
        200,
        200,
        300,
        300,
    )

    track1 = Track(
        track_id=1,
        face=face1,
    )

    track2 = Track(
        track_id=2,
        face=face2,
    )

    matrix = CostMatrix().build(
        [track1, track2],
        [face1, face2],
    )

    assert len(matrix) == 2

    assert len(matrix[0]) == 2

    assert matrix[0][0] > matrix[0][1]

    assert matrix[1][1] > matrix[1][0]