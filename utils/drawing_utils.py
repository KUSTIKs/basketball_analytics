import cv2
import numpy as np

from common_types import ColorT, FrameT


def draw_ellipse(
    frame: FrameT,
    bbox: list[float],
    color: ColorT,
    track_id: int | None = None,
):
    bbox_center = get_bbox_center(bbox)
    bbox_width = get_bbox_width(bbox)

    center = (int(bbox_center[0]), int(bbox[3]))
    axes = (int(0.75 * bbox_width), int(0.3 * bbox_width))

    cv2.ellipse(
        img=frame,
        center=center,
        axes=axes,
        angle=0,
        startAngle=-45,
        endAngle=235,
        color=color,
        thickness=2,
        lineType=cv2.LINE_4,
    )

    if track_id is None:
        return frame

    rect_width = 40
    rect_height = 20

    rect_x = int(center[0] - rect_width / 2)
    rect_y = int(center[1] + axes[1] - rect_height / 2)

    cv2.rectangle(
        img=frame,
        pt1=(rect_x, rect_y),
        pt2=(rect_x + rect_width, rect_y + rect_height),
        color=color,
        thickness=cv2.FILLED,
    )

    text = str(track_id)

    (text_width, text_height), _ = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, thickness=1
    )

    text_x = int(center[0] - text_width / 2)
    text_y = int(center[1] + axes[1] + text_height / 2)

    cv2.putText(
        img=frame,
        text=text,
        org=(text_x, text_y),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.5,
        color=(255, 255, 255),
        thickness=1,
        lineType=cv2.LINE_AA,
    )

    return frame


def draw_triangle(
    frame: FrameT,
    bbox: list[float],
    color: ColorT,
):
    bbox_center = get_bbox_center(bbox)

    triangle_height = 20
    triangle_width = 20

    bottom_point = (int(bbox_center[0]), int(bbox[1]))
    top_left_point = (
        bottom_point[0] - triangle_width // 2,
        bottom_point[1] - triangle_height,
    )
    top_right_point = (
        bottom_point[0] + triangle_width // 2,
        bottom_point[1] - triangle_height,
    )

    triangle_points = np.array([bottom_point, top_left_point, top_right_point])

    cv2.drawContours(
        image=frame,
        contours=[triangle_points],
        contourIdx=0,
        color=color,
        thickness=cv2.FILLED,
    )

    cv2.drawContours(
        image=frame,
        contours=[triangle_points],
        contourIdx=0,
        color=(255, 255, 255),
        thickness=2,
    )

    return frame


def get_bbox_center(bbox: list[float]):
    x1, y1, x2, y2 = bbox

    x = (x1 + x2) / 2
    y = (y1 + y2) / 2

    return x, y


def get_bbox_width(bbox: list[float]):
    x1, _, x2, _ = bbox

    return x2 - x1


def get_bbox_height(bbox: list[float]):
    _, y1, _, y2 = bbox

    return y2 - y1
