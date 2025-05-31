from typing import Final
import supervision as sv
from ultralytics.engine.results import Results

from common_types import FrameT


class CourtKeypointsDrawer:
    COLOR: Final = (255, 100, 0)
    vertex_anotator: sv.VertexAnnotator
    vertext_label_anotator: sv.VertexLabelAnnotator

    def __init__(self):
        self.vertex_anotator = sv.VertexAnnotator(
            color=sv.Color.from_rgb_tuple(self.COLOR),
            radius=5,
        )

        self.vertext_label_anotator = sv.VertexLabelAnnotator(
            color=sv.Color.from_rgb_tuple(self.COLOR),
            text_color=sv.Color.WHITE,
            text_scale=0.5,
            text_thickness=1,
        )

    def draw(
        self,
        frames: list[FrameT],
        keypoints: list[Results],
    ):
        result_frames: list[FrameT] = []

        for i, frame in enumerate(frames):
            frame = frame.copy()
            keypoint_list = keypoints[i]
            sv_keypoints = sv.KeyPoints.from_ultralytics(keypoint_list)

            self.vertex_anotator.annotate(
                scene=frame,
                key_points=sv_keypoints,
            )
            self.vertext_label_anotator.annotate(
                scene=frame,
                key_points=sv_keypoints,
            )

            result_frames.append(frame)

        return result_frames
