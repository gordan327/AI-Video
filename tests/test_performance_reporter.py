from ai_video.processing.performance_reporter import (
    PerformanceReporter,
)


def test_performance_reporter_prints_report(
    capsys,
):
    """應輸出完整的模組效能報告。"""

    PerformanceReporter.print_report(
        frame_count=10,
        processing_time=2.0,
        detector_time=0.8,
        tracker_time=0.2,
        renderer_time=0.4,
        writer_time=0.1,
    )

    output = capsys.readouterr().out

    assert "AI-Video Module Performance" in output
    assert "Frames          : 10" in output
    assert "Processing Time : 2.00 sec" in output
    assert "Processing FPS  : 5.00" in output
    assert "Detection" in output
    assert "Tracking" in output
    assert "Rendering" in output
    assert "Video Writing" in output
    assert "Other / Reading" in output


def test_performance_reporter_handles_zero_frames(
    capsys,
):
    """沒有影格時應顯示提示，而不是進行除法。"""

    PerformanceReporter.print_report(
        frame_count=0,
        processing_time=0.0,
        detector_time=0.0,
        tracker_time=0.0,
        renderer_time=0.0,
        writer_time=0.0,
    )

    output = capsys.readouterr().out

    assert output.strip() == "沒有可供統計的影格。"
