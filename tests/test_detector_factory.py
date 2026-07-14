import pytest

from ai_video.detector_factory import DetectorFactory
from ai_video.face_detector import FaceDetector
from ai_video.scrfd_face_detector import SCRFDFaceDetector


class DummyConfig:
    def get(self, key, default=None):
        return default


class DummyModelManager:
    @property
    def face_analysis(self):
        return object()


def test_create_scrfd_detector():
    detector = DetectorFactory.create(
        detector_type="scrfd",
        model_manager=DummyModelManager(),
        config=DummyConfig(),
    )

    assert isinstance(
        detector,
        SCRFDFaceDetector,
    )

    assert isinstance(
        detector,
        FaceDetector,
    )


def test_detector_type_is_case_insensitive():
    detector = DetectorFactory.create(
        detector_type="SCRFD",
        model_manager=DummyModelManager(),
        config=DummyConfig(),
    )

    assert isinstance(
        detector,
        SCRFDFaceDetector,
    )


def test_unknown_detector_raises_error():
    with pytest.raises(
        ValueError,
        match="未知人臉偵測器",
    ):
        DetectorFactory.create(
            detector_type="unknown",
            model_manager=DummyModelManager(),
            config=DummyConfig(),
        )