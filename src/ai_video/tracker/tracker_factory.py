from ai_video.tracker.bytetrack_face_tracker import (
    ByteTrackFaceTracker,
)
from ai_video.tracker.face_tracker import FaceTracker


_TRACKERS = {
    "bytetrack": ByteTrackFaceTracker,
}


class TrackerFactory:
    """建立指定類型的人臉追蹤器。"""

    @staticmethod
    def create(
        tracker_type: str,
        **kwargs,
    ) -> FaceTracker:
        """依類型建立 Tracker。"""

        tracker_key = (
            tracker_type
            .strip()
            .lower()
        )

        tracker_class = _TRACKERS.get(
            tracker_key
        )

        if tracker_class is None:
            raise ValueError(
                f"未知人臉追蹤器：{tracker_type}"
            )

        if tracker_key == "bytetrack":
            return tracker_class(
                privacy_hold_frames=kwargs.get(
                    "privacy_hold_frames",
                    15,
                ),
                prediction_frames=kwargs.get(
                    "prediction_frames",
                    3,
                ),
                freeze_expansion_per_frame=kwargs.get(
                    "freeze_expansion_per_frame",
                    0.03,
                ),
            )

        raise ValueError(
            f"無法建立人臉追蹤器：{tracker_type}"
        )