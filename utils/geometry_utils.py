import math

from common_types import RectCoordsT


def get_shortest_distance_between_rects(rect1: RectCoordsT, rect2: RectCoordsT):
    x1_min, y1_min, x1_max, y1_max = rect1
    x2_min, y2_min, x2_max, y2_max = rect2

    if x1_min > x1_max:
        x1_min, x1_max = x1_max, x1_min
    if y1_min > y1_max:
        y1_min, y1_max = y1_max, y1_min
    if x2_min > x2_max:
        x2_min, x2_max = x2_max, x2_min
    if y2_min > y2_max:
        y2_min, y2_max = y2_max, y2_min

    dx = max(0, x1_min - x2_max, x2_min - x1_max)
    dy = max(0, y1_min - y2_max, y2_min - y1_max)

    return math.hypot(dx, dy)


def get_containment_ratio(rect1: RectCoordsT, rect2: RectCoordsT):
    x1_min, y1_min, x1_max, y1_max = rect1
    x2_min, y2_min, x2_max, y2_max = rect2

    if x1_min > x1_max or y1_min > y1_max or x2_min > x2_max or y2_min > y2_max:
        return 0.0

    intersection_x_min = max(x1_min, x2_min)
    intersection_y_min = max(y1_min, y2_min)
    intersection_x_max = min(x1_max, x2_max)
    intersection_y_max = min(y1_max, y2_max)

    if (
        intersection_x_min >= intersection_x_max
        or intersection_y_min >= intersection_y_max
    ):
        return 0.0

    intersection_area = (intersection_x_max - intersection_x_min) * (
        intersection_y_max - intersection_y_min
    )
    rect1_area = (x1_max - x1_min) * (y1_max - y1_min)

    return intersection_area / rect1_area if rect1_area > 0 else 0.0


def get_rect_center(rect: RectCoordsT):
    x1, y1, x2, y2 = rect

    x = (x1 + x2) / 2
    y = (y1 + y2) / 2

    return x, y


def get_rect_width(rect: RectCoordsT):
    x1, _, x2, _ = rect

    return x2 - x1


def get_rect_height(rect: RectCoordsT):
    _, y1, _, y2 = rect

    return y2 - y1
