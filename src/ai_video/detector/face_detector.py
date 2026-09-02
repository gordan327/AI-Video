from abc import ABC, abstractmethod

from ai_video.face import Face


class FaceDetector(ABC):
    """所有人臉偵測器的共同介面"""

    @abstractmethod
    def detect(self, frame) -> list[Face]:
        """
        偵測影格中的所有人臉。

        Parameters
        ----------
        frame
            OpenCV 讀入的一個 Frame

        Returns
        -------
        list[Face]
            偵測到的人臉列表
        """
        pass