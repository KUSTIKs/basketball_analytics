from ultralytics import YOLO
import constants
from drawers.player_tracks_drawer import PlayerTracksDrawer
from trackers.player_tracker import PlayerTracker
from utils.video_utils import read_video, save_video


def main():
    video_frames = read_video(constants.INPUT_VIDEO)

    player_tracker = PlayerTracker(model_path=constants.PLAYER_MODEL)

    player_tracks = player_tracker.get_object_tracks(video_frames)

    player_tracks_drawer = PlayerTracksDrawer()

    result = player_tracks_drawer.draw(video_frames, player_tracks)

    save_video(result, constants.OUTPUT_VIDEO)


if __name__ == "__main__":
    main()
