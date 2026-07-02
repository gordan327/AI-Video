import cv2
from pathlib import Path


class VideoReader:
    """負責讀取影片及取得影片資訊"""

    def __init__(self, video_path: str):
        self.video_path = Path(video_path)
        self.cap = None

    def open(self):
        """開啟影片"""

        if not self.video_path.exists():
            raise FileNotFoundError(f"找不到影片：{self.video_path}")

        self.cap = cv2.VideoCapture(str(self.video_path))

        if not self.cap.isOpened():
            raise RuntimeError(f"無法開啟影片：{self.video_path}")

    def close(self):
        """關閉影片"""

        if self.cap is not None:
            self.cap.release()

    @property
    def fps(self) -> float:
        return self.cap.get(cv2.CAP_PROP_FPS)

    @property
    def width(self) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def frame_count(self) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def duration(self) -> float:
        if self.fps == 0:
            return 0.0
        return self.frame_count / self.fps

    def read(self):
        """讀取下一個 Frame"""

        if self.cap is None:
            raise RuntimeError("影片尚未開啟，請先呼叫 open()")

        success, frame = self.cap.read()
        return success, frame