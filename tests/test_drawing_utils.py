import numpy as np
from utils.drawing_utils import draw_ellipse, draw_triangle, put_text


def test_draw_ellipse_runs():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    bbox = (20, 20, 80, 80)
    result = draw_ellipse(img.copy(), bbox, (255, 0, 0), track_id=1)
    assert result.shape == img.shape


def test_draw_triangle_runs():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    bbox = (20, 20, 80, 80)
    result = draw_triangle(img.copy(), bbox, (0, 255, 0))
    assert result.shape == img.shape


def test_put_text_runs():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    result = put_text(img.copy(), "Test", (10, 50))
    assert result.shape == img.shape
