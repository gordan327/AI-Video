import numpy as np
import supervision as sv

from ai_video.face import Face


class FaceDetectionAdapter:
    """將 Face 物件轉換成 Supervision Detections"""

    def to_detections(
        self,
        faces: list[Face],
    ) -> sv.Detections:

        if len(faces) == 0:

            return sv.Detections.empty()

        xyxy = np.array(
            [
                [f.x1, f.y1, f.x2, f.y2]
                for f in faces
            ],
            dtype=np.float32,
        )

        confidence = np.array(
            [
                f.confidence
                for f in faces
            ],
            dtype=np.float32,
        )

        class_id = np.zeros(
            len(faces),
            dtype=np.int32,
        )

        return sv.Detections(
            xyxy=xyxy,
            confidence=confidence,
            class_id=class_id,
        )