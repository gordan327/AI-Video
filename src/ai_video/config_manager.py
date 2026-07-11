from pathlib import Path

import yaml


class ConfigManager:
    """讀取 config.yaml"""

    def __init__(self, config_path: str = "config/config.yaml"):

        self.config_path = Path(config_path)

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"找不到設定檔：{self.config_path}"
            )

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def get(self, key: str, default=None):
        """
        使用點號取得設定值，例如：

        detector.model
        video.input
        renderer.show_track_id
        """

        value = self.config

        for part in key.split("."):

            if not isinstance(value, dict):
                return default

            value = value.get(part)

            if value is None:
                return default

        return value