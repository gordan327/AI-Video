import subprocess
from pathlib import Path


class FFmpegProcessor:
    """FFmpeg 相關影片處理。"""

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

        command = [
            "ffmpeg",
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
                "找不到 FFmpeg。請確認 FFmpeg 已正確安裝，"
                "而且可從終端機執行。"
            ) from error

        except subprocess.CalledProcessError as error:
            stderr = (error.stderr or "").strip()
            stdout = (error.stdout or "").strip()

            details = stderr or stdout or "FFmpeg 未提供詳細錯誤訊息。"

            raise RuntimeError(
                "FFmpeg 合併音訊失敗。\n\n"
                f"{details}"
            ) from error