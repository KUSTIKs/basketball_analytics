from ultralytics import YOLO
import constants
from drawers.ball_tracks_drawer import BallTracksDrawer
from drawers.player_tracks_drawer import PlayerTracksDrawer
from trackers.ball_tracker import BallTracker
from trackers.player_tracker import PlayerTracker
from utils.video_utils import read_video, save_video


def main():
    video_frames = read_video(constants.INPUT_VIDEO)

    player_tracker = PlayerTracker(model_path=constants.PLAYER_MODEL)
    ball_tracker = BallTracker(model_path=constants.BALL_MODEL)
    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()

    player_tracks = player_tracker.get_object_tracks(video_frames)
    ball_tracks = ball_tracker.get_object_tracks(video_frames)

    # result = player_tracks_drawer.draw(video_frames, player_tracks)
    result = ball_tracks_drawer.draw(video_frames, ball_tracks)

    save_video(result, constants.OUTPUT_VIDEO)

    # model = YOLO(model=constants.PLAYER_MODEL)

    # results = model.predict(
    #     source=constants.INPUT_VIDEO, save=True, project="output_videos"
    # )


if __name__ == "__main__":
    main()
