from ai_video.face import Face
from ai_video.face_tracker import FaceTracker
from ai_video.matching import Matcher
from ai_video.track_manager import TrackManager


class ByteTrackFaceTracker(FaceTracker):
    """以隱私保護為優先的人臉追蹤器。"""

    def __init__(
        self,
        privacy_hold_frames: int = 15,
        prediction_frames: int = 3,
        freeze_expansion_per_frame: float = 0.03,
    ):
        self.matcher = Matcher()
        self.track_manager = TrackManager()

        self.privacy_hold_frames = max(
            0,
            int(privacy_hold_frames),
        )

        self.prediction_frames = max(
            0,
            int(prediction_frames),
        )

        self.freeze_expansion_per_frame = max(
            0.0,
            float(freeze_expansion_per_frame),
        )

    def track(
        self,
        faces: list[Face],
    ) -> list[Face]:
        """
        更新追蹤結果並輸出需要模糊的人臉區域。

        策略：
        1. 有偵測結果時，使用最新偵測框。
        2. 漏偵測初期，使用 Kalman 預測框。
        3. 漏偵測較久時，凍結最後可信框並逐步放大。
        4. 超過 privacy_hold_frames 後停止輸出該框。
        """

        self.track_manager.update_tracks(
            self.matcher,
            faces,
        )

        output_faces = list(faces)

        for track in self.track_manager.get_tracks():
            if track.missed <= 0:
                continue

            if track.missed > self.privacy_hold_frames:
                continue

            privacy_box = self._get_privacy_box(track)

            if privacy_box is None:
                continue

            x1, y1, x2, y2 = privacy_box

            x1 = int(round(x1))
            y1 = int(round(y1))
            x2 = int(round(x2))
            y2 = int(round(y2))

            if x2 <= x1 or y2 <= y1:
                continue

            output_faces.append(
                Face(
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                    confidence=track.face.confidence,
                    track_id=track.track_id,
                    embedding=track.face.embedding,
                )
            )

        return output_faces

    def _get_privacy_box(self, track):
        """依漏偵測時間決定預測框或凍結擴張框。"""

        if track.missed <= self.prediction_frames:
            return track.predicted_box

        return self._get_expanded_frozen_box(track)

    def _get_expanded_frozen_box(self, track):
        """將最後可信框凍結，並隨漏偵測時間逐步放大。"""

        confirmed_box = track.last_confirmed_box

        if confirmed_box is None:
            return track.predicted_box

        x1, y1, x2, y2 = confirmed_box

        width = x2 - x1
        height = y2 - y1

        if width <= 0 or height <= 0:
            return None

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        freeze_frame_count = max(
            0,
            track.missed - self.prediction_frames,
        )

        expansion_ratio = (
            1.0
            + freeze_frame_count
            * self.freeze_expansion_per_frame
        )

        expanded_width = width * expansion_ratio
        expanded_height = height * expansion_ratio

        return (
            center_x - expanded_width / 2,
            center_y - expanded_height / 2,
            center_x + expanded_width / 2,
            center_y + expanded_height / 2,
        )