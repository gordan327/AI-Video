import cv2

from ai_video.face import Face


class FaceRenderer:
    """負責將人臉資訊繪製到影像上"""

    def draw(self, frame, faces: list[Face]):

        for face in faces:

            cv2.rectangle(
                frame,
                (face.x1, face.y1),
                (face.x2, face.y2),
                (0, 255, 0),
                2,
            )

            label = f"ID:{face.track_id}  {face.confidence:.2f}"

            cv2.putText(
                frame,
                label,
                (face.x1, face.y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        return frame