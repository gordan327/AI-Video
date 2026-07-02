from ai_video.video_reader import VideoReader


def main():

    reader = VideoReader("videos/demo.mp4")

    reader.open()

    print("=" * 40)
    print("Video Information")
    print("=" * 40)

    print(f"FPS        : {reader.fps:.2f}")
    print(f"Width      : {reader.width}")
    print(f"Height     : {reader.height}")
    print(f"Frames     : {reader.frame_count}")
    print(f"Duration   : {reader.duration:.2f} sec")

    reader.close()


if __name__ == "__main__":
    main()