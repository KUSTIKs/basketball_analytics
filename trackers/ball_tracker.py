import math
from typing import Final, TypedDict
import pandas as pd
import supervision as sv
from ultralytics import YOLO
from ultralytics.engine.results import Results

from common_types import FrameT
from constants import YOLOClassName
from utils.cache_utils import file_cache
from utils.common_utils import invert_dict
from utils.drawing_utils import get_bbox_center

type BallTrackT = BallTrackMeta | None


class BallTracker:
    model: YOLO
    tracker: sv.ByteTrack
    yolo_id: int

    CONFIDENCE: Final = 0.5

    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()

        self.yolo_id = invert_dict(self.model.names)[YOLOClassName.BALL]

    def detect_frames(self, frames: list[FrameT]):
        BATCH_SIZE: Final = 20
        frames_detections: list[Results] = []

        for i in range(0, len(frames), BATCH_SIZE):
            frames_batch = frames[i : i + BATCH_SIZE]
            batch_detections = self.model.predict(
                source=frames_batch, conf=self.CONFIDENCE
            )

            frames_detections.extend(batch_detections)

        return frames_detections

    @file_cache()
    def get_object_tracks(self, frames: list[FrameT]):
        frames_detections = self.detect_frames(frames)
        tracks: list[BallTrackT] = []

        for frame_detections in frames_detections:
            sv_frame_detections = sv.Detections.from_ultralytics(
                frame_detections,
            )

            track: BallTrackT = None
            max_confidence = 0

            for frame_detection in sv_frame_detections:
                bbox = frame_detection[0].tolist()
                class_id = frame_detection[3]
                confidence = frame_detection[2]

                if (
                    class_id != self.yolo_id
                    or bbox is None
                    or confidence is None
                    or confidence <= max_confidence
                ):
                    continue

                max_confidence = confidence
                track = BallTrackMeta(bbox=bbox)
                break

            tracks.append(track)

        return tracks

    def remove_wrong_tracks(self, tracks: list[BallTrackT]):
        MAX_DISTANCE_PER_FRAME: Final = 25
        last_detection_index: int | None = None

        for i, track in enumerate(tracks):
            if track is None:
                continue

            bbox = track.get("bbox")
            if bbox is None:
                continue

            if (
                last_detection_index is None
                or (last_detection := tracks[last_detection_index]) is None
            ):
                last_detection_index = i
                continue

            last_ball_bbox = last_detection.get("bbox")

            new_ball_position = get_bbox_center(bbox)
            last_ball_position = get_bbox_center(last_ball_bbox)
            distance = math.hypot(
                new_ball_position[0] - last_ball_position[0],
                new_ball_position[1] - last_ball_position[1],
            )

            frames_passed = i - last_detection_index
            max_distance = MAX_DISTANCE_PER_FRAME * frames_passed

            if distance > max_distance:
                tracks[i] = None
            else:
                last_detection_index = i

        return tracks

    def interpolate_tracks(self, tracks: list[BallTrackT]):
        positions = [{} if track is None else track.get("bbox") for track in tracks]

        df_positions = pd.DataFrame(positions, columns=["x1", "y1", "x2", "y2"])
        df_positions.interpolate(method="linear", inplace=True)
        df_positions.fillna("ffill", inplace=True)
        df_positions.fillna("bfill", inplace=True)

        updated_tracks: list[BallTrackT] = [
            BallTrackMeta(bbox=position) for position in df_positions.values.tolist()
        ]

        return updated_tracks


class BallTrackMeta(TypedDict):
    bbox: list[float]
