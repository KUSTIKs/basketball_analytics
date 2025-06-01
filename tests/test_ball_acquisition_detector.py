from trackers.ball_acquisition_detector import BallAcquisitionDetector
from trackers.ball_tracker import BallTrackMeta, BallTrackT
from trackers.player_tracker import PlayerTrackT, PlayerTrackMeta


def test_get_best_candidate_containment():
    detector = BallAcquisitionDetector()
    ball_bbox = (10, 10, 20, 20)
    player_track: PlayerTrackT = {
        1: PlayerTrackMeta(bbox=(9, 9, 21, 21)),
        2: PlayerTrackMeta(bbox=(30, 30, 40, 40)),
    }

    assert detector.get_best_candidate(ball_bbox, player_track) == 1


def test_get_best_candidate_distance():
    detector = BallAcquisitionDetector()
    ball_bbox = (10, 10, 20, 20)
    player_track: PlayerTrackT = {
        1: PlayerTrackMeta(bbox=(100, 100, 110, 110)),
        2: PlayerTrackMeta(bbox=(21, 10, 31, 20)),
    }

    assert detector.get_best_candidate(ball_bbox, player_track) == 2


def test_get_ball_acquirers_streak():
    detector = BallAcquisitionDetector()
    frames_to_confirm = detector.MIN_FRAMES_TO_CONFIRM
    ball_tracks: list[BallTrackT] = [
        BallTrackMeta(bbox=(9, 9, 21, 21)) for _ in range(frames_to_confirm * 2)
    ]
    player_tracks = [
        {1: PlayerTrackMeta(bbox=(9, 9, 21, 21))} for _ in range(frames_to_confirm * 2)
    ]

    result = detector.get_ball_acquirers(ball_tracks, player_tracks)
    assert result[: frames_to_confirm - 1] == [None] * (frames_to_confirm - 1)
    assert result[frames_to_confirm - 1 :] == [1] * (
        len(result) - (frames_to_confirm - 1)
    )
