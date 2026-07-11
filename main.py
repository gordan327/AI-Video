from ai_video.processor import VideoProcessor
from ai_video.config_manager import ConfigManager


def main():

    config = ConfigManager()

    processor = VideoProcessor(config)

    processor.run()


if __name__ == "__main__":
    main()