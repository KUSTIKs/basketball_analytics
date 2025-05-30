import constants
from drawers.ball_tracks_drawer import BallTracksDrawer
from drawers.player_tracks_drawer import PlayerTracksDrawer
from drawers.ball_controll_drawer import BallControllDrawer
from trackers.ball_acquisition_detector import BallAcquisitionDetector
from trackers.ball_tracker import BallTracker
from trackers.player_tracker import PlayerTracker
from utils.team_assigner import TeamAssigner
from utils.video_utils import read_video, save_video


def main():
    video_frames = read_video(constants.INPUT_VIDEO)

    player_tracker = PlayerTracker(model_path=constants.PLAYER_MODEL)
    ball_tracker = BallTracker(model_path=constants.BALL_MODEL)
    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    team_assigner = TeamAssigner(
        team_a_class="Dark blue shirt", team_b_class="White shirt"
    )
    ball_acquisition_detector = BallAcquisitionDetector()
    ball_controll_drawer = BallControllDrawer()

    player_tracks = player_tracker.get_object_tracks(video_frames)

    teams = team_assigner.get_teams(video_frames, player_tracks)

    ball_tracks = ball_tracker.get_object_tracks(video_frames)
    ball_tracks = ball_tracker.remove_wrong_tracks(ball_tracks)
    ball_tracks = ball_tracker.interpolate_tracks(ball_tracks)

    ball_acquirers = ball_acquisition_detector.get_ball_acquirers(
        ball_tracks, player_tracks
    )

    result = player_tracks_drawer.draw(
        video_frames, player_tracks, teams, ball_acquirers
    )
    result = ball_tracks_drawer.draw(result, ball_tracks)
    result = ball_controll_drawer.draw(result, teams, ball_acquirers)

    save_video(result, constants.OUTPUT_VIDEO)


if __name__ == "__main__":
    main()
