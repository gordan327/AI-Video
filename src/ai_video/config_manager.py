from pathlib import Path
from ai_video.config.configuration_error import (
    ConfigurationError,
)

import yaml


class ConfigManager:
    """讀取並管理 AI-Video 設定。"""

    def __init__(
        self,
        config_path: str | Path | None = None,
    ):
        if config_path is None:
            config_path = (
                Path(__file__).resolve().parent
                / "config"
                / "config.yaml"
            )

        self.config_path = Path(config_path)

        self.config = {}

        self.reload()

    def reload(self):
        """重新從設定檔載入設定。"""

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"找不到設定檔：{self.config_path}"
            )

        try:
            with self.config_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                loaded_config = yaml.safe_load(file)
        except yaml.YAMLError as error:
            raise ValueError(
                f"Invalid YAML configuration: {self.config_path}"
            ) from error

        if loaded_config is None:
            loaded_config = {}

        if not isinstance(loaded_config, dict):
            raise ValueError(
                "Configuration root must be a mapping."
            )

        self.config = loaded_config

        if loaded_config is None:
            loaded_config = {}

        if not isinstance(loaded_config, dict):
            raise ValueError(
                "Configuration root must be a mapping."
            )

        self.config = loaded_config

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
        config.set("detector.confidence", 0.60)
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

    def save(self):
        """將目前設定寫回 YAML 檔案。"""

        self.config_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.config_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            yaml.safe_dump(
                self.config,
                file,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
            )

    def validate(self) -> None:
        """驗證目前設定內容。"""

        renderer_type = self.get(
            "renderer.type"
        )

        supported_renderers = {
            "blur",
            "pixelate",
            "solid",
        }

        if renderer_type not in supported_renderers:
            raise ConfigurationError(
                "Unsupported renderer type: "
                f"{renderer_type}"
            )