import constants
from drawers.ball_tracks_drawer import BallTracksDrawer
from drawers.diagram_drawer import DiagramDrawer
from drawers.court_keypoints_drawer import CourtKeypointsDrawer
from drawers.interception_drawer import InterceptionDrawer
from drawers.player_tracks_drawer import PlayerTracksDrawer
from drawers.ball_controll_drawer import BallControllDrawer
from trackers.ball_acquisition_detector import BallAcquisitionDetector
from trackers.ball_tracker import BallTracker
from trackers.court_keypoints_detector import CourtKeypointsDetector
from trackers.interception_detector import InterceptionDetector
from trackers.player_tracker import PlayerTracker
from utils.diagram_converter import DiagramConverter
from utils.team_assigner import TeamAssigner
from utils.video_utils import read_video, save_video
import supervision as sv


def main():
    video_frames = read_video(constants.INPUT_VIDEO)

    player_tracker = PlayerTracker(model_path=constants.PLAYER_MODEL)
    ball_tracker = BallTracker(model_path=constants.BALL_MODEL)
    court_keypoints_detector = CourtKeypointsDetector(
        model_path=constants.COURT_KEYPOINT_MODEL
    )
    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    ball_controll_drawer = BallControllDrawer()
    interception_drawer = InterceptionDrawer()
    court_keypoints_drawer = CourtKeypointsDrawer()
    diagram_drawer = DiagramDrawer()
    team_assigner = TeamAssigner(
        team_a_class="Dark blue shirt",
        team_b_class="White shirt",
    )
    ball_acquisition_detector = BallAcquisitionDetector()
    interception_detector = InterceptionDetector()
    diagram_converter = DiagramConverter()

    player_tracks = player_tracker.get_object_tracks(video_frames)

    teams = team_assigner.get_teams(video_frames, player_tracks)

    ball_tracks = ball_tracker.get_object_tracks(video_frames)
    ball_tracks = ball_tracker.remove_wrong_tracks(ball_tracks)
    ball_tracks = ball_tracker.interpolate_tracks(ball_tracks)

    ball_acquirers = ball_acquisition_detector.get_ball_acquirers(
        ball_tracks, player_tracks
    )
    passes, interceptions = interception_detector.get_passes_and_interceptions(
        ball_acquirers, teams
    )
    court_keypoints = court_keypoints_detector.get_keypoints(video_frames)
    court_keypoints = diagram_converter.validate_keypoints(court_keypoints)
    player_positions = diagram_converter.project_players(court_keypoints, player_tracks)

    result = player_tracks_drawer.draw(
        video_frames, player_tracks, teams, ball_acquirers
    )
    result = ball_tracks_drawer.draw(result, ball_tracks)
    result = ball_controll_drawer.draw(result, teams, ball_acquirers)
    result = interception_drawer.draw(result, passes, interceptions)
    result = court_keypoints_drawer.draw(result, court_keypoints)
    result = diagram_drawer.draw(result, player_positions, teams, ball_acquirers)

    # for i, frame in enumerate(result):
    #     frame = sv.draw_text(
    #         scene=frame,
    #         text=f"Frame: {i + 1}",
    #         text_anchor=sv.Point(x=frame.shape[1] - 100, y=30),
    #         text_color=sv.Color.WHITE,
    #     )
    #     result[i] = frame

    save_video(result, constants.OUTPUT_VIDEO)


if __name__ == "__main__":
    main()
