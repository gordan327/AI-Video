import traceback
from ai_video.face import Face
from ai_video.detector.face_detector import FaceDetector

class SCRFDFaceDetector(FaceDetector):
    """使用 SCRFD 偵測人臉並取得 embedding。"""

    def __init__(self, model_manager=None, config=None, model_name=None, **kwargs):
        self.model_manager = model_manager
        self.config = config
        self.app = None

        # 嘗試透過 ModelManager 取得（注意：face_analysis 是 property，不能加括號）
        try:
            if self.model_manager is not None and hasattr(self.model_manager, "face_analysis"):
                self.app = self.model_manager.face_analysis
        except Exception as e:
            print(f"從 ModelManager 取得 FaceAnalysis 失敗: {e}")
            traceback.print_exc()

        # 如果前面失敗，嘗試使用預設的 buffalo_sc
        if self.app is None:
            try:
                from insightface.app import FaceAnalysis
                self.app = FaceAnalysis(name="buffalo_sc", root="~/.insightface")
                self.app.prepare(ctx_id=0, det_size=(640, 640))
            except Exception as e:
                print(f"初始化 FaceAnalysis (buffalo_sc) 失敗: {e}")
                traceback.print_exc()

    def detect(self, frame) -> list[Face]:
        """偵測影格中的人臉。"""
        if self.app is None:
            print("[ERROR] self.app 為空，無法進行偵測")
            return []

        try:
            results = self.app.get(frame)
        except Exception as e:
            print(f"執行 app.get 時發生錯誤: {e}")
            traceback.print_exc()
            return []

        faces: list[Face] = []
        confidence_threshold = 0.5
        if self.config and hasattr(self.config, "get"):
            try:
                confidence_threshold = self.config.get("detector.confidence", 0.5)
            except Exception:
                pass

        for result in results:
            score = getattr(result, "det_score", 0.0)
            if score < confidence_threshold:
                continue

            bbox = getattr(result, "bbox", [0, 0, 0, 0])
            x1, y1, x2, y2 = map(int, bbox)
            embedding = getattr(result, "normed_embedding", None)

            faces.append(
                Face(
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                    confidence=float(score),
                    embedding=embedding,
                )
            )

        return faces
