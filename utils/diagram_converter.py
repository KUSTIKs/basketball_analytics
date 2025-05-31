from copy import deepcopy
import cv2
import numpy as np
import torch
from ultralytics.engine.results import Results, Keypoints
from typing import Final, cast

from trackers.player_tracker import PlayerTrackT
from utils.geometry_utils import get_point_distance, project


class DiagramConverter:
    REAL_WIDTH: Final = 28
    REAL_HEIGHT: Final = 15
    DISTANCE_THRESHOLD: Final = 50

    REAL_KEYPOINTS = [
        (0, 0),
        (0, 0.9),
        (0, 5.2),
        (0, 9.8),
        (0, 14.1),
        (0, 15),
        (14, 15),
        (14, 0),
        (5.8, 5.2),
        (5.8, 9.8),
        (28, 15),
        (28, 14.1),
        (28, 9.8),
        (28, 5.2),
        (28, 0.9),
        (28, 0),
        (22.2, 5.2),
        (22.2, 9.8),
    ]

    @staticmethod
    def get_relative_cordinate(
        real_coordinate: tuple[float, float], width: int, height: int
    ):
        x, y = real_coordinate
        rel_x = (x / DiagramConverter.REAL_WIDTH) * width
        rel_y = (y / DiagramConverter.REAL_HEIGHT) * height

        return (rel_x, rel_y)

    def validate_keypoints(self, keypoints: list[Results]):
        result_keypoints = deepcopy(keypoints)

        for frame_index, frame_keypoints in enumerate(result_keypoints):
            if frame_keypoints.keypoints is None:
                continue

            coords = cast(list[list[float]], frame_keypoints.keypoints.xy.tolist()[0])

            real_points = []
            frame_points = []
            valid_indices = []

            for i, (x, y) in enumerate(coords):
                if x != 0 or y != 0:
                    real_points.append(self.REAL_KEYPOINTS[i])
                    frame_points.append((x, y))
                    valid_indices.append(i)

            if len(valid_indices) < 4:
                continue

            real_points_np = np.array(real_points, dtype=np.float32)
            frame_points_np = np.array(frame_points, dtype=np.float32)
            H, _ = cv2.findHomography(
                real_points_np, frame_points_np, method=cv2.RANSAC
            )

            if H is None:
                continue

            for i in valid_indices:
                real_point = self.REAL_KEYPOINTS[i]
                projected_point = project(real_point, H)
                err = get_point_distance(coords[i], projected_point)

                if err > self.DISTANCE_THRESHOLD:
                    coords[i] = [0.0, 0.0]

            frame_keypoints.keypoints.xy[0] = torch.tensor(coords, dtype=torch.float32)

        return result_keypoints

    def project_players(
        self, keypoints: list[Results], player_tracks: list[PlayerTrackT]
    ):
        player_positions: list[dict[int, tuple[float, float]]] = []

        for frame_index, frame_keypoints in enumerate(keypoints):
            if frame_keypoints.keypoints is None:
                player_positions.append({})
                continue

            coords = cast(list[list[float]], frame_keypoints.keypoints.xy.tolist()[0])

            real_points = []
            frame_points = []
            valid_indices = []

            for i, (x, y) in enumerate(coords):
                if x != 0 or y != 0:
                    real_points.append(self.REAL_KEYPOINTS[i])
                    frame_points.append((x, y))
                    valid_indices.append(i)

            if len(valid_indices) < 4:
                player_positions.append({})
                continue

            real_points_np = np.array(real_points, dtype=np.float32)
            frame_points_np = np.array(frame_points, dtype=np.float32)
            H, _ = cv2.findHomography(
                real_points_np, frame_points_np, method=cv2.RANSAC
            )

            if H is None:
                player_positions.append({})
                continue

            H_inv = np.linalg.inv(H.astype(np.float32))

            positions = {}

            players = player_tracks[frame_index]
            for track_id, meta in players.items():
                bbox = meta.get("bbox")
                point = ((bbox[0] + bbox[2]) / 2, bbox[3])

                projected_point = project(point, H_inv)
                positions[track_id] = projected_point

            player_positions.append(positions)

        return player_positions
