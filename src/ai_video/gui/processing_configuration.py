from pathlib import Path

from ai_video.config_manager import ConfigManager
from ai_video.gui.processing_job import ProcessingJob

class ProcessingConfiguration:
    """集中設定影片處理工作所需的組態。"""

    @staticmethod
    def apply(
        config: ConfigManager,
        job: ProcessingJob,
    ) -> None:
        """將影片處理工作寫入設定。"""

        config.set(
            "video.input",
            str(job.input_path),
        )

        config.set(
            "video.temp_output",
            str(job.temp_output_path),
        )

        config.set(
            "video.output",
            str(job.output_path),
        )

        config.set(
            "detector.type",
            job.detector,
        )

        config.set(
            "tracker.type",
            job.tracker,
        )

        config.set(
            "renderer.type",
            job.renderer,
        )