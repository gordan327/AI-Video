import cv2

from ai_video.face import Face
from ai_video.privacy_region import PrivacyRegion
from ai_video.renderer.blur_renderer import BlurRenderer
from ai_video.renderer.renderer_factory import RendererFactory


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
        self.region_cache: dict[int, dict] = {}

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

                self.region_cache[face.track_id] = {
                    "box": box_tuple,
                    "remaining": self.temporal_hold_frames,
                }

        # 再處理本影格暫時消失的 Track
        expired_track_ids = []

        for track_id, cached in self.region_cache.items():
            if track_id in seen_track_ids:
                continue

            remaining = int(
                cached.get(
                    "remaining",
                    0,
                )
            )

            if remaining <= 0:
                expired_track_ids.append(track_id)
                continue

            cached_box = cached.get("box")

            if cached_box is not None:
                self._blur_box(
                    frame,
                    cached_box,
                )

            cached["remaining"] = remaining - 1

            if cached["remaining"] <= 0:
                expired_track_ids.append(track_id)

        for track_id in expired_track_ids:
            self.region_cache.pop(
                track_id,
                None,
            )

        return frame

    def _blur_box(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        self.effect_renderer.render(
            frame,
            box,
        )
        return

        """模糊指定矩形區域。"""

        frame_height, frame_width = frame.shape[:2]

        x1, y1, x2, y2 = box

        x1 = max(
            0,
            min(frame_width, int(x1)),
        )

        y1 = max(
            0,
            min(frame_height, int(y1)),
        )

        x2 = max(
            0,
            min(frame_width, int(x2)),
        )

        y2 = max(
            0,
            min(frame_height, int(y2)),
        )

        if x2 <= x1 or y2 <= y1:
            return

        face_region = frame[
            y1:y2,
            x1:x2,
        ]

        if face_region.size == 0:
            return

        region_height, region_width = (
            face_region.shape[:2]
        )

        kernel_size = min(
            self.blur_strength,
            region_width,
            region_height,
        )

        kernel_size = self._normalize_kernel_size(
            kernel_size
        )

        if kernel_size > region_width:
            kernel_size = (
                region_width
                if region_width % 2 == 1
                else region_width - 1
            )

        if kernel_size > region_height:
            kernel_size = (
                region_height
                if region_height % 2 == 1
                else region_height - 1
            )

        if kernel_size < 3:
            return

        blurred_region = cv2.GaussianBlur(
            face_region,
            (
                kernel_size,
                kernel_size,
            ),
            0,
        )

        frame[
            y1:y2,
            x1:x2,
        ] = blurred_region

    def reset(self):
        """清除所有歷史隱私區域。"""

        self.region_cache.clear()