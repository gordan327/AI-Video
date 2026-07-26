import os
import subprocess
import sys
from pathlib import Path


class FFmpegProcessor:
    """FFmpeg 相關影片處理。"""

    @staticmethod
    def _get_ffmpeg_command() -> str:
        """取得 FFmpeg 執行檔位置。

        發行版會優先使用 AI-Video 主程式旁邊隨附的
        ffmpeg 執行檔；開發環境則退回使用系統 PATH。
        """

        executable_name = (
            "ffmpeg.exe"
            if os.name == "nt"
            else "ffmpeg"
        )

        application_directory = (
            Path(sys.executable).resolve().parent
        )

        bundled_candidates = [
            application_directory / executable_name,
            application_directory / "bin" / executable_name,
        ]

        for candidate in bundled_candidates:
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
                "請確認 AI-Video 發行資料夾內包含 "
                "ffmpeg.exe，或已將 FFmpeg 加入系統 PATH。"
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
                f"{details}"
            ) from error