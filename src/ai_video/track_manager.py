from ai_video.face import Face
from ai_video.track import Track
from ai_video.track_state import TrackState


class TrackManager:
    """負責管理所有 Track"""

    def __init__(self):
        self.tracks: list[Track] = []
        self.next_track_id = 1

    def create_track(self, face: Face) -> Track:
        """建立新的 Track"""

        face.track_id = self.next_track_id

        track = Track(
            track_id=self.next_track_id,
            face=face,
            state=TrackState.ACTIVE,
        )

        self.tracks.append(track)

        self.next_track_id += 1

        return track

    def update_track(
        self,
        track: Track,
        face: Face,
    ):
        """更新 Track"""

        # Bounding Box 中心
        center_x = (face.x1 + face.x2) / 2
        center_y = (face.y1 + face.y2) / 2

        # 更新 Kalman
        track.kalman.update(center_x, center_y)

        face.track_id = track.track_id
        track.face = face

        track.age += 1
        track.missed = 0
        track.state = TrackState.ACTIVE

    def predict_tracks(self):
        """利用 Kalman Filter 預測所有 Track"""

        for track in self.tracks:

            if track.state == TrackState.REMOVED:
                continue

            # 取得預測中心
            pred_x, pred_y = track.kalman.predict()

            track.predicted_x = pred_x
            track.predicted_y = pred_y

            # 保留上一個 bbox 的大小
            width = track.face.x2 - track.face.x1
            height = track.face.y2 - track.face.y1

            x1 = pred_x - width / 2
            y1 = pred_y - height / 2
            x2 = pred_x + width / 2
            y2 = pred_y + height / 2

            track.predicted_box = (
                x1,
                y1,
                x2,
                y2,
            )

    def mark_lost_track(
        self,
        track: Track,
    ):
        """標記 Track 為 LOST"""

        track.missed += 1

        if track.missed >= 30:
            track.state = TrackState.REMOVED
        else:
            track.state = TrackState.LOST

    def remove_removed_tracks(self):
        """移除已刪除 Track"""

        self.tracks = [
            track
            for track in self.tracks
            if track.state != TrackState.REMOVED
        ]

    def update_tracks(
        self,
        matcher,
        faces: list[Face],
    ) -> list[Face]:
        """更新所有 Track"""

        # 先做 Kalman Prediction
        self.predict_tracks()

        matched_pairs, unmatched_tracks, unmatched_faces = matcher.match(
            self.tracks,
            faces,
        )

        # 更新已配對 Track
        for track, face in matched_pairs:
            self.update_track(track, face)

        # 建立新的 Track
        for face in unmatched_faces:
            self.create_track(face)

        # 處理遺失 Track
        for track in unmatched_tracks:
            self.mark_lost_track(track)

        # 清除已移除 Track
        self.remove_removed_tracks()

        return faces

    def get_tracks(self) -> list[Track]:
        """取得所有 Track"""

        return self.tracks

    def reset(self):
        """重置 Tracker"""

        self.tracks.clear()
        self.next_track_id = 1