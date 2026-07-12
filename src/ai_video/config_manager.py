from pathlib import Path

import yaml


class ConfigManager:
    """讀取並管理 AI-Video 設定。"""

    def __init__(self, config_path: str | Path | None = None):
        if config_path is None:
            config_path = (
                Path(__file__).resolve().parent
                / "config"
                / "config.yaml"
            )

        self.config_path = Path(config_path)

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"找不到設定檔：{self.config_path}"
            )

        with self.config_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            self.config = yaml.safe_load(file) or {}

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

    def set(self, key: str, value):
        """
        使用點號修改設定值。

        例如：
        config.set("video.input", "/path/input.mp4")
        """

        parts = key.split(".")
        target = self.config

        for part in parts[:-1]:
            current = target.get(part)

            if not isinstance(current, dict):
                current = {}
                target[part] = current

            target = current

        target[parts[-1]] = value