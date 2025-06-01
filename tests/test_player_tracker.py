import numpy as np
from unittest.mock import patch, MagicMock
from trackers.player_tracker import PlayerTracker, PlayerTrackMeta, PlayerTrackT
from constants import YOLOClassName


def test_detect_frames_calls_model_predict():
    dummy_frames: list[np.ndarray] = [
        np.zeros((10, 10, 3), dtype=np.uint8) for _ in range(5)
    ]
    dummy_results = ["result1", "result2", "result3", "result4", "result5"]

    with patch("trackers.player_tracker.YOLO") as MockYOLO:
        mock_model = MockYOLO.return_value
        mock_model.names = {0: YOLOClassName.PLAYER}
        mock_model.predict.return_value = dummy_results

        tracker = PlayerTracker("dummy_path.pt")
        results = tracker.detect_frames(dummy_frames)

        mock_model.predict.assert_called()
        assert results == dummy_results


def test_get_object_tracks_returns_tracks():
    dummy_frames: list[np.ndarray] = [np.zeros((10, 10, 3), dtype=np.uint8)]
    dummy_detection = MagicMock()
    dummy_bbox = np.array([1.0, 2.0, 3.0, 4.0])
    dummy_class_id = 0
    dummy_track_id = 42

    with patch("trackers.player_tracker.YOLO") as MockYOLO, patch(
        "trackers.player_tracker.sv.Detections.from_ultralytics"
    ) as mock_from_ultralytics, patch(
        "trackers.player_tracker.sv.ByteTrack.update_with_detections"
    ) as mock_update_with_detections:

        mock_model = MockYOLO.return_value
        mock_model.names = {0: YOLOClassName.PLAYER}
        mock_model.predict.return_value = [dummy_detection]
        mock_from_ultralytics.return_value = [
            [dummy_bbox, None, None, dummy_class_id, dummy_track_id]
        ]
        mock_update_with_detections.return_value = [
            [dummy_bbox, None, None, dummy_class_id, dummy_track_id]
        ]

        tracker = PlayerTracker("dummy_path.pt")
        tracker.yolo_id = dummy_class_id

        tracks = tracker.get_object_tracks(dummy_frames)
        assert isinstance(tracks, list)
        assert isinstance(tracks[0], dict)
        assert tracks[0][dummy_track_id]["bbox"] == dummy_bbox.tolist()
