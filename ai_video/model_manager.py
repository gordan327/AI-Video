from insightface.app import FaceAnalysis

from ai_video.resource_manager import ResourceManager


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

            insightface_root = (
                ResourceManager.ensure_insightface_root()
            )

            self._face_analysis = FaceAnalysis(
                name=model_name,
                root=str(insightface_root),
                providers=[provider],
            )

            self._face_analysis.prepare(
                ctx_id=0,
                det_size=(det_size, det_size),
            )

        return self._face_analysis

    def _resolve_det_size(self):
        """取得實際使用的 SCRFD det_size。"""
        # 加上預設值 800 與型態保護，避免回傳 ConfigManager 物件導致 int() 崩潰
        det_size = self.config.get("detector.det_size", 800)

        if det_size == "auto" or det_size is None:
            return 800

        if not isinstance(det_size, (int, float, str)):
            return 800

        try:
            return int(det_size)
        except (TypeError, ValueError):
            return 800