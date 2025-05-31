from common_types import ColorT, FrameT
from constants import TeamNumber
from trackers.player_movement_calculator import MovementRecord
from trackers.player_tracker import PlayerTrackT
from utils.drawing_utils import draw_ellipse, draw_triangle, put_text


class PlayerTracksDrawer:
    team_colors: tuple[ColorT, ColorT]

    def __init__(self, team_colors: tuple[ColorT, ColorT] = ((255, 0, 0), (0, 0, 255))):
        self.team_colors = team_colors

    def draw(
        self,
        video_frames: list[FrameT],
        tracks: list[PlayerTrackT],
        teams: list[dict[int, TeamNumber]],
        ball_acquirers: list[int | None],
        movement_stats: list[dict[int, MovementRecord]],
    ):
        result_frames: list[FrameT] = []

        for frame_index, frame in enumerate(video_frames):
            frame = frame.copy()
            player_track = tracks[frame_index]
            ball_acquirer = ball_acquirers[frame_index]
            movements = movement_stats[frame_index]

            for player_id, meta in player_track.items():
                team = teams[frame_index].get(player_id, TeamNumber.A)
                color = self.team_colors[team.value]

                frame = draw_ellipse(
                    frame=frame,
                    bbox=meta.get("bbox"),
                    color=color,
                    track_id=player_id,
                )

                if ball_acquirer == player_id:
                    frame = draw_triangle(
                        frame=frame,
                        bbox=meta.get("bbox"),
                        color=(0, 0, 255),
                    )

                player_movement = movements.get(player_id)
                if player_movement is None:
                    continue

                x1, _, _, y2 = meta.get("bbox")

                speed = player_movement.get("speed", 0)
                text = f"Speed: {speed:.2f} m/s"
                org = (int(x1), int(y2 + 50))

                put_text(
                    img=frame,
                    text=text,
                    org=org,
                    color=(0, 0, 0),
                    font_scale=0.5,
                    thickness=2,
                )

                put_text(
                    img=frame,
                    text=text,
                    org=org,
                    color=(255, 255, 255),
                    font_scale=0.5,
                    thickness=1,
                )

            result_frames.append(frame)

        return result_frames
