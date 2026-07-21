import cv2

from ai_video.face import Face
from ai_video.privacy_region import PrivacyRegion
from ai_video.renderer.blur_renderer import BlurRenderer
from ai_video.renderer.renderer_factory import RendererFactory
from ai_video.temporal_region_cache import (
    TemporalRegionCache,
)

class FaceRenderer:
    """負責對影像中的人臉區域進行模糊處理。"""

    def __init__(
        self,
        renderer_type="blur",
        blur_strength=51,
        pixel_size=12,
        padding_ratio=0.35,
        temporal_hold_frames=5,
    ):
        self.pixel_size = max(
            2,
            int(pixel_size),
        )

        self.blur_strength = self._normalize_kernel_size(
            blur_strength
        )

        self.effect_renderer = RendererFactory.create(
            renderer_type=renderer_type,
            blur_strength=self.blur_strength,
            pixel_size=pixel_size,
        )

        self.privacy_region = PrivacyRegion(
            padding_ratio=padding_ratio,
        )

        self.temporal_hold_frames = max(
            0,
            int(temporal_hold_frames),
        )

        # track_id -> {
        #     "box": (x1, y1, x2, y2),
        #     "remaining": 剩餘保留幀數,
        # }
        self.region_cache = TemporalRegionCache(
            hold_frames=self.temporal_hold_frames,
        )

    @staticmethod
    def _normalize_kernel_size(value: int) -> int:
        """確保 Gaussian Blur 核心尺寸為大於 1 的奇數。"""

        value = max(
            3,
            int(value),
        )

        if value % 2 == 0:
            value += 1

        return value

    def draw(
        self,
        frame,
        faces: list[Face],
    ):
        """模糊目前人臉，以及短暫消失的歷史人臉區域。"""

        frame_height, frame_width = frame.shape[:2]

        seen_track_ids: set[int] = set()

        # 先處理本影格收到的人臉框
        for face in faces:
            privacy_box = self.privacy_region.create(
                face=face,
                frame_width=frame_width,
                frame_height=frame_height,
            )

            if privacy_box is None:
                continue

            box_tuple = privacy_box.as_tuple()

            self._blur_box(
                frame,
                box_tuple,
            )

            if face.track_id is not None:
                seen_track_ids.add(face.track_id)

                self.region_cache.update(
                    track_id=face.track_id,
                    box=box_tuple,
                )

        # 再處理本影格暫時消失的 Track
        for box in self.region_cache.get_held_boxes(
            seen_track_ids,
        ):
            self._blur_box(
                frame,
                box,
            )

    def _blur_box(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        """將指定區域交由目前的 Renderer 處理。"""

        self.effect_renderer.render(
            frame,
            box,
        )

    def reset(self):
        """清除所有歷史隱私區域。"""

        self.region_cache.reset()