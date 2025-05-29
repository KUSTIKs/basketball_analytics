from common_types import FrameT
from trackers.player_tracker import PlayerTrackT
from utils.drawing_utils import draw_ellipse


class PlayerTracksDrawer:
    def draw(self, video_frames: list[FrameT], tracks: list[PlayerTrackT]):
        result_frames: list[FrameT] = []

        for i, frame in enumerate(video_frames):
            frame = frame.copy()
            player_track = tracks[i]

            for track_id, meta in player_track.items():
                frame = draw_ellipse(frame, meta.get("bbox"), (0, 0, 255), track_id)

                result_frames.append(frame)

            result_frames.append(frame)

        return result_frames
