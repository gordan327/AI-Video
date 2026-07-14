from math import sqrt
from typing import Tuple

Box = Tuple[int, int, int, int]


def bbox_area(box: Box) -> float:
    """計算 Bounding Box 面積"""

    x1, y1, x2, y2 = box

    width = max(0, x2 - x1)
    height = max(0, y2 - y1)

    return width * height


def bbox_center(box: Box) -> tuple[float, float]:
    """計算 Bounding Box 中心點"""

    x1, y1, x2, y2 = box

    return (
        (x1 + x2) / 2,
        (y1 + y2) / 2,
    )


def calculate_center_distance(
    box1: Box,
    box2: Box,
) -> float:
    """計算兩個 Bounding Box 中心點距離"""

    cx1, cy1 = bbox_center(box1)
    cx2, cy2 = bbox_center(box2)

    return sqrt(
        (cx1 - cx2) ** 2 +
        (cy1 - cy2) ** 2
    )


def calculate_iou(
    box1: Box,
    box2: Box,
) -> float:
    """計算兩個 Bounding Box 的 IoU"""

    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = bbox_area(
        (
            x1,
            y1,
            x2,
            y2,
        )
    )

    union = (
        bbox_area(box1)
        + bbox_area(box2)
        - intersection
    )

    if union == 0:
        return 0.0

    return intersection / union