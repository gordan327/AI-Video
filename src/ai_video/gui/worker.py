import logging
import traceback
from pathlib import Path
from PySide6.QtCore import QObject, Signal

from ai_video.video.video_reader import VideoReader
from ai_video.video.video_writer import VideoWriter
from ai_video.video.ffmpeg_processor import FFmpegProcessor

logger = logging.getLogger(__name__)


class VideoWorker(QObject):
    """背景影片處理工作物件。"""

    progress = Signal(int)
    stats_changed = Signal(dict)
    status_changed = Signal(str)
    finished = Signal(str)
    cancelled = Signal()
    failed = Signal(str)

    def __init__(self, input_path: str, output_path: str, temp_output_path: str = None, parent=None):
        super().__init__(parent)
        self.input_path_str = input_path
        self.output_path_str = output_path
        self.temp_output_path_str = temp_output_path
        self._stop_requested = False
        self.ffmpeg_processor = FFmpegProcessor()

    def request_stop(self):
        """請求停止背景工作。"""
        self._stop_requested = True

    def run(self):
        """執行影片處理流程。"""
        temp_output_path = None
        try:
            if not self.input_path_str or not self.output_path_str:
                raise ValueError("未設定有效的輸入或輸出影片路徑。")

            input_path = Path(self.input_path_str)
            output_path = Path(self.output_path_str)
            temp_output_path = Path(self.temp_output_path_str) if self.temp_output_path_str else output_path.with_suffix(".tmp.mp4")

            self.status_changed.emit("正在開啟影片......")
            self.progress.emit(0)

            # 1. 初始化讀取與寫入器
            reader = VideoReader(str(input_path))
            total_frames = getattr(reader, "frame_count", 0)
            fps = getattr(reader, "fps", 30)
            width = getattr(reader, "width", 1920)
            height = getattr(reader, "height", 1080)
            
            writer = VideoWriter(
                str(temp_output_path),
                fps=fps,
                width=width,
                height=height
            )

            self.status_changed.emit("正在偵測及模糊影片中的人臉......")
            
            current_frame = 0
            
            # 安全取得畫面迴圈（相容各種實作方式）
            frames_iterator = None
            if hasattr(reader, "read_frames"):
                frames_iterator = reader.read_frames()
            elif hasattr(reader, "__iter__"):
                frames_iterator = iter(reader)
            else:
                # 如果 reader 本身可疊代
                frames_iterator = reader

            for frame in frames_iterator:
                if self._stop_requested:
                    raise InterruptedError("使用者要求中止處理")

                writer.write_frame(frame)
                current_frame += 1

                if total_frames > 0:
                    percent = int((current_frame / total_frames) * 100)
                    self.progress.emit(percent)
                    self.stats_changed.emit({"frame": current_frame, "total": total_frames})

            if hasattr(reader, "release"):
                reader.release()
            if hasattr(writer, "release"):
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
            if temp_output_path and temp_output_path.is_file():
                try:
                    temp_output_path.unlink()
                except OSError:
                    pass

            self.progress.emit(100)
            self.status_changed.emit("影片處理完成")
            self.finished.emit(str(output_path))

        except InterruptedError:
            logger.warning("影片處理工作已被使用者停止")
            if temp_output_path and isinstance(temp_output_path, Path) and temp_output_path.is_file():
                try:
                    temp_output_path.unlink()
                except OSError:
                    pass
            self.cancelled.emit()

        except Exception as error:
            error_trace = traceback.format_exc()
            logger.error(f"Worker 處理失敗:\n{error_trace}")
            
            if temp_output_path and isinstance(temp_output_path, Path) and temp_output_path.is_file():
                try:
                    temp_output_path.unlink()
                except OSError:
                    pass

            self.failed.emit(f"處理失敗: {str(error)}")


# 相容性別名
Worker = VideoWorker