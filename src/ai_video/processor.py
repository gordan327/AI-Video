from pathlib import Path
from time import perf_counter

from tqdm import tqdm

from ai_video.tracker.tracker_factory import (
    TrackerFactory,
)
from ai_video.face_renderer import FaceRenderer
from ai_video.model_manager import ModelManager
from ai_video.processing_stats import ProcessingStats
from ai_video.processing.frame_processor import (
    FrameProcessor,
)
from ai_video.logger import Logger
from ai_video.detector.detector_factory import DetectorFactory
from ai_video.video.ffmpeg_processor import (
    FFmpegProcessor,
)
from ai_video.video.video_reader import (
    VideoReader,
)
from ai_video.video.video_writer import (
    VideoWriter,
)


class VideoProcessor:
    """影片處理流程控制器與模組效能統計器。"""

    def __init__(
        self,
        config,
        progress_callback=None,
        status_callback=None,
        stats_callback=None,
        stop_checker=None,
    ):
        self.config = config

        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.stats_callback = stats_callback
        self.stop_checker = stop_checker

        self.reader = VideoReader(
            self.config.get("video.input")
        )

        self.writer = None

        self.model_manager = ModelManager(self.config)

        self.detector = DetectorFactory.create(
            detector_type=self.config.get(
                "detector.type",
                "scrfd",
            ),
            model_manager=self.model_manager,
            config=self.config,
        )

        self.tracker = TrackerFactory.create(
            tracker_type=self.config.get(
                "tracker.type",
                "bytetrack",
            ),
            privacy_hold_frames=self.config.get(
                "tracker.privacy_hold_frames",
                15,
            ),
            prediction_frames=self.config.get(
                "tracker.prediction_frames",
                3,
            ),
            freeze_expansion_per_frame=self.config.get(
                "tracker.freeze_expansion_per_frame",
                0.03,
            ),
        )

        self.renderer = FaceRenderer(
            renderer_type=self.config.get(
                "renderer.type",
                "blur",
            ),
            blur_strength=self.config.get(
                "renderer.blur_strength",
                51,
            ),
            pixel_size=self.config.get(
                "renderer.pixel_size",
                12,
            ),            
            padding_ratio=self.config.get(
                "renderer.padding_ratio",
                0.35,
            ),
            temporal_hold_frames=self.config.get(
                "renderer.temporal_hold_frames",
                5,
            ),
        )
        
        self.frame_processor = FrameProcessor(
            detector=self.detector,
            tracker=self.tracker,
            renderer=self.renderer,
        )

        self.ffmpeg = FFmpegProcessor()

        self.detector_time = 0.0
        self.tracker_time = 0.0
        self.renderer_time = 0.0
        self.writer_time = 0.0

        self.current_faces = []

    def report_progress(self, value: int):
        """將處理進度回報給 GUI。"""

        if self.progress_callback is not None:
            self.progress_callback(value)

    def report_status(self, message: str):
        """將目前狀態回報給 GUI。"""

        if self.status_callback is not None:
            self.status_callback(message)

    def report_stats(self, stats: ProcessingStats):
        """將即時處理統計資料回報給呼叫端。"""

        if self.stats_callback is not None:
            self.stats_callback(stats)

    def stop_requested(self) -> bool:
        """檢查使用者是否要求停止。"""

        if self.stop_checker is None:
            return False

        return bool(self.stop_checker())

    def run(self) -> bool:
        """
        執行完整影片處理流程。

        Returns:
            True：影片處理完成。
            False：使用者中途停止。
        """

        self.report_status("正在開啟影片……")
        self.report_progress(0)

        self.reader.open()

        temp_output = self.config.get("video.temp_output")
        final_output = self.config.get("video.output")

        if not temp_output:
            raise ValueError("尚未設定暫存影片路徑 video.temp_output")

        if not final_output:
            raise ValueError("尚未設定輸出影片路徑 video.output")

        temp_path = Path(temp_output)
        final_path = Path(final_output)

        temp_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        final_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.writer = VideoWriter(
            output_path=str(temp_path),
            fps=self.reader.fps,
            width=self.reader.width,
            height=self.reader.height,
        )

        self.writer.open()

        total_frames = self.get_total_frames()

        Logger.info("開始處理影片")

        self.report_status(
            "正在偵測及模糊影片中的人臉……"
        )

        frame_index = 0
        processing_start = perf_counter()
        was_stopped = False

        progress_bar = tqdm(
            total=total_frames if total_frames > 0 else None,
            desc="處理進度",
            unit="frame",
            dynamic_ncols=True,
        )

        try:
            while True:
                if self.stop_requested():
                    was_stopped = True

                    self.report_status(
                        "正在停止處理……"
                    )

                    break

                success, frame = self.reader.read()

                if not success:
                    break

                frame = self.process_frame(frame)

                writer_start = perf_counter()

                self.writer.write(frame)

                self.writer_time += (
                    perf_counter() - writer_start
                )

                frame_index += 1

                elapsed_time = (
                    perf_counter() - processing_start
                )

                current_fps = (
                    frame_index / elapsed_time
                    if elapsed_time > 0
                    else 0.0
                )

                progress_bar.set_postfix(
                    fps=f"{current_fps:.2f}",
                    faces=len(self.current_faces),
                )

                progress_bar.update(1)

                if total_frames > 0:
                    percentage = int(
                        frame_index
                        / total_frames
                        * 100
                    )

                    remaining_frames = max(
                        0,
                        total_frames - frame_index,
                    )

                    eta_seconds = (
                        remaining_frames / current_fps
                        if current_fps > 0
                        else 0.0
                    )

                    stats = ProcessingStats(
                        progress=min(percentage, 99),
                        frame_index=frame_index,
                        total_frames=total_frames,
                        fps=current_fps,
                        faces=len(self.current_faces),
                        elapsed_seconds=elapsed_time,
                        eta_seconds=eta_seconds,
                    )

                    self.report_progress(
                        stats.progress
                    )

                    self.report_stats(stats)

                    self.report_status(
                        f"正在處理第 "
                        f"{frame_index:,} / "
                        f"{total_frames:,} 個影格，"
                        f"速度 {current_fps:.2f} FPS"
                    )

                else:
                    stats = ProcessingStats(
                        progress=0,
                        frame_index=frame_index,
                        total_frames=0,
                        fps=current_fps,
                        faces=len(self.current_faces),
                        elapsed_seconds=elapsed_time,
                        eta_seconds=0.0,
                    )

                    self.report_stats(stats)

                    self.report_status(
                        f"已處理 {frame_index:,} 個影格，"
                        f"速度 {current_fps:.2f} FPS"
                    )

        finally:
            progress_bar.close()

            self.reader.close()

            if self.writer is not None:
                self.writer.close()

        processing_time = (
            perf_counter() - processing_start
        )

        if was_stopped:
            self.report_status("影片處理已停止")
            self.report_progress(0)

            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass

            return False

        self.report_status(
            "影像處理完成，正在合併原始音訊……"
        )

        Logger.info("正在合併音訊")

        self.ffmpeg.merge_audio(
            original_video=self.config.get(
                "video.input"
            ),
            processed_video=str(temp_path),
            output_video=str(final_path),
        )

        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass

        self.report_progress(100)
        self.report_status("影片處理完成")

        Logger.success(
            f"完成，共處理 "
            f"{frame_index} 個 Frame。"
        )

        self.print_performance_report(
            frame_count=frame_index,
            processing_time=processing_time,
        )

        return True

    def get_total_frames(self) -> int:
        """取得影片總影格數，並相容不同欄位名稱。"""

        possible_names = (
            "frame_count",
            "total_frames",
            "frames",
        )

        for name in possible_names:
            value = getattr(
                self.reader,
                name,
                None,
            )

            if value is not None:
                try:
                    return int(value)
                except (TypeError, ValueError):
                    continue

        return 0

    def process_frame(self, frame):
        """委派 FrameProcessor 處理影格並累加模組耗時。"""

        frame, faces = self.frame_processor.process(
            frame
        )

        self.detector_time += (
            self.frame_processor.detector_time
        )
        self.tracker_time += (
            self.frame_processor.tracker_time
        )
        self.renderer_time += (
            self.frame_processor.renderer_time
        )

        self.current_faces = faces

        return frame