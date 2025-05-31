import cv2
from common_types import FrameT
from constants import TeamNumber
from utils.drawing_utils import put_text


class BallControllDrawer:
    def draw(
        self,
        frames: list[FrameT],
        teams: list[dict[int, TeamNumber]],
        acquirers: list[int | None],
    ):
        result_frames: list[FrameT] = []
        team_a_occurances = 0
        team_b_occurances = 0

        for i, frame in enumerate(frames):
            frame = frame.copy()
            acquirer = acquirers[i]
            team = teams[i]

            team_number = team.get(acquirer) if acquirer else None

            if team_number == TeamNumber.A:
                team_a_occurances += 1
            elif team_number == TeamNumber.B:
                team_b_occurances += 1

            team_a_rate = team_a_occurances / (i + 1) * 100
            team_b_rate = team_b_occurances / (i + 1) * 100

            frame = self.draw_box(
                frame=frame,
                team_a_rate=team_a_rate,
                team_b_rate=team_b_rate,
            )

            result_frames.append(frame)

        return result_frames

    def draw_box(
        self,
        frame: FrameT,
        team_a_rate: float,
        team_b_rate: float,
    ):
        height, width, _ = frame.shape
        box_height = int(height * 0.1)
        box_width = int(width * 0.4)

        overlay = frame.copy()
        alpha = 0.7

        box_x2 = width - 10
        box_x1 = box_x2 - box_width
        box_y2 = height - 10
        box_y1 = box_y2 - box_height

        cv2.rectangle(
            img=overlay,
            pt1=(box_x1, box_y1),
            pt2=(box_x2, box_y2),
            color=(255, 255, 255),
            thickness=cv2.FILLED,
        )
        cv2.addWeighted(
            src1=overlay, alpha=alpha, src2=frame, beta=1 - alpha, gamma=0, dst=frame
        )

        lines = [
            f"Team A: {team_a_rate:.1f}% ball control",
            f"Team B: {team_b_rate:.1f}% ball control",
        ]
        line_height = int((box_height - 10) / len(lines))

        text_x = box_x1 + 10
        text_y = box_y1 + line_height

        for i, line in enumerate(lines):
            put_text(img=frame, text=line, org=(text_x, text_y + i * line_height))

        return frame
