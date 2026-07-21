#!/usr/bin/env python3
"""
AI-Video Pipeline Benchmark Tool.

Version 0.5B initializes the main pipeline components, benchmarks face
detection across multiple video frames, saves a debug image, and prints
a benchmark summary.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Any

import cv2


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
DEBUG_IMAGE_PATH = PROJECT_ROOT / "benchmark_detect.jpg"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from ai_video.config_manager import ConfigManager
from ai_video.detector.detector_factory import DetectorFactory
from ai_video.model_manager import ModelManager
from ai_video.renderer.renderer_factory import RendererFactory
from ai_video.tracker.tracker_factory import TrackerFactory
from ai_video.video.video_reader import VideoReader


@dataclass(frozen=True)
class PipelineComponents:
    """Store initialized AI-Video pipeline components."""

    config: ConfigManager
    model_manager: ModelManager
    detector: Any
    tracker: Any
    renderer: Any
    detector_type: str
    tracker_type: str
    renderer_type: str


@dataclass(frozen=True)
class DetectionResult:
    """Store one-frame face detection results."""

    detections: Any
    elapsed_seconds: float


@dataclass
class BenchmarkStatistics:
    """Collect and summarize detector benchmark results."""

    frames_tested: int = 0
    faces_total: int = 0
    elapsed_seconds: list[float] = field(default_factory=list)

    def add(self, result: DetectionResult) -> None:
        """Add one detection result to the statistics."""

        self.frames_tested += 1
        self.faces_total += len(result.detections)
        self.elapsed_seconds.append(result.elapsed_seconds)

    @property
    def average_milliseconds(self) -> float:
        """Return average detection time in milliseconds."""

        if not self.elapsed_seconds:
            return 0.0

        return sum(self.elapsed_seconds) / len(self.elapsed_seconds) * 1000.0

    @property
    def minimum_milliseconds(self) -> float:
        """Return minimum detection time in milliseconds."""

        if not self.elapsed_seconds:
            return 0.0

        return min(self.elapsed_seconds) * 1000.0

    @property
    def maximum_milliseconds(self) -> float:
        """Return maximum detection time in milliseconds."""

        if not self.elapsed_seconds:
            return 0.0

        return max(self.elapsed_seconds) * 1000.0


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Initialize the AI-Video pipeline, benchmark face detection "
            "across multiple video frames, save a debug image, and print "
            "a benchmark summary."
        ),
    )

    parser.add_argument(
        "video",
        type=Path,
        help="Path to the input video.",
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to a YAML configuration file.",
    )

    parser.add_argument(
        "--frames",
        type=int,
        default=10,
        help="Number of frames to benchmark.",
    )

    return parser


def print_header() -> None:
    """Print the benchmark header."""

    print("=" * 50)
    print("AI-Video Pipeline Benchmark")
    print("Version 0.5B")
    print("=" * 50)


def print_video_information(reader: VideoReader) -> None:
    """Print input video metadata."""

    print()
    print("Video Information")
    print("-----------------")
    print(f"Resolution : {reader.width} x {reader.height}")
    print(f"FPS        : {reader.fps:.2f}")
    print(f"Frames     : {reader.frame_count}")
    print(f"Duration   : {reader.duration:.2f} sec")


def initialize_pipeline(config_path: Path | None) -> PipelineComponents:
    """Initialize all primary AI-Video pipeline components."""

    config = ConfigManager(config_path=config_path)

    detector_type = config.get("detector.type", "scrfd")
    tracker_type = config.get("tracker.type", "bytetrack")
    renderer_type = config.get("renderer.type", "blur")

    model_manager = ModelManager(config)

    detector = DetectorFactory.create(
        detector_type=detector_type,
        model_manager=model_manager,
        config=config,
    )

    tracker = TrackerFactory.create(
        tracker_type=tracker_type,
        privacy_hold_frames=config.get("tracker.privacy_hold_frames", 15),
        prediction_frames=config.get("tracker.prediction_frames", 3),
        freeze_expansion_per_frame=config.get(
            "tracker.freeze_expansion_per_frame",
            0.03,
        ),
    )

    renderer = RendererFactory.create(
        renderer_type=renderer_type,
        blur_strength=config.get("renderer.blur_strength", 51),
        pixel_size=config.get("renderer.pixel_size", 12),
    )

    return PipelineComponents(
        config=config,
        model_manager=model_manager,
        detector=detector,
        tracker=tracker,
        renderer=renderer,
        detector_type=detector_type,
        tracker_type=tracker_type,
        renderer_type=renderer_type,
    )


def print_pipeline_information(pipeline: PipelineComponents) -> None:
    """Print initialized pipeline component information."""

    print()
    print("Pipeline Initialization")
    print("-----------------------")
    print("ConfigManager : OK")
    print("ModelManager  : OK")
    print(
        f"Detector      : "
        f"{pipeline.detector_type} "
        f"({pipeline.detector.__class__.__name__})"
    )
    print(
        f"Tracker       : "
        f"{pipeline.tracker_type} "
        f"({pipeline.tracker.__class__.__name__})"
    )
    print(
        f"Renderer      : "
        f"{pipeline.renderer_type} "
        f"({pipeline.renderer.__class__.__name__})"
    )


def detect_faces(detector: Any, frame: Any) -> DetectionResult:
    """Detect faces in one frame and measure elapsed time."""

    started_at = perf_counter()
    detections = detector.detect(frame)
    elapsed_seconds = perf_counter() - started_at

    if detections is None:
        raise RuntimeError("The detector returned no detection result.")

    return DetectionResult(
        detections=detections,
        elapsed_seconds=elapsed_seconds,
    )


def print_frame_detection_information(
    frame_index: int,
    result: DetectionResult,
) -> None:
    """Print one-frame face detection information."""

    elapsed_milliseconds = result.elapsed_seconds * 1000.0

    print(
        f"Frame {frame_index:5d} | "
        f"Faces: {len(result.detections):2d} | "
        f"{elapsed_milliseconds:.2f} ms"
    )


def save_debug_image(
    frame: Any,
    detections: Any,
    output_path: Path,
) -> None:
    """Draw detected face boxes and save the debug image."""

    debug_renderer = RendererFactory.create(
        renderer_type="debug",
        line_thickness=2,
    )

    debug_frame = frame.copy()

    for face in detections:
        debug_renderer.render(
            debug_frame,
            (
                face.x1,
                face.y1,
                face.x2,
                face.y2,
            ),
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    saved = cv2.imwrite(str(output_path), debug_frame)

    if not saved:
        raise RuntimeError(f"Unable to save debug image: {output_path}")


def print_debug_image_information(output_path: Path) -> None:
    """Print debug image output information."""

    print()
    print("Debug Image")
    print("-----------")
    print(f"Output : {output_path}")


def print_benchmark_summary(statistics: BenchmarkStatistics) -> None:
    """Print the detector benchmark summary."""

    print()
    print("=" * 40)
    print("Benchmark Summary")
    print("=" * 40)
    print(f"Frames Tested : {statistics.frames_tested}")
    print(f"Faces Total   : {statistics.faces_total}")
    print()
    print(f"Average Time  : {statistics.average_milliseconds:.2f} ms")
    print(f"Minimum Time  : {statistics.minimum_milliseconds:.2f} ms")
    print(f"Maximum Time  : {statistics.maximum_milliseconds:.2f} ms")
    print("=" * 40)


def main() -> int:
    """Benchmark multi-frame detection and print a summary."""

    parser = create_parser()
    args = parser.parse_args()

    if args.frames <= 0:
        parser.error("--frames must be greater than zero.")

    print_header()

    print()
    print(f"Input video : {args.video}")

    reader = VideoReader(str(args.video))

    try:
        reader.open()
        print_video_information(reader)

        pipeline = initialize_pipeline(config_path=args.config)
        print_pipeline_information(pipeline)

        statistics = BenchmarkStatistics()
        first_saved = False

        for _ in range(args.frames):
            success, frame = reader.read()

            if not success or frame is None:
                break

            frame_index = reader.current_frame_index - 1

            detection_result = detect_faces(
                detector=pipeline.detector,
                frame=frame,
            )

            statistics.add(detection_result)

            print_frame_detection_information(
                frame_index=frame_index,
                result=detection_result,
            )

            if not first_saved:
                save_debug_image(
                    frame=frame,
                    detections=detection_result.detections,
                    output_path=DEBUG_IMAGE_PATH,
                )
                print_debug_image_information(DEBUG_IMAGE_PATH)
                first_saved = True

        if statistics.frames_tested == 0:
            raise RuntimeError("No video frames were available for benchmarking.")

        print_benchmark_summary(statistics)

    except (
        FileNotFoundError,
        RuntimeError,
        TypeError,
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
