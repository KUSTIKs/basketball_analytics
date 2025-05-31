import cv2

from common_types import FrameT
from constants import TeamNumber
from utils.drawing_utils import put_text


class InterceptionDrawer:
    def draw(
        self,
        frames: list[FrameT],
        passes: list[TeamNumber | None],
        interceptions: list[TeamNumber | None],
    ):
        result_frames: list[FrameT] = []

        team_a_passes = 0
        team_b_passes = 0
        team_a_interceptions = 0
        team_b_interceptions = 0

        for i, frame in enumerate(frames):
            frame = frame.copy()
            team_passes = passes[i]
            team_interceptions = interceptions[i]

            if team_passes == TeamNumber.A:
                team_a_passes += 1
            elif team_passes == TeamNumber.B:
                team_b_passes += 1

            if team_interceptions == TeamNumber.A:
                team_a_interceptions += 1
            elif team_interceptions == TeamNumber.B:
                team_b_interceptions += 1

            frame = self.draw_box(
                frame=frame,
                team_a_passes=team_a_passes,
                team_b_passes=team_b_passes,
                team_a_interceptions=team_a_interceptions,
                team_b_interceptions=team_b_interceptions,
            )

            result_frames.append(frame)

        return result_frames

    def draw_box(
        self,
        frame: FrameT,
        team_a_passes: int,
        team_b_passes: int,
        team_a_interceptions: int,
        team_b_interceptions: int,
    ):
        height, width, _ = frame.shape
        box_height = int(height * 0.1)
        box_width = int(width * 0.4)
        overlay = frame.copy()
        alpha = 0.7

        box_x1 = 10
        box_x2 = box_x1 + box_width
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
            f"Team A: {team_a_passes} passes, {team_a_interceptions} interceptions",
            f"Team B: {team_b_passes} passes, {team_b_interceptions} interceptions",
        ]
        line_height = int((box_height - 10) / len(lines))

        text_x = box_x1 + 10
        text_y = box_y1 + line_height

        for i, line in enumerate(lines):
            put_text(img=frame, text=line, org=(text_x, text_y + i * line_height))

        return frame
