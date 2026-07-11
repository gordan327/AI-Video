import cv2

from ai_video.video_reader import VideoReader
from ai_video.video_writer import VideoWriter
from ai_video.ffmpeg_processor import FFmpegProcessor

from ai_video.scrfd_face_detector import SCRFDFaceDetector
from ai_video.bytetrack_face_tracker import ByteTrackFaceTracker
from ai_video.face_renderer import FaceRenderer

from ai_video.model_manager import ModelManager

class VideoProcessor:
    """影片處理流程控制器"""

    def __init__(self, config):

        self.config = config

        self.reader = VideoReader(
            self.config.get("video.input")
        )

        self.writer = None

        self.model_manager = ModelManager(self.config)

        self.detector = SCRFDFaceDetector(
            self.model_manager,
            self.config,
        )

        self.tracker = ByteTrackFaceTracker()

        self.renderer = FaceRenderer()

        self.ffmpeg = FFmpegProcessor()

    def run(self):

        self.reader.open()

        self.writer = VideoWriter(
            output_path=self.config.get("video.temp_output"),
            fps=self.reader.fps,
            width=self.reader.width,
            height=self.reader.height,
        )

        self.writer.open()

        print("開始處理影片...")

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

        print("正在合併音訊...")

        self.ffmpeg.merge_audio(
            original_video=self.config.get("video.input"),
            processed_video=self.config.get("video.temp_output"),
            output_video=self.config.get("video.output"),
        )

        print(f"完成，共處理 {frame_index} 個 Frame。")

    def process_frame(self, frame):

        faces = self.detector.detect(frame)

        faces = self.tracker.track(faces)

        frame = self.renderer.draw(frame, faces)

        return frame