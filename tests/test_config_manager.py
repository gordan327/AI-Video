from pathlib import Path

import yaml

from ai_video.config_manager import ConfigManager

import pytest

from ai_video.config.configuration_error import (
    ConfigurationError,
)


def create_config_file(
    tmp_path: Path,
) -> Path:
    """建立測試用 YAML 設定檔。"""

    config_path = tmp_path / "config.yaml"

    config_data = {
        "detector": {
            "type": "scrfd",
            "confidence": 0.5,
        },
        "renderer": {
            "type": "blur",
            "blur_strength": 51,
        },
    }

    with config_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        yaml.safe_dump(
            config_data,
            file,
            allow_unicode=True,
            sort_keys=False,
        )

    return config_path


def test_load_config(
    tmp_path,
):
    """應能正確載入 YAML 設定。"""

    config_path = create_config_file(
        tmp_path
    )

    config = ConfigManager(
        config_path=config_path,
    )

    assert config.config_path == config_path
    assert isinstance(
        config.config,
        dict,
    )


def test_get_existing_value(
    tmp_path,
):
    """應能以點號取得既有設定。"""

    config = ConfigManager(
        create_config_file(
            tmp_path
        )
    )

    assert (
        config.get(
            "detector.type"
        )
        == "scrfd"
    )


def test_get_default_value(
    tmp_path,
):
    """設定不存在時應回傳預設值。"""

    config = ConfigManager(
        create_config_file(
            tmp_path
        )
    )

    assert (
        config.get(
            "unknown.value",
            123,
        )
        == 123
    )


def test_set_existing_value(
    tmp_path,
):
    """應能修改既有設定。"""

    config = ConfigManager(
        create_config_file(
            tmp_path
        )
    )

    config.set(
        "detector.confidence",
        0.75,
    )

    assert (
        config.get(
            "detector.confidence"
        )
        == 0.75
    )


def test_set_new_nested_value(
    tmp_path,
):
    """應能建立新的巢狀設定。"""

    config = ConfigManager(
        create_config_file(
            tmp_path
        )
    )

    config.set(
        "new_section.level.value",
        100,
    )

    assert (
        config.get(
            "new_section.level.value"
        )
        == 100
    )


def test_save_and_reload(
    tmp_path,
):
    """儲存後重新載入應保留修改內容。"""

    config_path = create_config_file(
        tmp_path
    )

    config = ConfigManager(
        config_path=config_path,
    )

    config.set(
        "renderer.blur_strength",
        77,
    )

    config.save()

    reloaded_config = ConfigManager(
        config_path=config_path,
    )

    assert (
        reloaded_config.get(
            "renderer.blur_strength"
        )
        == 77
    )

def test_reject_non_mapping_root(
    tmp_path,
):
    """YAML 根節點不是 mapping 時應拒絕載入。"""

    config_path = tmp_path / "config.yaml"

    config_path.write_text(
        "- item1\n- item2\n",
        encoding="utf-8",
    )

    try:
        ConfigManager(
            config_path=config_path,
        )
    except ValueError as error:
        assert (
            str(error)
            == "Configuration root must be a mapping."
        )
    else:
        raise AssertionError(
            "Expected ValueError"
        )

def test_invalid_yaml_should_raise_value_error(
    tmp_path,
):
    """YAML 格式錯誤應回報 ValueError。"""

    config_path = tmp_path / "config.yaml"

    config_path.write_text(
        "detector:\n  type: [scrfd\n",
        encoding="utf-8",
    )

    try:
        ConfigManager(
            config_path=config_path,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected ValueError"
        )

def test_validate_accepts_supported_renderer(
    tmp_path,
):
    config_path = tmp_path / "config.yaml"

    config_path.write_text(
        "renderer:\n"
        "  type: blur\n",
        encoding="utf-8",
    )

    config_manager = ConfigManager(
        config_path
    )

    config_manager.validate()


def test_validate_rejects_unsupported_renderer(
    tmp_path,
):
    config_path = tmp_path / "config.yaml"

    config_path.write_text(
        "renderer:\n"
        "  type: banana\n",
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError):
        ConfigManager(config_path)