from ai_video.processor import VideoProcessor


def main():

    processor = VideoProcessor("videos/demo.mp4")

    processor.run()


if __name__ == "__main__":
    main()