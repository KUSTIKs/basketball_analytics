from operator import is_
from typing import Final
import cv2

from common_types import ColorT, FrameT
from constants import COURT_IMAGE_PATH, TeamNumber
from utils.diagram_converter import DiagramConverter
from utils.drawing_utils import put_text


class DiagramDrawer:
    COURT_IMAGE_PATH: Final = COURT_IMAGE_PATH
    IMAGE_WIDTH: Final = 300
    IMAGE_HEIGHT: Final = 161

    y_offset = 10
    x_offset = 10
    alpha = 0.7

    team_colors: tuple[ColorT, ColorT]

    def __init__(self, team_colors: tuple[ColorT, ColorT] = ((255, 0, 0), (0, 0, 255))):
        self.team_colors = team_colors

    def draw(
        self,
        frames: list[FrameT],
        player_positions: list[dict[int, tuple[float, float]]],
        teams: list[dict[int, TeamNumber]],
        acquirers: list[int | None],
    ):
        result_frames: list[FrameT] = []

        court_image = cv2.imread(self.COURT_IMAGE_PATH)
        court_image = cv2.resize(
            court_image,
            (self.IMAGE_WIDTH, self.IMAGE_HEIGHT),
            interpolation=cv2.INTER_AREA,
        )

        for frame_index, frame in enumerate(frames):
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

            team = teams[frame_index]
            points = player_positions[frame_index]

            for player_id, position in points.items():
                x, y = DiagramConverter.get_relative_cordinate(
                    position, self.IMAGE_WIDTH, self.IMAGE_HEIGHT
                )
                x = int(self.x_offset + x)
                y = int(self.y_offset + y)

                team_number = team.get(player_id) if player_id else None

                if team_number is None:
                    continue

                color = self.team_colors[team_number.value]

                cv2.circle(frame, (x, y), radius=5, color=color, thickness=cv2.FILLED)

                is_acquirer = acquirers[frame_index] == player_id
                if is_acquirer:
                    cv2.circle(frame, (x, y), radius=8, color=(0, 0, 255), thickness=2)

                put_text(
                    img=frame,
                    text=f"{player_id}",
                    org=(x + 5, y - 5),
                    color=(255, 255, 255),
                    font_scale=0.5,
                )

            result_frames.append(frame)

        return result_frames
