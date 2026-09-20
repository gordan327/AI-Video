"""AI-Video 應用程式資源與執行期目錄管理。"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


class ResourceManager:
    """集中管理 AI-Video 的應用程式資源與使用者資料路徑。"""

    APPLICATION_NAME = "AI-Video"

    # ------------------------------------------------------------------
    # Application resources
    # ------------------------------------------------------------------

    @staticmethod
    def package_root() -> Path:
        """回傳 ai_video 套件根目錄。"""

        return Path(__file__).resolve().parent

    @classmethod
    def config_path(cls) -> Path:
        """回傳套件內建的預設設定檔路徑。"""

        return cls.package_root() / "config" / "config.yaml"

    # ------------------------------------------------------------------
    # User application data
    # ------------------------------------------------------------------

    @classmethod
    def application_support_path(cls) -> Path:
        """回傳目前作業系統的 AI-Video 使用者資料根目錄。"""

        home = Path.home()

        if sys.platform == "darwin":
            return (
                home
                / "Library"
                / "Application Support"
                / cls.APPLICATION_NAME
            )

        if sys.platform.startswith("win"):
            appdata = os.environ.get("APPDATA")

            if appdata:
                return Path(appdata) / cls.APPLICATION_NAME

            return (
                home
                / "AppData"
                / "Roaming"
                / cls.APPLICATION_NAME
            )

        xdg_data_home = os.environ.get("XDG_DATA_HOME")

        if xdg_data_home:
            return Path(xdg_data_home) / cls.APPLICATION_NAME

        return (
            home
            / ".local"
            / "share"
            / cls.APPLICATION_NAME
        )

    # ------------------------------------------------------------------
    # AI model directories
    # ------------------------------------------------------------------

    @classmethod
    def insightface_root(cls) -> Path:
        """回傳 InsightFace 的資源根目錄。

        InsightFace 會自行在此目錄下建立：

            models/<model-name>
        """

        return cls.application_support_path() / "insightface"

    @classmethod
    def ultralytics_root(cls) -> Path:
        """回傳 Ultralytics 模型存放目錄。"""

        return cls.application_support_path() / "ultralytics"

    @classmethod
    def model_root(cls) -> Path:
        """回傳舊版通用模型目錄。

        此方法暫時保留，以避免既有程式碼立即失效。
        新程式應優先使用：

        - insightface_root()
        - ultralytics_root()
        """

        return (
            cls.application_support_path()
            / "models"
            / "downloads"
        )

    # ------------------------------------------------------------------
    # Runtime directories
    # ------------------------------------------------------------------

    @classmethod
    def log_directory(cls) -> Path:
        """回傳應用程式記錄檔目錄。"""

        return cls.application_support_path() / "logs"

    @classmethod
    def cache_directory(cls) -> Path:
        """回傳可安全刪除的快取目錄。"""

        return cls.application_support_path() / "cache"

    @classmethod
    def temp_directory(cls) -> Path:
        """回傳影片處理期間使用的暫存目錄。"""

        return cls.application_support_path() / "temp"

    # ------------------------------------------------------------------
    # FFmpeg
    # ------------------------------------------------------------------

    @classmethod
    def ffmpeg_directory(cls) -> Path:
        """回傳使用者資料區內的 FFmpeg 目錄。"""

        return cls.application_support_path() / "ffmpeg"

    @staticmethod
    def _ffmpeg_executable_name() -> str:
        """依作業系統回傳 FFmpeg 執行檔名稱。"""

        if sys.platform.startswith("win"):
            return "ffmpeg.exe"

        return "ffmpeg"

    @classmethod
    def ffmpeg_path(cls) -> Path:
        """尋找可使用的 FFmpeg 執行檔。

        搜尋順序：

        1. AI_VIDEO_FFMPEG 環境變數
        2. Application Support/AI-Video/ffmpeg
        3. macOS App Bundle Resources
        4. 套件內 resources/ffmpeg
        5. 系統 PATH
        """

        executable_name = cls._ffmpeg_executable_name()

        environment_path = os.environ.get("AI_VIDEO_FFMPEG")

        if environment_path:
            candidate = Path(environment_path).expanduser()

            if candidate.is_file():
                return candidate.resolve()

        candidate = cls.ffmpeg_directory() / executable_name

        if candidate.is_file():
            return candidate.resolve()

        bundle_candidate = (
            cls.package_root().parent.parent
            / "Resources"
            / "ffmpeg"
            / executable_name
        )

        if bundle_candidate.is_file():
            return bundle_candidate.resolve()

        package_candidate = (
            cls.package_root()
            / "resources"
            / "ffmpeg"
            / executable_name
        )

        if package_candidate.is_file():
            return package_candidate.resolve()

        system_ffmpeg = shutil.which(executable_name)

        if system_ffmpeg:
            return Path(system_ffmpeg).resolve()

        raise FileNotFoundError(
            "找不到 FFmpeg 執行檔。請安裝 FFmpeg，"
            "或設定 AI_VIDEO_FFMPEG 環境變數。"
        )

    # ------------------------------------------------------------------
    # Directory creation
    # ------------------------------------------------------------------

    @classmethod
    def _ensure_directory(cls, path: Path) -> Path:
        """建立目錄並回傳其路徑。"""

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path

    @classmethod
    def ensure_application_support(cls) -> Path:
        """建立並回傳應用程式資料根目錄。"""

        return cls._ensure_directory(
            cls.application_support_path()
        )

    @classmethod
    def ensure_model_directory(cls) -> Path:
        """建立並回傳舊版通用模型目錄。

        此方法暫時保留供既有程式使用。
        """

        return cls._ensure_directory(
            cls.model_root()
        )

    @classmethod
    def ensure_insightface_root(cls) -> Path:
        """建立並回傳 InsightFace 資源根目錄。"""

        return cls._ensure_directory(
            cls.insightface_root()
        )

    @classmethod
    def ensure_ultralytics_root(cls) -> Path:
        """建立並回傳 Ultralytics 模型目錄。"""

        return cls._ensure_directory(
            cls.ultralytics_root()
        )

    @classmethod
    def ensure_log_directory(cls) -> Path:
        """建立並回傳記錄檔目錄。"""

        return cls._ensure_directory(
            cls.log_directory()
        )

    @classmethod
    def ensure_cache_directory(cls) -> Path:
        """建立並回傳快取目錄。"""

        return cls._ensure_directory(
            cls.cache_directory()
        )

    @classmethod
    def ensure_temp_directory(cls) -> Path:
        """建立並回傳暫存目錄。"""

        return cls._ensure_directory(
            cls.temp_directory()
        )

    @classmethod
    def ensure_ffmpeg_directory(cls) -> Path:
        """建立並回傳 FFmpeg 目錄。"""

        return cls._ensure_directory(
            cls.ffmpeg_directory()
        )