from common_types import FrameT
from trackers.ball_tracker import BallTrackT
from utils.drawing_utils import draw_triangle


class BallTracksDrawer:
    pointer_color = (0, 255, 0)

    def draw(self, video_frames: list[FrameT], tracks: list[BallTrackT]):
        result_frames: list[FrameT] = []

        for i, frame in enumerate(video_frames):
            frame = frame.copy()
            ball_track = tracks[i]

            if ball_track is None:
                result_frames.append(frame)
                continue

            meta = ball_track

            frame = draw_triangle(
                frame=frame,
                bbox=meta.get("bbox"),
                color=self.pointer_color,
            )

            result_frames.append(frame)

        return result_frames
