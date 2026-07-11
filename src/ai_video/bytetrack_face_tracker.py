from ai_video.face import Face
from ai_video.face_tracker import FaceTracker

from ai_video.matching import Matcher
from ai_video.track_manager import TrackManager


class ByteTrackFaceTracker(FaceTracker):
    """ByteTrack 人臉追蹤器（目前為骨架版本）"""

    def __init__(self):

        self.matcher = Matcher()
        self.track_manager = TrackManager()

    def track(self, faces: list[Face]) -> list[Face]:
        """使用 IoU 更新人臉 Track"""

        self.track_manager.update_tracks(
            self.matcher,
            faces
        )

        return faces