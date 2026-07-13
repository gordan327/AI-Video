from dataclasses import dataclass, field

import numpy as np

from ai_video.face import Face
from ai_video.kalman_filter import KalmanFilter
from ai_video.track_state import TrackState


@dataclass
class Track:
    """代表一個持續追蹤中的目標。"""

    track_id: int
    face: Face

    kalman: KalmanFilter = field(default_factory=KalmanFilter)
    state: TrackState = TrackState.ACTIVE

    age: int = 0
    missed: int = 0

    predicted_x: float = 0.0
    predicted_y: float = 0.0
    predicted_box: tuple[
        float, 
        float, 
        float, 
        float
    ] | None = None

    last_confirmed_box: tuple[
        float, 
        float, 
        float, 
        float
    ] | None = None

    embedding_history: list[np.ndarray] = field(default_factory=list)

    def __post_init__(self):
        """初始化 Kalman Filter、預測框及 embedding 紀錄。"""

        center_x = (self.face.x1 + self.face.x2) / 2
        center_y = (self.face.y1 + self.face.y2) / 2

        self.kalman.initiate(
            center_x,
            center_y,
        )

        self.predicted_x = center_x
        self.predicted_y = center_y

        initial_box = (
            float(self.face.x1),
            float(self.face.y1),
            float(self.face.x2),
            float(self.face.y2),
        )

        self.predicted_box = initial_box
        self.last_confirmed_box = initial_box

        self.add_embedding(self.face.embedding)

    def add_embedding(
        self,
        embedding: np.ndarray | None,
        max_history: int = 20,
    ):
        """加入 embedding，最多保留最近指定筆數。"""

        if embedding is None:
            return

        vector = np.asarray(
            embedding,
            dtype=np.float32,
        ).reshape(-1)

        norm = np.linalg.norm(vector)

        if norm == 0:
            return

        vector = vector / norm

        self.embedding_history.append(vector)

        if len(self.embedding_history) > max_history:
            self.embedding_history = self.embedding_history[-max_history:]

    def get_average_embedding(self) -> np.ndarray | None:
        """取得歷史 embedding 的正規化平均值。"""

        if not self.embedding_history:
            return None

        average = np.mean(
            np.stack(self.embedding_history),
            axis=0,
        )

        norm = np.linalg.norm(average)

        if norm == 0:
            return None

        return average / norm