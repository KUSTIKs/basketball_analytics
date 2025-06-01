import numpy as np
from unittest.mock import patch, MagicMock
from constants import YOLOClassName
from trackers.ball_tracker import BallTracker, BallTrackMeta, BallTrackT


def test_detect_frames_calls_model_predict():
    dummy_frames: list[np.ndarray] = [
        np.zeros((10, 10, 3), dtype=np.uint8) for _ in range(5)
    ]
    dummy_results = ["result1", "result2", "result3", "result4", "result5"]

    with patch("trackers.ball_tracker.YOLO") as MockYOLO:
        mock_model = MockYOLO.return_value
        mock_model.names = {0: YOLOClassName.BALL}
        mock_model.predict.return_value = dummy_results

        tracker = BallTracker("dummy_path.pt")
        results = tracker.detect_frames(dummy_frames)

        mock_model.predict.assert_called()
        assert results == dummy_results


def test_get_object_tracks_returns_tracks():
    dummy_frames: list[np.ndarray] = [np.zeros((10, 10, 3), dtype=np.uint8)]
    dummy_detection = MagicMock()
    dummy_bbox = np.array([1.0, 2.0, 3.0, 4.0])
    dummy_confidence = 0.9
    dummy_class_id = 0

    with patch("trackers.ball_tracker.YOLO") as MockYOLO, patch(
        "trackers.ball_tracker.sv.Detections.from_ultralytics"
    ) as mock_from_ultralytics:

        mock_model = MockYOLO.return_value
        mock_model.names = {0: YOLOClassName.BALL}
        mock_model.predict.return_value = [dummy_detection]
        mock_from_ultralytics.return_value = [
            [dummy_bbox, None, dummy_confidence, dummy_class_id]
        ]

        tracker = BallTracker("dummy_path.pt")
        tracker.yolo_id = dummy_class_id

        tracks = tracker.get_object_tracks(dummy_frames)
        assert isinstance(tracks, list)
        assert isinstance(tracks[0], dict)
        assert tracks[0]["bbox"] == dummy_bbox.tolist()


def test_remove_wrong_tracks_removes_far_tracks():
    tracker = BallTracker.__new__(BallTracker)

    tracks: list[BallTrackT] = [
        BallTrackMeta(bbox=(0.0, 0.0, 1.0, 1.0)),
        BallTrackMeta(bbox=(100.0, 100.0, 101.0, 101.0)),
    ]
    cleaned = tracker.remove_wrong_tracks(tracks.copy())
    assert cleaned[1] is None


def test_interpolate_tracks_fills_missing():
    tracker = BallTracker.__new__(BallTracker)
    tracks: list[BallTrackT] = [
        BallTrackMeta(bbox=(0.0, 0.0, 1.0, 1.0)),
        None,
        BallTrackMeta(bbox=(2.0, 2.0, 3.0, 3.0)),
    ]
    interpolated = tracker.interpolate_tracks(tracks)
    assert all(isinstance(t, dict) for t in interpolated)
    assert interpolated[1] is not None
    assert interpolated[1]["bbox"] == [1.0, 1.0, 2.0, 2.0]
