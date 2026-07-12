from ai_video.appearance import cosine_similarity
from ai_video.geometry import (
    calculate_center_distance,
    calculate_iou,
)


class CostMatrix:
    """建立 Track 與 Face 的配對分數矩陣。"""

    def __init__(
        self,
        max_center_distance: float = 80.0,
        motion_weight: float = 0.40,
        appearance_weight: float = 0.60,
    ):
        self.max_center_distance = max_center_distance
        self.motion_weight = motion_weight
        self.appearance_weight = appearance_weight

    def build(self, tracks, faces) -> list[list[float]]:
        """建立 Track × Face 的配對分數矩陣。"""

        matrix: list[list[float]] = []

        for track in tracks:
            row: list[float] = []

            predicted_box = track.predicted_box

            if predicted_box is None:
                predicted_box = (
                    track.face.x1,
                    track.face.y1,
                    track.face.x2,
                    track.face.y2,
                )

            track_embedding = track.get_average_embedding()

            for face in faces:
                face_box = (
                    face.x1,
                    face.y1,
                    face.x2,
                    face.y2,
                )

                iou = calculate_iou(
                    predicted_box,
                    face_box,
                )

                center_distance = calculate_center_distance(
                    predicted_box,
                    face_box,
                )

                distance_score = max(
                    0.0,
                    1.0
                    - center_distance / self.max_center_distance,
                )

                motion_score = (
                    iou * 0.8
                    + distance_score * 0.2
                )

                similarity = cosine_similarity(
                    track_embedding,
                    face.embedding,
                )

                appearance_score = (
                    similarity + 1.0
                ) / 2.0

                final_score = (
                    motion_score * self.motion_weight
                    + appearance_score * self.appearance_weight
                )

                row.append(final_score)

            matrix.append(row)

        return matrix