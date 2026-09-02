from enum import Enum


class TrackState(Enum):
    """Track 的生命週期"""

    ACTIVE = 1

    LOST = 2

    REMOVED = 3