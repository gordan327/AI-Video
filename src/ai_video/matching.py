from ai_video.assignment import GreedyAssignment
from ai_video.cost_matrix import CostMatrix


class Matcher:
    """負責協調成本矩陣與配對演算法。"""

    def __init__(
        self,
        minimum_score: float = 0.20,
    ):
        self.minimum_score = minimum_score

        self.cost_matrix = CostMatrix()
        self.assignment = GreedyAssignment()

    def match(self, tracks, faces):
        """
        配對 Track 與 Face。

        回傳：
            matched_pairs: list[tuple[Track, Face]]
            unmatched_tracks: list[Track]
            unmatched_faces: list[Face]
        """

        if not tracks:
            return (
                [],
                [],
                faces.copy(),
            )

        if not faces:
            return (
                [],
                tracks.copy(),
                [],
            )

        score_matrix = self.cost_matrix.build(
            tracks,
            faces,
        )

        assigned_pairs = self.assignment.assign(
            score_matrix,
        )

        matched_pairs = []
        matched_track_indexes = set()
        matched_face_indexes = set()

        for track_index, face_index in assigned_pairs:

            score = score_matrix[track_index][face_index]

            if score < self.minimum_score:
                continue

            matched_pairs.append(
                (
                    tracks[track_index],
                    faces[face_index],
                )
            )

            matched_track_indexes.add(track_index)
            matched_face_indexes.add(face_index)

        unmatched_tracks = [
            track
            for index, track in enumerate(tracks)
            if index not in matched_track_indexes
        ]

        unmatched_faces = [
            face
            for index, face in enumerate(faces)
            if index not in matched_face_indexes
        ]

        return (
            matched_pairs,
            unmatched_tracks,
            unmatched_faces,
        )