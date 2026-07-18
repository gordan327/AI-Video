from pathlib import Path

from ai_video.gui.processing_job import ProcessingJob


def test_processing_job_stores_processing_values():
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

    assert job.input_path == Path(
        "/videos/input.mp4"
    )
    assert job.output_path == Path(
        "/exports/output.mp4"
    )
    assert job.temp_output_path == Path(
        "/exports/output_video_only.mp4"
    )
    assert job.detector == "scrfd"
    assert job.tracker == "bytetrack"
    assert job.renderer == "blur"