import argparse
import os
from pathlib import Path

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
from trackers.player_movement_calculator import PlayerMovementCalculator
from trackers.player_tracker import PlayerTracker
from utils.diagram_converter import DiagramConverter
from utils.models_utils import download_models
from utils.team_assigner import TeamAssigner
from utils.video_utils import read_video, save_video


def parse_args():
    parser = argparse.ArgumentParser(description="Process basketball video.")
    parser.add_argument(
        "input_video",
        type=str,
        nargs="?",
        default=constants.INPUT_VIDEO,
        help="Path to the input video file.",
    )
    parser.add_argument(
        "--output-video",
        type=str,
        dest="output_video",
        default=constants.OUTPUT_VIDEO,
        help="Path to save the output video file.",
    )
    parser.add_argument(
        "--team-a-class",
        dest="team_a_class",
        type=str,
        default="Dark blue shirt",
    )
    parser.add_argument(
        "--team-b-class",
        dest="team_b_class",
        type=str,
        default="White shirt",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    download_models()

    if not os.path.exists(args.input_video):
        raise FileNotFoundError(
            f"Input video file '{args.input_video}' does not exist."
        )

    Path(args.output_video).parent.mkdir(parents=True, exist_ok=True)

    video_frames = read_video(args.input_video)

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
        team_a_class=args.team_a_class,
        team_b_class=args.team_b_class,
    )
    ball_acquisition_detector = BallAcquisitionDetector()
    interception_detector = InterceptionDetector()
    diagram_converter = DiagramConverter()
    player_movement_calculator = PlayerMovementCalculator()

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
    movement_stats = player_movement_calculator.get_movement_stats(player_positions)

    result = player_tracks_drawer.draw(
        video_frames, player_tracks, teams, ball_acquirers, movement_stats
    )
    result = ball_tracks_drawer.draw(result, ball_tracks)
    result = ball_controll_drawer.draw(result, teams, ball_acquirers)
    result = interception_drawer.draw(result, passes, interceptions)
    result = court_keypoints_drawer.draw(result, court_keypoints)
    result = diagram_drawer.draw(result, player_positions, teams, ball_acquirers)

    save_video(result, args.output_video)

    print(f"Processed video saved to: {args.output_video}")


if __name__ == "__main__":
    main()
