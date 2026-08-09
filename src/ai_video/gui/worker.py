import logging
import traceback
from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)


class VideoWorker(QThread):
    # 定義日誌與完成信號
    log_signal = Signal(str)
    finished_signal = Signal(bool, str)

    def run(self):
        try:
            self.log_signal.emit("背景影片處理工作已啟動")
            self.log_signal.emit("正在開啟影片......")
            self.log_signal.emit("開始處理影片")
            self.log_signal.emit("正在偵測及模糊影片中的人臉......")

            # 1. 執行人臉處理 (已成功)
            # ... (您的影像處理邏輯) ...

            self.log_signal.emit("影像處理完成，正在合併原始音訊......")

            # 2. 執行音訊合併
            self.processor.merge_audio(
                original_video=self.input_path,
                processed_video=self.temp_video_path,
                output_video=self.output_path,
            )

            self.log_signal.emit("影片處理成功完成！")
            self.finished_signal.emit(True, "處理完成")

        except Exception as error:
            # 捕獲所有詳細錯誤訊息，強制印到 UI Log 畫面
            error_trace = traceback.format_exc()
            logger.error(f"Worker 處理失敗: {error_trace}")

            error_msg = f"[ERROR] 處理過程發生錯誤：\n{str(error)}"
            self.log_signal.emit(error_msg)
            self.finished_signal.emit(False, str(error))

# 相容性設定：允許透過 Worker 或 VideoWorker 匯入
Worker = VideoWorker