from pathlib import Path

from ai_video.config_manager import ConfigManager

class ProcessingConfiguration:
    """集中設定影片處理工作所需的組態。"""

    @staticmethod
    def apply(
        config: ConfigManager,
        input_path: str | Path,
        output_path: str | Path,
        temp_output_path: str | Path,
        detector: str,
        tracker: str,
        renderer: str,
    ) -> None:
        """將影片處理參數寫入設定。"""

        config.set(
            "video.input",
            str(input_path),
        )

        config.set(
            "video.temp_output",
            str(temp_output_path),
        )

        config.set(
            "video.output",
            str(output_path),
        )

        config.set(
            "detector.type",
            detector,
        )

        config.set(
            "tracker.type",
            tracker,
        )

        config.set(
            "renderer.type",
            renderer,
        )