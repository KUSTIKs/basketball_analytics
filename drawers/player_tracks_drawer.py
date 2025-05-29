from common_types import ColorT, FrameT
from constants import TeamNumber
from trackers.player_tracker import PlayerTrackT
from utils.drawing_utils import draw_ellipse


class PlayerTracksDrawer:
    team_colors: tuple[ColorT, ColorT]

    def __init__(self, team_colors: tuple[ColorT, ColorT] = ((255, 0, 0), (0, 0, 255))):
        self.team_colors = team_colors

    def draw(
        self,
        video_frames: list[FrameT],
        tracks: list[PlayerTrackT],
        teams: list[dict[int, TeamNumber]],
    ):
        result_frames: list[FrameT] = []

        for i, frame in enumerate(video_frames):
            frame = frame.copy()
            player_track = tracks[i]

            for track_id, meta in player_track.items():
                team = teams[i].get(track_id, TeamNumber.A)
                color = self.team_colors[team.value]

                frame = draw_ellipse(
                    frame=frame,
                    bbox=meta.get("bbox"),
                    color=color,
                    track_id=track_id,
                )

            result_frames.append(frame)

        return result_frames
