from pathlib import Path

from insightface.app import FaceAnalysis


class ModelManager:
    """統一管理 AI 模型"""

    def __init__(self, config):

        self.config = config

        self._face_analysis = None

    @property
    def face_analysis(self):

        if self._face_analysis is None:

            model_name = self.config.get(
                "detector.model"
            )

            det_size = self._resolve_det_size()

            provider = self.config.get(
                "runtime.provider",
                "CPUExecutionProvider",
            )

            if not provider or provider == "auto":
                provider = "CPUExecutionProvider"

            self._face_analysis = FaceAnalysis(
                name=model_name,
                root=str(Path("models/downloads")),
                providers=[provider],
            )

            self._face_analysis.prepare(
                ctx_id=0,
                det_size=(det_size, det_size),
            )

        return self._face_analysis

    def _resolve_det_size(self):
        """取得實際使用的 SCRFD det_size。"""

        det_size = self.config.get(
            "detector.det_size"
        )

        if det_size == "auto":
            # 第一版：auto 先固定使用 800。
            # 後續可依影片解析度自動決定。
            return 800

        return int(det_size)