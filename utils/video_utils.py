import cv2
import os

from common_types import FrameT


def read_video(path: str):
    video_capture = cv2.VideoCapture(path)
    frames: list[FrameT] = []

    while True:
        is_frame, frame = video_capture.read()

        if not is_frame:
            break

        frames.append(frame)

    return frames


def save_video(frames: list[FrameT], path: str):
    path_dir = os.path.dirname(path)

    if not os.path.exists(path_dir):
        os.mkdir(path_dir)

    frame_size = frames[0].shape
    fourcc = cv2.VideoWriter.fourcc(*"XVID")

    video_writer = cv2.VideoWriter(path, fourcc, 24, (frame_size[1], frame_size[0]))

    for frame in frames:
        video_writer.write(frame)

    video_writer.release()
