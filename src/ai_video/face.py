from dataclasses import dataclass

import numpy as np


@dataclass
class Face:
    """代表一張偵測到的人臉"""

    x1: int
    y1: int
    x2: int
    y2: int

    confidence: float

    track_id: int | None = None

    # InsightFace embedding
    embedding: np.ndarray | None = None