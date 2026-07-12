from ai_video.assignment import HungarianAssignment


def test_empty_matrix_returns_no_pairs():
    assignment = HungarianAssignment()

    assert assignment.assign([]) == []


def test_matrix_with_empty_row_returns_no_pairs():
    assignment = HungarianAssignment()

    assert assignment.assign([[]]) == []


def test_single_track_single_face():
    assignment = HungarianAssignment()

    pairs = assignment.assign([
        [0.9],
    ])

    assert pairs == [(0, 0)]


def test_two_tracks_choose_diagonal_pairs():
    assignment = HungarianAssignment()

    pairs = assignment.assign([
        [0.9, 0.1],
        [0.2, 0.8],
    ])

    assert set(pairs) == {
        (0, 0),
        (1, 1),
    }


def test_hungarian_finds_global_best_assignment():
    assignment = HungarianAssignment()

    # 若使用逐筆 Greedy，可能先選 (0, 0)，
    # 但整體最佳解是 (0, 1) 與 (1, 0)。
    pairs = assignment.assign([
        [0.90, 0.80],
        [0.85, 0.10],
    ])

    assert set(pairs) == {
        (0, 1),
        (1, 0),
    }


def test_more_tracks_than_faces():
    assignment = HungarianAssignment()

    pairs = assignment.assign([
        [0.9, 0.1],
        [0.2, 0.8],
        [0.4, 0.3],
    ])

    assert len(pairs) == 2

    track_indexes = {
        track_index
        for track_index, _ in pairs
    }

    face_indexes = {
        face_index
        for _, face_index in pairs
    }

    assert len(track_indexes) == 2
    assert face_indexes == {0, 1}