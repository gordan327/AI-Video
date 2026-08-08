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
        """取得 FFmpeg 執行檔位置。"""

        executable_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"

        # 1. Nuitka / PyInstaller 打包環境 (sys.executable 所在目錄)
        if getattr(sys, "frozen", False) or "__compiled__" in globals():
            exe_dir = Path(sys.executable).resolve().parent
            candidates = [
                exe_dir / executable_name,
                exe_dir / "bin" / executable_name,
                exe_dir / "_internal" / executable_name,
            ]
            for cand in candidates:
                if cand.is_file():
                    logger.info(f"找到打包隨附之 FFmpeg: {cand}")
                    return str(cand)

        # 2. 檢查當前工作目錄 (CWD)
        cwd_cand = Path.cwd() / executable_name
        if cwd_cand.is_file():
            logger.info(f"於工作目錄找到 FFmpeg: {cwd_cand}")
            return str(cwd_cand)

        # 3. 檢查系統環境變數 PATH
        system_ffmpeg = shutil.which("ffmpeg")
        if system_ffmpeg:
            logger.info(f"於系統 PATH 找到 FFmpeg: {system_ffmpeg}")
            return system_ffmpeg

        # 4. 開發環境相對路徑 fallback
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        dev_cand = base_dir / "lib" / "ffmpeg" / "tools" / "ffmpeg" / "bin" / executable_name
        if dev_cand.is_file():
            logger.info(f"於開發路徑找到 FFmpeg: {dev_cand}")
            return str(dev_cand)

        logger.warning("未找到任何實體 FFmpeg 檔案，將嘗試直接呼叫 'ffmpeg'")
        return "ffmpeg"

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