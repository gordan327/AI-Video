from ai_video.temporal_region_cache import (
    TemporalRegionCache,
)


def test_cache_starts_empty():
    cache = TemporalRegionCache()

    assert len(cache) == 0


def test_update_adds_region():
    cache = TemporalRegionCache(
        hold_frames=5,
    )

    cache.update(
        track_id=1,
        box=(10, 20, 30, 40),
    )

    assert len(cache) == 1


def test_seen_track_is_not_returned():
    cache = TemporalRegionCache(
        hold_frames=5,
    )

    cache.update(
        track_id=1,
        box=(10, 20, 30, 40),
    )

    boxes = cache.get_held_boxes(
        seen_track_ids={1},
    )

    assert boxes == []
    assert len(cache) == 1


def test_missing_track_returns_cached_box():
    cache = TemporalRegionCache(
        hold_frames=5,
    )

    box = (10, 20, 30, 40)

    cache.update(
        track_id=1,
        box=box,
    )

    boxes = cache.get_held_boxes(
        seen_track_ids=set(),
    )

    assert boxes == [box]
    assert len(cache) == 1


def test_region_expires_after_hold_frames():
    cache = TemporalRegionCache(
        hold_frames=2,
    )

    box = (10, 20, 30, 40)

    cache.update(
        track_id=1,
        box=box,
    )

    first_boxes = cache.get_held_boxes(
        seen_track_ids=set(),
    )

    second_boxes = cache.get_held_boxes(
        seen_track_ids=set(),
    )

    third_boxes = cache.get_held_boxes(
        seen_track_ids=set(),
    )

    assert first_boxes == [box]
    assert second_boxes == [box]
    assert third_boxes == []
    assert len(cache) == 0


def test_update_refreshes_remaining_frames():
    cache = TemporalRegionCache(
        hold_frames=2,
    )

    first_box = (10, 20, 30, 40)
    updated_box = (15, 25, 35, 45)

    cache.update(
        track_id=1,
        box=first_box,
    )

    cache.get_held_boxes(
        seen_track_ids=set(),
    )

    cache.update(
        track_id=1,
        box=updated_box,
    )

    first_held = cache.get_held_boxes(
        seen_track_ids=set(),
    )

    second_held = cache.get_held_boxes(
        seen_track_ids=set(),
    )

    assert first_held == [updated_box]
    assert second_held == [updated_box]
    assert len(cache) == 0


def test_zero_hold_frames_does_not_return_box():
    cache = TemporalRegionCache(
        hold_frames=0,
    )

    cache.update(
        track_id=1,
        box=(10, 20, 30, 40),
    )

    boxes = cache.get_held_boxes(
        seen_track_ids=set(),
    )

    assert boxes == []
    assert len(cache) == 0


def test_reset_clears_all_regions():
    cache = TemporalRegionCache(
        hold_frames=5,
    )

    cache.update(
        track_id=1,
        box=(10, 20, 30, 40),
    )

    cache.update(
        track_id=2,
        box=(50, 60, 70, 80),
    )

    cache.reset()

    assert len(cache) == 0