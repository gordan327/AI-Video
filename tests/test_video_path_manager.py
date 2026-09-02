from pathlib import Path

from ai_video.gui.video_path_manager import (
    VideoPathManager,
)


def test_build_default_output_path():
    output_path = (
        VideoPathManager.build_default_output_path(
            "/videos/sample.mov",
            "/exports",
        )
    )

    assert output_path == Path(
        "/exports/sample_blurred.mp4"
    )

def test_build_output_path_keeps_existing_suffix():
    output_path = (
        VideoPathManager.build_output_path(
            "/exports/result.mp4"
        )
    )

    assert output_path == Path(
        "/exports/result.mp4"
    )


def test_build_output_path_adds_mp4_suffix():
    output_path = (
        VideoPathManager.build_output_path(
            "/exports/result"
        )
    )

    assert output_path == Path(
        "/exports/result.mp4"
    )

def test_build_temp_output_path():
    temp_output_path = (
        VideoPathManager.build_temp_output_path(
            "/exports/result.mp4"
        )
    )

    assert temp_output_path == Path(
        "/exports/result_video_only.mp4"
    )