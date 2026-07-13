from ai_video.face import Face
from ai_video.track import Track
from ai_video.track_state import TrackState


class TrackManager:
    """負責管理所有 Track。"""

    def __init__(self):
        self.tracks: list[Track] = []
        self.next_track_id = 1

    def create_track(self, face: Face) -> Track:
        """建立新的 Track。"""

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
        """以新偵測結果更新 Track。"""

        center_x = (face.x1 + face.x2) / 2
        center_y = (face.y1 + face.y2) / 2

        track.kalman.update(
            center_x,
            center_y,
        )

        track.add_embedding(
            face.embedding,
            max_history=20,
        )

        face.track_id = track.track_id
        track.face = face

        track.last_confirmed_box = (
            float(face.x1),
            float(face.y1),
            float(face.x2),
            float(face.y2),
        )

        track.age += 1
        
        track.missed = 0
        track.state = TrackState.ACTIVE

    def predict_tracks(self):
        """利用 Kalman Filter 預測所有 Track 的下一個位置。"""

        for track in self.tracks:
            if track.state == TrackState.REMOVED:
                continue

            predicted_x, predicted_y = track.kalman.predict()

            track.predicted_x = float(predicted_x)
            track.predicted_y = float(predicted_y)

            width = track.face.x2 - track.face.x1
            height = track.face.y2 - track.face.y1

            track.predicted_box = (
                predicted_x - width / 2,
                predicted_y - height / 2,
                predicted_x + width / 2,
                predicted_y + height / 2,
            )

    def mark_lost_track(self, track: Track):
        """標記 Track 為 LOST 或 REMOVED。"""

        track.missed += 1

        if track.missed >= 30:
            track.state = TrackState.REMOVED
        else:
            track.state = TrackState.LOST

    def remove_removed_tracks(self):
        """移除狀態為 REMOVED 的 Track。"""

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
        """配對偵測結果並更新所有 Track。"""

        self.predict_tracks()

        matched_pairs, unmatched_tracks, unmatched_faces = matcher.match(
            self.tracks,
            faces,
        )

        for track, face in matched_pairs:
            self.update_track(track, face)

        for face in unmatched_faces:
            self.create_track(face)

        for track in unmatched_tracks:
            self.mark_lost_track(track)

        self.remove_removed_tracks()

        return faces

    def get_tracks(self) -> list[Track]:
        """取得所有 Track。"""

        return self.tracks

    def reset(self):
        """重置所有追蹤狀態。"""

        self.tracks.clear()
        self.next_track_id = 1