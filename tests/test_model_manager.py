from ai_video.model_manager import ModelManager


class DummyConfig:
    """提供 ModelManager 測試所需的最小設定物件。"""

    def __init__(self, values):
        self.values = values

    def get(self, key, default=None):
        return self.values.get(key, default)


def test_resolve_det_size_auto_returns_800():
    """det_size 設為 auto 時，暫時解析為 800。"""

    config = DummyConfig(
        {
            "detector.det_size": "auto",
        }
    )

    model_manager = ModelManager(config)

    assert model_manager._resolve_det_size() == 800


def test_resolve_det_size_integer_returns_same_value():
    """det_size 為整數時，應回傳相同的整數。"""

    config = DummyConfig(
        {
            "detector.det_size": 640,
        }
    )

    model_manager = ModelManager(config)

    assert model_manager._resolve_det_size() == 640