#!/usr/bin/env python3
"""
AI-Video Detector Benchmark Tool

This tool benchmarks detector configurations by measuring
face detection speed on the first frame of an input video.
"""

from __future__ import annotations

import argparse
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from ai_video.config_manager import ConfigManager
from ai_video.detector.detector_factory import DetectorFactory
from ai_video.model_manager import ModelManager
from ai_video.video.video_reader import VideoReader


@dataclass(frozen=True)
class BenchmarkResult:
    """Store detector benchmark results."""

    face_count: int
    elapsed_times: tuple[float, ...]

    @property
    def runs(self) -> int:
        """Return the number of measured benchmark runs."""

        return len(self.elapsed_times)

    @property
    def average_seconds(self) -> float:
        """Return the average detection time in seconds."""

        return statistics.fmean(self.elapsed_times)

    @property
    def minimum_seconds(self) -> float:
        """Return the minimum detection time in seconds."""

        return min(self.elapsed_times)

    @property
    def maximum_seconds(self) -> float:
        """Return the maximum detection time in seconds."""

        return max(self.elapsed_times)

    @property
    def standard_deviation_seconds(self) -> float:
        """Return the population standard deviation in seconds."""

        return statistics.pstdev(self.elapsed_times)

    @property
    def average_fps(self) -> float:
        """Return the FPS equivalent based on average detection time."""

        if self.average_seconds <= 0:
            return 0.0

        return 1.0 / self.average_seconds


def positive_integer(value: str) -> int:
    """Convert a command-line value to a positive integer."""

    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Expected an integer, received: {value}"
        ) from exc

    if number < 1:
        raise argparse.ArgumentTypeError(
            "The number of benchmark runs must be at least 1."
        )

    return number


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="Benchmark AI-Video detector configurations.",
    )

    parser.add_argument(
        "video",
        type=Path,
        help="Path to the input video.",
    )

    parser.add_argument(
        "--runs",
        type=positive_integer,
        default=1,
        help="Number of measured detection runs (default: 1).",
    )

    return parser


def benchmark_detector(
    detector: Any,
    frame: Any,
    runs: int,
) -> BenchmarkResult:
    """
    Benchmark a detector on one frame.

    One warm-up detection is performed before measurements so that
    one-time initialization work does not distort the statistics.
    """

    detector.detect(frame)

    elapsed_times: list[float] = []
    face_count = 0

    for _ in range(runs):
        start_time = time.perf_counter()

        faces = detector.detect(frame)

        elapsed_time = time.perf_counter() - start_time

        elapsed_times.append(elapsed_time)
        face_count = len(faces)

    return BenchmarkResult(
        face_count=face_count,
        elapsed_times=tuple(elapsed_times),
    )


def print_benchmark_result(result: BenchmarkResult) -> None:
    """Print detector benchmark statistics."""

    print()
    print("Detection Result")
    print("----------------")
    print(f"Faces detected : {result.face_count}")

    print()
    print("Benchmark Statistics")
    print("--------------------")
    print(f"Runs           : {result.runs}")
    print(f"Average        : {result.average_seconds * 1000:.2f} ms")
    print(f"Minimum        : {result.minimum_seconds * 1000:.2f} ms")
    print(f"Maximum        : {result.maximum_seconds * 1000:.2f} ms")
    print(
        "Std Dev        : "
        f"{result.standard_deviation_seconds * 1000:.2f} ms"
    )
    print(f"FPS Equivalent : {result.average_fps:.2f}")


def main() -> int:
    """Run the detector benchmark tool."""

    parser = create_parser()
    args = parser.parse_args()

    print("=" * 50)
    print("AI-Video Detector Benchmark")
    print("Version 0.2")
    print("=" * 50)
    print()

    print(f"Input video : {args.video}")

    reader = VideoReader(str(args.video))

    try:
        reader.open()

        print()
        print("Video Information")
        print("-----------------")
        print(f"Resolution : {reader.width} x {reader.height}")
        print(f"FPS        : {reader.fps:.2f}")
        print(f"Frames     : {reader.frame_count}")
        print(f"Duration   : {reader.duration:.2f} sec")

        success, frame = reader.read()

        if not success or frame is None:
            print()
            print("Status : Error")
            print("Unable to read the first frame.")
            return 1

        print()
        print("First Frame")
        print("-----------")
        print(f"Shape      : {frame.shape}")
        print(f"Data type  : {frame.dtype}")

        config = ConfigManager()

        detector_type = config.get(
            "detector.type",
            "scrfd",
        )

        model_manager = ModelManager(config)

        detector = DetectorFactory.create(
            detector_type=detector_type,
            model_manager=model_manager,
            config=config,
        )

        print()
        print("Detector")
        print("--------")
        print(f"Type       : {detector_type}")
        print(f"Class      : {detector.__class__.__name__}")
        print("Status     : Initialized")

        print()
        print("Benchmark")
        print("---------")
        print("Warm-up    : 1 run")
        print(f"Measured   : {args.runs} run(s)")

        result = benchmark_detector(
            detector=detector,
            frame=frame,
            runs=args.runs,
        )

        print_benchmark_result(result)

    except (
        FileNotFoundError,
        RuntimeError,
        ValueError,
    ) as exc:
        print()
        print("Status : Error")
        print(exc)
        return 1

    finally:
        reader.close()

    print()
    print("Status : Ready")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())