from ai_video.face import Face
from ai_video.face_detector import FaceDetector

class SCRFDFaceDetector(FaceDetector):
    """使用 SCRFD 偵測人臉並取得 embedding。"""

    def __init__(self, model_manager, config):
        self.model_manager = model_manager
        self.config = config

        self.app = self.model_manager.face_analysis

    def detect(self, frame) -> list[Face]:
        """偵測影格中的人臉。"""

        results = self.app.get(frame)

        faces: list[Face] = []

        confidence_threshold = self.config.get(
            "detector.confidence",
            0.5,
        )

        for result in results:
            if result.det_score < confidence_threshold:
                continue

            x1, y1, x2, y2 = map(int, result.bbox)

            embedding = result.normed_embedding

            faces.append(
                Face(
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                    confidence=float(result.det_score),
                    embedding=embedding,
                )
            )

        return faces