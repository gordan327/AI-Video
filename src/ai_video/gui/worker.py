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
        temp_output_path = None
        try:
            # 確保安全取得設定路徑，避免 NoneType 錯誤
            raw_input = self.config.get("job.input_path")
            raw_output = self.config.get("job.output_path")
            raw_temp = self.config.get("job.temp_output_path")

            if not raw_input or not raw_output:
                raise ValueError("未設定有效的輸入或輸出影片路徑。")

            input_path = Path(raw_input)
            output_path = Path(raw_output)
            # 若 temp 為空，則產生預設臨時路徑
            temp_output_path = Path(raw_temp) if raw_temp else output_path.with_suffix(".tmp.mp4")

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

                # 處理影像 (預留給後續整合處理邏輯)
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

            # 3. 清理暫存檔 (加入嚴格檢查以避免 PermissionError)
            if temp_output_path and temp_output_path.is_file():
                try:
                    temp_output_path.unlink()
                except OSError as e:
                    logger.warning(f"無法刪除暫存檔，但處理已完成: {e}")

            self.progress.emit(100)
            self.status_changed.emit("影片處理完成")
            self.finished.emit(str(output_path))

        except InterruptedError:
            logger.warning("影片處理工作已被使用者停止")
            if temp_output_path and isinstance(temp_output_path, Path) and temp_output_path.is_file():
                temp_output_path.unlink()
            self.cancelled.emit()

        except Exception as error:
            error_trace = traceback.format_exc()
            logger.error(f"Worker 處理失敗:\n{error_trace}")
            
            # 安全清理邏輯
            if temp_output_path and isinstance(temp_output_path, Path) and temp_output_path.is_file():
                try:
                    temp_output_path.unlink()
                except OSError:
                    pass # 忽略清理過程的權限錯誤

            self.failed.emit(f"處理失敗: {str(error)}")


# 相容性別名
Worker = VideoWorker