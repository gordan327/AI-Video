from dataclasses import dataclass


Box = tuple[int, int, int, int]


@dataclass
class TemporalRegion:
    """代表需要短暫保留的歷史隱私區域。"""

    box: Box
    remaining: int


class TemporalRegionCache:
    """管理短暫消失 Track 的歷史隱私區域。"""

    def __init__(
        self,
        hold_frames: int = 5,
    ):
        self.hold_frames = max(
            0,
            int(hold_frames),
        )

        self._regions: dict[
            int,
            TemporalRegion,
        ] = {}

    def update(
        self,
        track_id: int,
        box: Box,
    ):
        """新增或更新指定 Track 的隱私區域。"""

        self._regions[int(track_id)] = TemporalRegion(
            box=box,
            remaining=self.hold_frames,
        )

    def get_held_boxes(
        self,
        seen_track_ids: set[int],
    ) -> list[Box]:
        """
        取得本影格需要繼續呈現的歷史隱私區域。

        本影格已出現的 Track 不會重複輸出；
        未出現的 Track 會逐幀扣除剩餘保留次數。
        """

        held_boxes: list[Box] = []
        expired_track_ids: list[int] = []

        for track_id, region in self._regions.items():
            if track_id in seen_track_ids:
                continue

            if region.remaining <= 0:
                expired_track_ids.append(track_id)
                continue

            held_boxes.append(region.box)

            region.remaining -= 1

            if region.remaining <= 0:
                expired_track_ids.append(track_id)

        for track_id in expired_track_ids:
            self._regions.pop(
                track_id,
                None,
            )

        return held_boxes

    def reset(self):
        """清除所有歷史隱私區域。"""

        self._regions.clear()

    def __len__(self) -> int:
        """回傳目前快取中的 Track 數量。"""

        return len(self._regions)