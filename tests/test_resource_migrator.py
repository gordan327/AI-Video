"""ResourceMigrator 單元測試。"""

from pathlib import Path

from ai_video.resource_manager import ResourceManager
from ai_video.resource_migrator import ResourceMigrator


def test_create_migrator(tmp_path: Path):
    """可以建立 ResourceMigrator。"""

    migrator = ResourceMigrator(
        project_root=tmp_path,
    )

    assert migrator.project_root == tmp_path


def test_has_no_legacy_models(tmp_path: Path):
    """舊版模型目錄不存在時，應回傳 False。"""

    migrator = ResourceMigrator(
        project_root=tmp_path,
    )

    assert migrator.has_legacy_models() is False


def test_has_legacy_models(tmp_path: Path):
    """舊版模型目錄存在時，應回傳 True。"""

    legacy_directory = (
        tmp_path
        / "models"
        / "downloads"
        / "models"
        / "buffalo_sc"
    )

    legacy_directory.mkdir(
        parents=True,
    )

    migrator = ResourceMigrator(
        project_root=tmp_path,
    )

    assert migrator.has_legacy_models() is True


def test_copy_directory(tmp_path: Path):
    """可以將來源目錄完整複製到目的目錄。"""

    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    model_file = source / "det_500m.onnx"
    model_file.write_text(
        "fake model data",
        encoding="utf-8",
    )

    migrator = ResourceMigrator(
        project_root=tmp_path,
    )

    result = migrator._copy_directory(
        source,
        destination,
    )

    assert result is True
    assert destination.is_dir()
    assert (
        destination / "det_500m.onnx"
    ).read_text(
        encoding="utf-8",
    ) == "fake model data"


def test_skip_existing_directory(tmp_path: Path):
    """目的目錄已存在時，不應覆蓋原有內容。"""

    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()
    destination.mkdir()

    (source / "model.onnx").write_text(
        "new model",
        encoding="utf-8",
    )

    existing_file = destination / "existing.txt"
    existing_file.write_text(
        "existing data",
        encoding="utf-8",
    )

    migrator = ResourceMigrator(
        project_root=tmp_path,
    )

    result = migrator._copy_directory(
        source,
        destination,
    )

    assert result is False
    assert existing_file.read_text(
        encoding="utf-8",
    ) == "existing data"
    assert not (
        destination / "model.onnx"
    ).exists()


def test_migrate_insightface_models(
    tmp_path: Path,
    monkeypatch,
):
    """可以將舊版 InsightFace 模型複製到新版目錄。"""

    legacy_directory = (
        tmp_path
        / "models"
        / "downloads"
        / "models"
        / "buffalo_sc"
    )

    legacy_directory.mkdir(
        parents=True,
    )

    (legacy_directory / "det_500m.onnx").write_text(
        "detector model",
        encoding="utf-8",
    )

    (legacy_directory / "w600k_mbf.onnx").write_text(
        "recognition model",
        encoding="utf-8",
    )

    insightface_root = (
        tmp_path
        / "application_support"
        / "insightface"
    )

    monkeypatch.setattr(
        ResourceManager,
        "ensure_insightface_root",
        staticmethod(
            lambda: insightface_root
        ),
    )

    migrator = ResourceMigrator(
        project_root=tmp_path,
    )

    result = migrator.migrate_insightface_models()

    destination = (
        insightface_root
        / "models"
        / "buffalo_sc"
    )

    assert result is True
    assert (
        destination / "det_500m.onnx"
    ).read_text(
        encoding="utf-8",
    ) == "detector model"
    assert (
        destination / "w600k_mbf.onnx"
    ).read_text(
        encoding="utf-8",
    ) == "recognition model"


def test_migrate_returns_none(tmp_path: Path):
    """migrate() 完成後應回傳 None。"""

    migrator = ResourceMigrator(
        project_root=tmp_path,
    )

    assert migrator.migrate() is None