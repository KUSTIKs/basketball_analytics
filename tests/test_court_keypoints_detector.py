import numpy as np
from unittest.mock import patch
from trackers.court_keypoints_detector import CourtKeypointsDetector


def test_get_keypoints_calls_model_predict():
    dummy_frames: list[np.ndarray] = [
        np.zeros((10, 10, 3), dtype=np.uint8) for _ in range(5)
    ]
    dummy_results = ["result1", "result2", "result3", "result4", "result5"]

    with patch("trackers.court_keypoints_detector.YOLO") as MockYOLO:
        mock_model = MockYOLO.return_value
        mock_model.predict.return_value = dummy_results

        detector = CourtKeypointsDetector("dummy_path.pt")
        results = detector.get_keypoints(dummy_frames)

        mock_model.predict.assert_called()
        assert results == dummy_results
