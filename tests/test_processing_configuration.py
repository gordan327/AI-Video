from pathlib import Path

from ai_video.gui.processing_configuration import (
    ProcessingConfiguration,
)
from ai_video.gui.processing_job import ProcessingJob

class FakeConfig:
    """測試用的簡易設定物件。"""

    def __init__(self):
        self.values = {}

    def set(self, key, value):
        self.values[key] = value


def test_apply_processing_configuration():
    config = FakeConfig()

    job = ProcessingJob(
        input_path=Path("/videos/input.mp4"),
        output_path=Path("/exports/output.mp4"),
        temp_output_path=Path(
            "/exports/output_video_only.mp4"
        ),
        detector="scrfd",
        tracker="bytetrack",
        renderer="blur",
    )

    ProcessingConfiguration.apply(
        config=config,
        job=job,
    )

    assert config.values == {
        "video.input": "/videos/input.mp4",
        "video.temp_output": (
            "/exports/output_video_only.mp4"
        ),
        "video.output": "/exports/output.mp4",
        "detector.type": "scrfd",
        "tracker.type": "bytetrack",
        "renderer.type": "blur",
    }