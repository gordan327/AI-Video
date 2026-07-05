import cv2

from ai_video.video_reader import VideoReader
from ai_video.video_writer import VideoWriter
from ai_video.ffmpeg_processor import FFmpegProcessor
from ai_video.logger import Logger
from ai_video.dummy_face_detector import DummyFaceDetector


class VideoProcessor:
    """影片處理流程控制器"""

    def __init__(self, video_path: str):

        self.video_path = video_path

        self.ffmpeg = FFmpegProcessor()

        self.reader = VideoReader(video_path)

        # 建立 Dummy Face Detector
        self.detector = DummyFaceDetector()

    def run(self):

        self.reader.open()

        self.writer = VideoWriter(
            output_path="output/temp_video.mp4",
            fps=self.reader.fps,
            width=self.reader.width,
            height=self.reader.height,
        )

        self.writer.open()

        Logger.info("開始處理影片...")

        frame_index = 0

        while True:

            success, frame = self.reader.read()

            if not success:
                break

            frame = self.process_frame(frame)

            self.writer.write(frame)

            frame_index += 1

        self.reader.close()
        self.writer.close()

        Logger.info("正在合併音訊...")

        self.ffmpeg.merge_audio(
            original_video=self.video_path,
            processed_video="output/temp_video.mp4",
            output_video="output/output.mp4",
        )

        Logger.success("音訊合併完成。")
        Logger.success(f"完成，共處理 {frame_index} 個 Frame。")

    def process_frame(self, frame):

        faces = self.detector.detect(frame)

        for face in faces:

            cv2.rectangle(
                frame,
                (face.x1, face.y1),
                (face.x2, face.y2),
                (0, 255, 0),
                3,
            )

        return frame