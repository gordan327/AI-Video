from ultralytics import YOLO

from ai_video.face import Face
from ai_video.detector.face_detector import FaceDetector


class YOLOFaceDetector(FaceDetector):
    """YOLO 人臉偵測器"""

    def __init__(self, model_path: str = "models/yolov11n-face.pt"):

        self.model = YOLO(model_path)

    def detect(self, frame) -> list[Face]:
        """偵測影格中的所有人臉"""

        return []