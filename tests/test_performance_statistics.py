import pytest

from ai_video.processing.performance_statistics import (
    PerformanceStatistics,
)


def test_default_statistics_are_zero():
    statistics = PerformanceStatistics()

    assert statistics.detector_time == 0.0
    assert statistics.tracker_time == 0.0
    assert statistics.renderer_time == 0.0
    assert statistics.writer_time == 0.0


def test_add_elapsed_times():
    statistics = PerformanceStatistics()

    statistics.add_detector_time(1.25)
    statistics.add_tracker_time(2.5)
    statistics.add_renderer_time(3.75)
    statistics.add_writer_time(4.0)

    assert statistics.detector_time == pytest.approx(
        1.25
    )
    assert statistics.tracker_time == pytest.approx(
        2.5
    )
    assert statistics.renderer_time == pytest.approx(
        3.75
    )
    assert statistics.writer_time == pytest.approx(
        4.0
    )


def test_elapsed_times_are_accumulated():
    statistics = PerformanceStatistics()

    statistics.add_detector_time(0.25)
    statistics.add_detector_time(0.75)

    statistics.add_writer_time(1.0)
    statistics.add_writer_time(2.0)

    assert statistics.detector_time == pytest.approx(
        1.0
    )
    assert statistics.writer_time == pytest.approx(
        3.0
    )


def test_reset_statistics():
    statistics = PerformanceStatistics(
        detector_time=1.0,
        tracker_time=2.0,
        renderer_time=3.0,
        writer_time=4.0,
    )

    statistics.reset()

    assert statistics.detector_time == 0.0
    assert statistics.tracker_time == 0.0
    assert statistics.renderer_time == 0.0
    assert statistics.writer_time == 0.0