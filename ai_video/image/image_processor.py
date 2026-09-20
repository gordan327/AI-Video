from pathlib import Path
import cv2
import numpy as np

from ai_video.detector.scrfd import SCRFDDetector
from ai_video.renderer.blur import BlurRenderer
from ai_video.renderer.pixelate import PixelateRenderer
from ai_video.renderer.solid import SolidRenderer
from ai_video.logger import Logger


class ImageProcessor:
    """處理單張照片的人臉偵測與隱私遮蔽。"""

    def __init__(self, config):
        self.config = config
        
        # 初始化偵測器
        model_name = config.get("detector.model", "buffalo_sc")
        det_size = config.get("detector.det_size", 640)
        confidence = config.get("detector.confidence", 0.5)
        provider = config.get("runtime.provider", "auto")

        self.detector = SCRFDDetector(
            model_name=model_name,
            det_size=(det_size, det_size),
            confidence=confidence,
            provider=provider,
        )

        # 初始化渲染器
        self.renderers = {
            "blur": BlurRenderer(config),
            "pixelate": PixelateRenderer(config),
            "solid": SolidRenderer(config),
        }

    def process(self, input_path: Path, output_path: Path, renderer_type: str) -> int:
        """處理單張照片，回傳偵測到的人臉數。"""
        Logger.info(f"正在讀取照片：{input_path}")
        image = cv2.imread(str(input_path))
        if image is None:
            raise RuntimeError(f"無法讀取圖片檔案：{input_path}")

        # 1. 偵測人臉
        Logger.info("正在進行人臉偵測...")
        faces = self.detector.detect(image)
        face_count = len(faces)
        Logger.info(f"偵測到 {face_count} 張人臉")

        if face_count > 0:
            # 2. 取得對應的渲染器並套用
            renderer = self.renderers.get(renderer_type)
            if renderer is None:
                renderer = self.renderers["blur"]

            Logger.info(f"正在套用處理方式：{renderer_type}")
            renderer.render(image, faces)

        # 3. 確保輸出資料夾存在並儲存
        output_path.parent.mkdir(parents=True, exist_ok=True)
        success = cv2.imwrite(str(output_path), image)
        if not success:
            raise RuntimeError(f"無法儲存處理後的圖片至：{output_path}")

        Logger.success(f"照片處理完成，已輸出至：{output_path}")
        return face_count