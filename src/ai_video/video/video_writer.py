import cv2
from pathlib import Path


class VideoWriter:
    """負責將處理後的影格寫入影片"""

    def __init__(
        self,
        output_path: str,
        fps: float,
        width: int,
        height: int,
    ):
        self.output_path = Path(output_path)
        self.fps = fps
        self.width = width
        self.height = height

        self.writer = None

    def open(self):
        """建立影片輸出"""

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        self.writer = cv2.VideoWriter(
            str(self.output_path),
            fourcc,
            self.fps,
            (self.width, self.height),
        )

        if not self.writer.isOpened():
            raise RuntimeError(
                f"無法建立輸出影片：{self.output_path}"
            )

    def write(self, frame):
        """寫入一個 Frame"""

        if self.writer is None:
            raise RuntimeError("VideoWriter 尚未開啟")

        self.writer.write(frame)

    def close(self):
        """關閉影片"""

        if self.writer is not None:
            self.writer.release()