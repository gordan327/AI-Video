from ai_video.face_detector import FaceDetector
from ai_video.scrfd_face_detector import SCRFDFaceDetector


_DETECTORS = {
    "scrfd": SCRFDFaceDetector,
}


class DetectorFactory:
    """建立指定類型的人臉偵測器。"""

    @staticmethod
    def create(
        detector_type: str,
        model_manager,
        config,
    ) -> FaceDetector:
        detector_key = detector_type.strip().lower()

        detector_class = _DETECTORS.get(
            detector_key
        )

        if detector_class is None:
            raise ValueError(
                f"未知人臉偵測器：{detector_type}"
            )

        return detector_class(
            model_manager=model_manager,
            config=config,
        )