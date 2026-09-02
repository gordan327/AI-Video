class ResourceMigrator:
    """管理 AI-Video 執行期資源搬移。"""

    def migrate(self) -> None:
        """執行所有資源搬移工作。"""

        self.migrate_insightface_models()

    def migrate_insightface_models(self) -> bool:
        """搬移 InsightFace 模型。"""

        return False

    def has_legacy_models(self) -> bool:
        """是否存在舊版模型目錄。"""

        return False