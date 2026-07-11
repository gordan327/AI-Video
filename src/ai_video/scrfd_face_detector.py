from ai_video.face import Face


class SCRFDFaceDetector:
    """使用 SCRFD 偵測人臉"""

    def __init__(self, model_manager, config):

        self.model_manager = model_manager
        self.config = config

        self.app = self.model_manager.face_analysis

    def detect(self, frame):

        results = self.app.get(frame)

        faces = []

        confidence_threshold = self.config.get(
            "detector.confidence",
            0.5,
        )

        for face in results:

            if face.det_score < confidence_threshold:
                continue

            x1, y1, x2, y2 = map(int, face.bbox)

            faces.append(
                Face(
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                    confidence=float(face.det_score),
                )
            )

        return faces