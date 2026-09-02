"""AI-Video 舊版執行期資源搬移。"""

from pathlib import Path
import shutil

from ai_video.resource_manager import ResourceManager


class ResourceMigrator:
    """管理 AI-Video 執行期資源的版本搬移。"""

    def __init__(self, project_root: Path | None = None):
        """建立 ResourceMigrator。"""

        if project_root is None:
            project_root = Path.cwd()

        self.project_root = Path(project_root)

    def migrate(self) -> None:
        """執行所有資源搬移工作。"""

        self._run(
            self.migrate_insightface_models,
        )

    def _run(self, migration) -> None:
        """執行單一搬移步驟。"""

        migration()

    def has_legacy_models(self) -> bool:
        """是否存在舊版 InsightFace 模型。"""

        legacy_directory = (
            self.project_root
            / "models"
            / "downloads"
            / "models"
            / "buffalo_sc"
        )

        return legacy_directory.is_dir()

    def migrate_insightface_models(self) -> bool:
        """搬移舊版 InsightFace 模型。"""

        if not self.has_legacy_models():
            return False

        source = (
            self.project_root
            / "models"
            / "downloads"
            / "models"
            / "buffalo_sc"
        )

        destination = (
            ResourceManager.ensure_insightface_root()
            / "models"
            / "buffalo_sc"
        )

        return self._copy_directory(
            source,
            destination,
        )

    def _copy_directory(
        self,
        source: Path,
        destination: Path,
    ) -> bool:
        """複製整個目錄。"""

        if destination.exists():
            return False

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copytree(
            source,
            destination,
        )

        return True