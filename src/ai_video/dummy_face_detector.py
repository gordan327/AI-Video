from ai_video.face import Face
from ai_video.face_detector import FaceDetector


class DummyFaceDetector(FaceDetector):
    """測試用的人臉偵測器"""

    def __init__(
        self,
        x1: int = 150,
        y1: int = 200,
        x2: int = 350,
        y2: int = 450,
    ):

        self.face = Face(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            confidence=1.0,
        )

    def detect(self, frame) -> list[Face]:
        """固定回傳一張人臉"""

        return [self.face]