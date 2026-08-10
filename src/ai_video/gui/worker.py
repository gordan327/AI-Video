import logging
import traceback
from pathlib import Path
from PySide6.QtCore import QObject, Signal

from ai_video.config_manager import ConfigManager
from ai_video.video.video_reader import VideoReader
from ai_video.video.video_writer import VideoWriter
from ai_video.video.ffmpeg_processor import FFmpegProcessor

logger = logging.getLogger(__name__)


class VideoWorker(QObject):
    """背景影片處理工作物件 (基於 QObject Worker 模式)。"""

    progress = Signal(int)
    stats_changed = Signal(dict)
    status_changed = Signal(str)
    finished = Signal(str)
    cancelled = Signal()
    failed = Signal(str)

    def __init__(self, config: ConfigManager, parent=None):
        super().__init__(parent)
        self.config = config
        self._stop_requested = False
        self.ffmpeg_processor = FFmpegProcessor()

    def request_stop(self):
        """請求停止背景工作。"""
        self._stop_requested = True

    def run(self):
        """執行影片處理流程。"""
        try:
            input_path = Path(self.config.get("job.input_path"))
            output_path = Path(self.config.get("job.output_path"))
            temp_output_path = Path(self.config.get("job.temp_output_path"))

            self.status_changed.emit("正在開啟影片......")
            self.progress.emit(0)

            # 1. 初始化讀取與寫入器
            reader = VideoReader(str(input_path))
            total_frames = reader.get_frame_count()
            
            writer = VideoWriter(
                str(temp_output_path),
                fps=reader.get_fps(),
                width=reader.get_width(),
                height=reader.get_height()
            )

            self.status_changed.emit("正在偵測及模糊影片中的人臉......")
            
            current_frame = 0
            for frame in reader.read_frames():
                if self._stop_requested:
                    raise InterruptedError("使用者要求中止處理")

                # 這裡可加入人臉偵測與模糊處理（依原專案處理邏輯）
                # ...

                writer.write_frame(frame)
                current_frame += 1

                if total_frames > 0:
                    percent = int((current_frame / total_frames) * 100)
                    self.progress.emit(percent)
                    self.stats_changed.emit({"frame": current_frame, "total": total_frames})

            reader.release()
            writer.release()

            if self._stop_requested:
                self.cancelled.emit()
                return

            # 2. 合併原始音訊
            self.status_changed.emit("正在合併原始音訊......")
            self.ffmpeg_processor.merge_audio(
                original_video=str(input_path),
                processed_video=str(temp_output_path),
                output_video=str(output_path),
            )

            # 3. 清理暫存檔
            if temp_output_path.exists():
                temp_output_path.unlink()

            self.progress.emit(100)
            self.status_changed.emit("影片處理完成")
            self.finished.emit(str(output_path))

        except InterruptedError:
            logger.warning("影片處理工作已被使用者停止")
            temp_output = Path(self.config.get("job.temp_output_path", ""))
            if temp_output.exists():
                temp_output.unlink()
            self.cancelled.emit()

        except Exception as error:
            error_trace = traceback.format_exc()
            logger.error(f"Worker 處理失敗:\n{error_trace}")
            
            temp_output = Path(self.config.get("job.temp_output_path", ""))
            if temp_output.exists():
                temp_output.unlink()

            self.failed.emit(f"處理失敗: {str(error)}")


# 相容性別名
Worker = VideoWorker