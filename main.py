from ai_video.config_manager import ConfigManager
from ai_video.processor import VideoProcessor
from ai_video.version import __build__, __codename__, __version__


def print_version():
    """顯示目前 AI-Video 版本。"""

    print("=" * 50)
    print(f"AI-Video {__version__}")
    print(f"Build    : {__build__}")
    print(f"Codename : {__codename__}")
    print("=" * 50)


def main():
    """AI-Video 主程式入口。"""

    print_version()

    config = ConfigManager()

    processor = VideoProcessor(config)

    processor.run()


if __name__ == "__main__":
    main()