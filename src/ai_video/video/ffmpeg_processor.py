import os
import shutil
import subprocess
import sys
from pathlib import Path


class FFmpegProcessor:
    """FFmpeg 相關影片處理。"""

    @staticmethod
    def _get_ffmpeg_command() -> str:
        """取得 FFmpeg 執行檔位置。

        優先順序：
        1. 應用程式目錄下隨附的 ffmpeg（打包發行版）
        2. 系統 PATH 中的 ffmpeg
        3. 專案開發環境相對路徑下的 ffmpeg
        """

        executable_name = (
            "ffmpeg.exe"
            if os.name == "nt"
            else "ffmpeg"
        )

        # 1. 檢查應用程式發行目錄（Nuitka 打包目錄）
        if getattr(sys, "frozen", False) or "__compiled__" in globals():
            application_directory = Path(sys.executable).resolve().parent
            bundled_candidates = [
                application_directory / executable_name,
                application_directory / "bin" / executable_name,
            ]

            for candidate in bundled_candidates:
                if candidate.is_file():
                    return str(candidate)

        # 2. 檢查系統環境變數 (PATH)
        system_ffmpeg = shutil.which("ffmpeg")
        if system_ffmpeg:
            return system_ffmpeg

        # 3. 檢查專案開發環境相對路徑 (Fallback)
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        dev_candidates = [
            base_dir / "lib" / "ffmpeg" / "tools" / "ffmpeg" / "bin" / executable_name,
            base_dir / "bin" / executable_name,
        ]

        for candidate in dev_candidates:
            if candidate.is_file():
                return str(candidate)

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
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )

        except FileNotFoundError as error:
            raise RuntimeError(
                "找不到 FFmpeg。\n\n"
                f"嘗試執行的指令為：'{ffmpeg_command}'\n"
                "請確認 AI-Video 發行資料夾內包含 "
                "ffmpeg 執行檔，或已將 FFmpeg 加入系統 PATH。"
            ) from error

        except subprocess.CalledProcessError as error:
            stderr = (error.stderr or "").strip()
            stdout = (error.stdout or "").strip()

            details = (
                stderr
                or stdout
                or "FFmpeg 未提供詳細錯誤訊息。"
            )

            raise RuntimeError(
                "FFmpeg 合併音訊失敗。\n\n"
                f"執行指令：{' '.join(command)}\n"
                f"錯誤細節：{details}"
            ) from error