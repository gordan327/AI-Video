import argparse

from ai_video.config_manager import ConfigManager
from ai_video.processor import VideoProcessor
from ai_video.version import (
    __build__,
    __codename__,
    __version__,
)


def print_version():
    """顯示目前 AI-Video 版本。"""

    print(f"AI-Video {__version__}")

def create_parser():
    """建立命令列參數解析器。"""

    parser = argparse.ArgumentParser(
        prog="ai-video",
        description=(
            "Privacy-first AI Video Framework"
        ),
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information.",
    )

    parser.add_argument(
        "--config",
        help="Path to a YAML configuration file.",
    )

    return parser

def main():
    parser = create_parser()

    args = parser.parse_args()

    if args.version:
        print_version()
        return

    config = ConfigManager(args.config)

    processor = VideoProcessor(config)

    processor.run()


if __name__ == "__main__":
    main()