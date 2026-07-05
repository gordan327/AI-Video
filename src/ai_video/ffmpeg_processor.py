import subprocess
from pathlib import Path


class FFmpegProcessor:
    """FFmpeg 相關影片處理"""

    def merge_audio(
        self,
        original_video: str,
        processed_video: str,
        output_video: str,
    ):
        """
        將原始影片的音訊合併到處理後的影片。
        """
        
        original_video = Path(original_video)
        processed_video = Path(processed_video)
        output_video = Path(output_video)


        command = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(processed_video),

            "-i",
            str(original_video),

            "-c:v",
            "copy",

             "-map",
            "0:v:0",

            "-map",
            "1:a:0?",

            "-c:a",
            "aac",

            str(output_video),
    
        ]

        
        subprocess.run(
            command,
            check=True,
        )
