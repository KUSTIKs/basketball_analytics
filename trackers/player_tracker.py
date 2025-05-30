from typing import Final, TypedDict
import supervision as sv
from ultralytics import YOLO
from ultralytics.engine.results import Results

from common_types import FrameT, RectCoordsT
from constants import YOLOClassName
from utils.cache_utils import file_cache
from utils.common_utils import invert_dict

type PlayerTrackT = dict[int, PlayerTrackMeta]


class PlayerTracker:
    CONFIDENCE: Final = 0.5

    model: YOLO
    tracker: sv.ByteTrack
    yolo_id: int

    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()

        self.yolo_id = invert_dict(self.model.names)[YOLOClassName.PLAYER]

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
        tracks: list[PlayerTrackT] = []

        for frame_detections in frames_detections:
            sv_frame_detections = sv.Detections.from_ultralytics(frame_detections)
            tracked_frame_detections = self.tracker.update_with_detections(
                sv_frame_detections
            )

            track: PlayerTrackT = {}

            for frame_detection in tracked_frame_detections:
                bbox = frame_detection[0].tolist()
                class_id = frame_detection[3]
                track_id = frame_detection[4]

                if (
                    class_id != self.yolo_id
                    or bbox is None
                    or track_id is None
                    or class_id is None
                ):
                    continue

                track[track_id] = PlayerTrackMeta(bbox=bbox)

            tracks.append(track)

        return tracks


class PlayerTrackMeta(TypedDict):
    bbox: RectCoordsT
