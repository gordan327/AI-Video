from ai_video.geometry import (
    calculate_iou,
    calculate_center_distance,
)


class CostMatrix:
    """建立 Track 與 Face 的成本矩陣"""

    def __init__(
        self,
        max_center_distance: float = 80,
    ):
        self.max_center_distance = max_center_distance

    def build(
        self,
        tracks,
        faces,
    ):

        matrix = []

        for track in tracks:

            row = []

            predicted_box = track.predicted_box

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

                distance = calculate_center_distance(
                    predicted_box,
                    face_box,
                )

                score = (
                    iou * 0.8
                    + max(
                        0,
                        1 - distance / self.max_center_distance,
                    ) * 0.2
                )

                row.append(score)

            matrix.append(row)

        return matrix