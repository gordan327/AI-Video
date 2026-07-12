import pytest

from ai_video.geometry import (
    bbox_area,
    bbox_center,
    calculate_center_distance,
    calculate_iou,
)


def test_bbox_area():
    assert bbox_area((0, 0, 100, 50)) == 5000


def test_bbox_area_with_invalid_box():
    assert bbox_area((100, 50, 0, 0)) == 0


def test_bbox_center():
    assert bbox_center((0, 0, 100, 50)) == (50.0, 25.0)


def test_calculate_center_distance():
    box1 = (0, 0, 100, 100)
    box2 = (10, 0, 110, 100)

    assert calculate_center_distance(box1, box2) == pytest.approx(10.0)


def test_calculate_iou_same_box():
    box = (0, 0, 100, 100)

    assert calculate_iou(box, box) == pytest.approx(1.0)


def test_calculate_iou_partial_overlap():
    box1 = (0, 0, 100, 100)
    box2 = (10, 10, 90, 90)

    assert calculate_iou(box1, box2) == pytest.approx(0.64)


def test_calculate_iou_no_overlap():
    box1 = (0, 0, 50, 50)
    box2 = (60, 60, 100, 100)

    assert calculate_iou(box1, box2) == pytest.approx(0.0)