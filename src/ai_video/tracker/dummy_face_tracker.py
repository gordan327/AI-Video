from ai_video.tracker.face_tracker import FaceTracker
from ai_video.face import Face


class DummyFaceTracker(FaceTracker):
    """暫時的人臉追蹤器"""

    def __init__(self):
        self.next_id = 1

    def track(
        self,
        faces: list[Face],
    ) -> list[Face]:

        for face in faces:

            if face.track_id is None:
                face.track_id = self.next_id
                self.next_id += 1

        return faces