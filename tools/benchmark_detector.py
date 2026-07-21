#!/usr/bin/env python3
"""
AI-Video Detector Benchmark Tool

This tool benchmarks different detector configurations.
Future versions will compare detection quality and speed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from ai_video.config_manager import ConfigManager
from ai_video.detector.detector_factory import DetectorFactory
from ai_video.model_manager import ModelManager
from ai_video.video.video_reader import VideoReader


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

    return parser


def main() -> int:
    """Run the detector benchmark tool."""

    parser = create_parser()
    args = parser.parse_args()

    print("=" * 50)
    print("AI-Video Detector Benchmark")
    print("Version 0.1")
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

        faces = detector.detect(frame)

        print()
        print("Detection Result")
        print("----------------")
        print(f"Faces detected : {len(faces)}")

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