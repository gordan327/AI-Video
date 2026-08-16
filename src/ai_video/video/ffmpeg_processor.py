import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


class FFmpegProcessor:
    """FFmpeg 相關影片處理。"""

    @staticmethod
    def _get_ffmpeg_command() -> str:
        """強制直接使用安裝目錄下的 ffmpeg.exe 或系統 PATH"""
        executable_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
        
        if getattr(sys, "frozen", False) or "__compiled__" in globals():
            exe_dir = Path(sys.executable).resolve().parent
            
            # 1. 檢查同層目錄
            local_ffmpeg = exe_dir / executable_name
            if local_ffmpeg.is_file():
                return str(local_ffmpeg)
                
            # 2. 檢查常見的子目錄或上一層結構（例如打包在根目錄或 lib 資料夾旁）
            alternative_paths = [
                exe_dir / "lib" / "ffmpeg" / executable_name,
                exe_dir.parent / executable_name,
                exe_dir.parent / "lib" / "ffmpeg" / executable_name,
            ]
            for path in alternative_paths:
                if path.is_file():
                    return str(path)

        # 3. 嘗試從系統環境變數中尋找
        system_ffmpeg = shutil.which("ffmpeg")
        if system_ffmpeg:
            return system_ffmpeg

        # 4. 若皆找不到，回傳預設字串讓系統嘗試呼叫
        return executable_name

    def merge_audio(
        self,
        original_video: str,
        processed_video: str,
        output_video: str,
    ) -> None:
        """將原始影片的音訊合併到處理後的影片。"""

        original_path = Path(original_video)
        processed_path = Path(processed_video)
        output_path = Path(output_video)

        ffmpeg_command = self._get_ffmpeg_command()
        logger.info(f"開始執行音訊合併，使用 FFmpeg 指令路徑: {ffmpeg_command}")

        command = [
            ffmpeg_command,
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(processed_path),
            "-i",
            str(original_path),
            "-c:v",
            "copy",
            "-map",
            "0:v",
            "-map",
            "1:a?",
            "-c:a",
            "aac",
            str(output_path),
        ]

        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
            logger.info("音訊合併完成！")

        except FileNotFoundError as error:
            err_msg = (
                f"找不到 FFmpeg 執行檔。\n"
                f"嘗試呼叫路徑：'{ffmpeg_command}'\n"
                f"請確認安裝目錄內包含 {os.path.basename(ffmpeg_command)}"
            )
            logger.error(err_msg)
            raise RuntimeError(err_msg) from error

        except subprocess.CalledProcessError as error:
            stderr = (error.stderr or "").strip()
            stdout = (error.stdout or "").strip()
            details = stderr or stdout or "FFmpeg 未提供詳細錯誤訊息。"
            
            err_msg = (
                f"FFmpeg 合併音訊失敗 (Exit Code: {error.returncode})\n"
                f"執行指令：{' '.join(command)}\n"
                f"錯誤細節：{details}"
            )
            logger.error(err_msg)
            raise RuntimeError(err_msg) from error