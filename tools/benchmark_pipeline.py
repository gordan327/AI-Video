#!/usr/bin/env python3
"""
AI-Video Pipeline Benchmark Tool.

Version 0.2 initializes the video reader, all main pipeline components,
and verifies that the first video frame can be read successfully.
"""

from __future__ import annotations

import argparse
import sys
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


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="Initialize the AI-Video processing pipeline.",
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
    print("Version 0.2")
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


def print_first_frame_information(
    reader: VideoReader,
    frame: Any,
) -> None:
    """Print information about the first frame."""

    print()
    print("First Frame")
    print("-----------")
    print(f"Frame Index : {reader.current_frame_index - 1}")
    print(f"Shape       : {frame.shape}")
    print(f"Data Type   : {frame.dtype}")


def main() -> int:
    """Run pipeline initialization verification."""

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

        success, frame = reader.read()

        if not success:
            raise RuntimeError(
                "Unable to read the first frame."
            )

        print_first_frame_information(
            reader,
            frame,
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