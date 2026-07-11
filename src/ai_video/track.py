from dataclasses import dataclass, field

from ai_video.face import Face
from ai_video.kalman_filter import KalmanFilter
from ai_video.track_state import TrackState


@dataclass
class Track:
    """代表一個持續追蹤中的目標"""

    # Identity
    track_id: int

    # 最新偵測到的人臉
    face: Face

    # Kalman Filter
    kalman: KalmanFilter = field(default_factory=KalmanFilter)

    # Track 狀態
    state: TrackState = TrackState.ACTIVE

    # 統計資訊
    age: int = 0
    missed: int = 0

    # Prediction
    predicted_x: float = 0.0
    predicted_y: float = 0.0

    predicted_box: tuple[float, float, float, float] | None = None

    def __post_init__(self):

        center_x = (self.face.x1 + self.face.x2) / 2
        center_y = (self.face.y1 + self.face.y2) / 2

        self.kalman.initiate(
            center_x,
            center_y,
        )

        self.predicted_x = center_x
        self.predicted_y = center_y

        self.predicted_box = (
            self.face.x1,
            self.face.y1,
            self.face.x2,
            self.face.y2,
        )