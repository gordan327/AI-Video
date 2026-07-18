from pathlib import Path


class VideoPathManager:
    """集中處理輸入及輸出影片路徑。"""

    @staticmethod
    def build_default_output_path(
        input_filename: str | Path,
        output_directory: str | Path,
    ) -> Path:
        """根據輸入影片產生預設輸出路徑。"""

        input_path = Path(input_filename)
        output_directory = Path(output_directory)

        return (
            output_directory
            / f"{input_path.stem}_blurred.mp4"
        )

    @staticmethod
    def build_output_path(
        filename: str | Path,
    ) -> Path:
        """建立輸出影片路徑，必要時補上 MP4 副檔名。"""

        output_path = Path(filename)

        if not output_path.suffix:
            output_path = output_path.with_suffix(".mp4")

        return output_path