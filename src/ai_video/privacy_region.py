from dataclasses import dataclass

from ai_video.face import Face


@dataclass(frozen=True)
class PrivacyBox:
    """代表需要進行隱私處理的矩形區域。"""

    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1

    @property
    def is_valid(self) -> bool:
        return self.width > 1 and self.height > 1

    def as_tuple(self) -> tuple[int, int, int, int]:
        return (
            self.x1,
            self.y1,
            self.x2,
            self.y2,
        )


class PrivacyRegion:
    """將人臉框轉換為較完整的頭部隱私區域。"""

    def __init__(
        self,
        padding_ratio: float = 0.35,
        top_multiplier: float = 1.7,
        bottom_multiplier: float = 0.8,
    ):
        self.padding_ratio = max(
            0.0,
            float(padding_ratio),
        )

        self.top_multiplier = max(
            0.0,
            float(top_multiplier),
        )

        self.bottom_multiplier = max(
            0.0,
            float(bottom_multiplier),
        )

    def create(
        self,
        face: Face,
        frame_width: int,
        frame_height: int,
    ) -> PrivacyBox | None:
        """依據人臉框建立頭部隱私區域。"""

        face_width = face.x2 - face.x1
        face_height = face.y2 - face.y1

        if face_width <= 1 or face_height <= 1:
            return None

        side_padding = int(
            face_width * self.padding_ratio
        )

        top_padding = int(
            face_height
            * self.padding_ratio
            * self.top_multiplier
        )

        bottom_padding = int(
            face_height
            * self.padding_ratio
            * self.bottom_multiplier
        )

        box = PrivacyBox(
            x1=max(
                0,
                int(face.x1 - side_padding),
            ),
            y1=max(
                0,
                int(face.y1 - top_padding),
            ),
            x2=min(
                frame_width,
                int(face.x2 + side_padding),
            ),
            y2=min(
                frame_height,
                int(face.y2 + bottom_padding),
            ),
        )

        if not box.is_valid:
            return None

        return box