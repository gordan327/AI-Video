from pathlib import Path
import cv2
import numpy as np

from ai_video.config_manager import ConfigManager
from ai_video.detector.scrfd_face_detector import SCRFDFaceDetector
from ai_video.model_manager import ModelManager


class ImageProcessor:
    """處理單張圖片的人臉偵測與多種隱私保護渲染。"""

    def __init__(self, config: ConfigManager = None):
        self.config = config if config is not None else ConfigManager()
        self.model_manager = ModelManager(self.config)

    def process(self, input_path: Path, output_path: Path, renderer_type: str) -> int:
        """處理圖片並回傳偵測到的人臉數。"""
        print(f"[ImageProcessor] 開始讀取圖片: {input_path}")
        
        # 使用 np.fromfile 搭配 cv2.imdecode 支援中文與特殊字元路徑
        img_bytes = np.fromfile(str(input_path), dtype=np.uint8)
        img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"無法讀取圖片檔案: {input_path}")

        print("[ImageProcessor] 正在初始化偵測器...")
        detector = SCRFDFaceDetector(model_manager=self.model_manager, config=self.config)

        print("[ImageProcessor] 正在進行人臉偵測...")
        faces = detector.detect(img)
        print(f"[ImageProcessor] 偵測完成，找到 {len(faces)} 張人臉")

        if not renderer_type:
            renderer_type = "blur"

        print(f"[ImageProcessor] 套用渲染模式: {renderer_type}")
        output_img = img.copy()
        h, w = img.shape[:2]

        for face in faces:
            x1, y1, x2, y2 = face.x1, face.y1, face.x2, face.y2
            x1, y1, x2, y2 = max(0, int(x1)), max(0, int(y1)), min(w, int(x2)), min(h, int(y2))
            
            if x2 <= x1 or y2 <= y1:
                continue

            roi = output_img[y1:y2, x1:x2]

            if renderer_type == "pixelate":
                # 馬賽克處理
                rh, rw = roi.shape[:2]
                if rw > 0 and rh > 0:
                    blocks = max(1, min(rw, rh) // 10)
                    small = cv2.resize(roi, (blocks, blocks), interpolation=cv2.INTER_LINEAR)
                    pixelated = cv2.resize(small, (rw, rh), interpolation=cv2.INTER_NEAREST)
                    output_img[y1:y2, x1:x2] = pixelated
            elif renderer_type == "solid":
                # 純色遮蔽 (黑色)
                output_img[y1:y2, x1:x2] = (0, 0, 0)
            else:
                # 預設高斯模糊
                output_img[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (99, 99), 30)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 使用 cv2.imencode 搭配 tofile 支援中文儲存路徑
        success, encoded_img = cv2.imencode(output_path.suffix, output_img)
        if success:
            encoded_img.tofile(str(output_path))
        else:
            raise ValueError(f"無法儲存圖片檔案: {output_path}")

        print(f"[ImageProcessor] 圖片已成功儲存至: {output_path}")

        return len(faces)