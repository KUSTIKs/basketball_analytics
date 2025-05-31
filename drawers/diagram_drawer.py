from typing import Final
import cv2

from common_types import FrameT
from constants import COURT_IMAGE_PATH
from utils.diagram_converter import DiagramConverter


class DiagramDrawer:
    COURT_IMAGE_PATH: Final = COURT_IMAGE_PATH
    IMAGE_WIDTH: Final = 300
    IMAGE_HEIGHT: Final = 161

    y_offset = 10
    x_offset = 10
    alpha = 0.7

    def draw(self, frames: list[FrameT], keypoints: list[tuple[float, float]]):
        result_frames: list[FrameT] = []

        court_image = cv2.imread(self.COURT_IMAGE_PATH)
        court_image = cv2.resize(
            court_image,
            (self.IMAGE_WIDTH, self.IMAGE_HEIGHT),
            interpolation=cv2.INTER_AREA,
        )

        for frame in frames:
            frame = frame.copy()
            overlay = frame.copy()

            overlay[
                self.y_offset : self.y_offset + self.IMAGE_HEIGHT,
                self.x_offset : self.x_offset + self.IMAGE_WIDTH,
            ] = court_image

            cv2.addWeighted(
                src1=overlay,
                alpha=self.alpha,
                src2=frame,
                beta=1 - self.alpha,
                gamma=0,
                dst=frame,
            )

            for i, keypoint in enumerate(keypoints):
                x, y = DiagramConverter.get_relative_cordinate(
                    keypoint, self.IMAGE_WIDTH, self.IMAGE_HEIGHT
                )
                x = int(self.x_offset + x)
                y = int(self.y_offset + y)
                cv2.circle(
                    frame, (x, y), radius=5, color=(255, 100, 0), thickness=cv2.FILLED
                )
                cv2.putText(
                    frame,
                    f"{i + 1}",
                    (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                )

            result_frames.append(frame)

        return result_frames
