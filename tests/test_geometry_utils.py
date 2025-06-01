import numpy as np
import math

from utils.geometry_utils import (
    get_shortest_distance_between_rects,
    get_containment_ratio,
    get_rect_center,
    get_rect_width,
    get_rect_height,
    get_point_distance,
    project,
)


def test_get_shortest_distance_between_rects():
    rect1 = (0, 0, 10, 10)
    rect2 = (20, 0, 30, 10)
    assert math.isclose(get_shortest_distance_between_rects(rect1, rect2), 10.0)

    rect3 = (5, 5, 15, 15)
    assert math.isclose(get_shortest_distance_between_rects(rect1, rect3), 0.0)


def test_get_containment_ratio():
    rect1 = (0, 0, 10, 10)
    rect2 = (2, 2, 8, 8)
    assert math.isclose(get_containment_ratio(rect1, rect2), 0.36)

    rect3 = (20, 20, 30, 30)
    assert get_containment_ratio(rect1, rect3) == 0.0


def test_get_rect_center():
    rect = (0, 0, 10, 10)
    assert get_rect_center(rect) == (5.0, 5.0)


def test_get_rect_width():
    rect = (2, 3, 8, 10)
    assert get_rect_width(rect) == 6


def test_get_rect_height():
    rect = (2, 3, 8, 10)
    assert get_rect_height(rect) == 7


def test_get_point_distance():
    p1 = (0, 0)
    p2 = (3, 4)
    assert math.isclose(get_point_distance(p1, p2), 5.0)


def test_project():
    point = (1.0, 2.0)
    matrix = np.eye(3)
    projected = project(point, matrix)
    assert np.allclose(projected, point)
