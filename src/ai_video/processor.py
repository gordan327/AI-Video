from ai_video.video_reader import VideoReader


class VideoProcessor:
    """影片處理流程控制器"""

    def __init__(self, video_path: str):

        self.reader = VideoReader(video_path)

    def run(self):

        self.reader.open()

        print("開始處理影片...")

        frame_index = 0

        while True:

            success, frame = self.reader.read()

            if not success:
                break

            frame = self.process_frame(frame)

            frame_index += 1

        self.reader.close()

        print(f"完成，共處理 {frame_index} 個 Frame。")

    def process_frame(self, frame):
        """
        處理單一影格。

        後續版本將在此加入：
        - 人臉偵測（Face Detection）
        - 人臉追蹤（Face Tracking）
        - 人臉模糊（Face Blur）
        """

        return frame