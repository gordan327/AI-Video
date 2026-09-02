from abc import ABC, abstractmethod

from ai_video.face import Face


class FaceTracker(ABC):
    """人臉追蹤器抽象基底類別"""

    @abstractmethod
    def track(
        self,
        faces: list[Face],
    ) -> list[Face]:
        """追蹤人臉"""
        pass