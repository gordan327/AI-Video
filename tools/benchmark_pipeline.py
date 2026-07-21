#!/usr/bin/env python3
"""
AI-Video Pipeline Benchmark Tool.

Version 0.4A initializes the main pipeline components, reads the first
video frame, measures face detection performance, and saves a debug
image with detected face bounding boxes.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
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
    """Store first-frame face detection results."""

    detections: Any
    elapsed_seconds: float


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Initialize the AI-Video pipeline, benchmark face detection "
            "on the first video frame, and save a debug image."
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

    return parser


def print_header() -> None:
    """Print the benchmark header."""

    print("=" * 50)
    print("AI-Video Pipeline Benchmark")
    print("Version 0.4A")
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


def initialize_pipeline(
    config_path: Path | None,
) -> PipelineComponents:
    """Initialize all primary AI-Video pipeline components."""

    config = ConfigManager(config_path=config_path)

    detector_type = config.get(
        "detector.type",
        "scrfd",
    )
    tracker_type = config.get(
        "tracker.type",
        "bytetrack",
    )
    renderer_type = config.get(
        "renderer.type",
        "blur",
    )

    model_manager = ModelManager(config)

    detector = DetectorFactory.create(
        detector_type=detector_type,
        model_manager=model_manager,
        config=config,
    )

    tracker = TrackerFactory.create(
        tracker_type=tracker_type,
        privacy_hold_frames=config.get(
            "tracker.privacy_hold_frames",
            15,
        ),
        prediction_frames=config.get(
            "tracker.prediction_frames",
            3,
        ),
        freeze_expansion_per_frame=config.get(
            "tracker.freeze_expansion_per_frame",
            0.03,
        ),
    )

    renderer = RendererFactory.create(
        renderer_type=renderer_type,
        blur_strength=config.get(
            "renderer.blur_strength",
            51,
        ),
        pixel_size=config.get(
            "renderer.pixel_size",
            12,
        ),
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


def print_pipeline_information(
    pipeline: PipelineComponents,
) -> None:
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


def read_first_frame(
    reader: VideoReader,
) -> Any:
    """Read the first frame from the video."""

    success, frame = reader.read()

    if not success or frame is None:
        raise RuntimeError(
            "Unable to read the first frame."
        )

    return frame


def print_first_frame_information(
    reader: VideoReader,
    frame: Any,
) -> None:
    """Print information about the first frame."""

    frame_index = reader.current_frame_index - 1

    print()
    print("First Frame")
    print("-----------")
    print(f"Frame Index : {frame_index}")
    print(f"Shape       : {frame.shape}")
    print(f"Data Type   : {frame.dtype}")


def detect_faces(
    detector: Any,
    frame: Any,
) -> DetectionResult:
    """Detect faces in one frame and measure elapsed time."""

    started_at = perf_counter()

    detections = detector.detect(frame)

    elapsed_seconds = perf_counter() - started_at

    if detections is None:
        raise RuntimeError(
            "The detector returned no detection result."
        )

    return DetectionResult(
        detections=detections,
        elapsed_seconds=elapsed_seconds,
    )


def print_detection_information(
    result: DetectionResult,
) -> None:
    """Print first-frame face detection information."""

    detection_count = len(result.detections)
    elapsed_milliseconds = result.elapsed_seconds * 1000.0

    print()
    print("Face Detection")
    print("--------------")
    print(f"Faces Found : {detection_count}")
    print(f"Elapsed     : {elapsed_milliseconds:.2f} ms")


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

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    saved = cv2.imwrite(
        str(output_path),
        debug_frame,
    )

    if not saved:
        raise RuntimeError(
            f"Unable to save debug image: {output_path}"
        )


def print_debug_image_information(
    output_path: Path,
) -> None:
    """Print debug image output information."""

    print()
    print("Debug Image")
    print("-----------")
    print(f"Output : {output_path}")


def main() -> int:
    """Benchmark first-frame detection and save a debug image."""

    parser = create_parser()
    args = parser.parse_args()

    print_header()

    print()
    print(f"Input video : {args.video}")

    reader = VideoReader(str(args.video))

    try:
        reader.open()

        print_video_information(reader)

        pipeline = initialize_pipeline(
            config_path=args.config,
        )

        print_pipeline_information(pipeline)

        frame = read_first_frame(reader)

        print_first_frame_information(
            reader,
            frame,
        )

        detection_result = detect_faces(
            detector=pipeline.detector,
            frame=frame,
        )

        print_detection_information(
            detection_result,
        )

        save_debug_image(
            frame=frame,
            detections=detection_result.detections,
            output_path=DEBUG_IMAGE_PATH,
        )

        print_debug_image_information(
            DEBUG_IMAGE_PATH,
        )

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