from typing import Final
from ultralytics import YOLO
from ultralytics.engine.results import Results

from common_types import FrameT
from utils.cache_utils import file_cache


class CourtKeypointsDetector:
    CONFIDENCE: Final = 0.5

    model: YOLO

    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    @file_cache()
    def get_keypoints(self, frames: list[FrameT]):
        BATCH_SIZE: Final = 20
        frames_detections: list[Results] = []

        for i in range(0, len(frames), BATCH_SIZE):
            frames_batch = frames[i : i + BATCH_SIZE]
            batch_detections = self.model.predict(
                source=frames_batch, conf=self.CONFIDENCE
            )

            frames_detections.extend(batch_detections)

        return frames_detections
