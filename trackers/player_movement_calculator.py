from typing import TypedDict
from trackers.player_tracker import PlayerTrackT
from utils.geometry_utils import get_point_distance


class PlayerMovementCalculator:
    FRAMES_FOR_SPEED_CALCULATION: int = 5

    fps: int

    def __init__(self, fps: int = 30):
        self.fps = fps

    def get_movement_stats(
        self, player_positions: list[dict[int, tuple[float, float]]]
    ):
        movement_stats: list[dict[int, MovementRecord]] = []
        frames_count = len(player_positions)

        for frame_index in range(frames_count):
            frame_player_positions = player_positions[frame_index]
            frame_movements: dict[int, MovementRecord] = {}

            for player_id, position in frame_player_positions.items():
                speed = 0
                distance_delta = 0

                if frame_index != 0 and player_id in movement_stats[frame_index - 1]:
                    previous_position = movement_stats[frame_index - 1][player_id].get(
                        "position"
                    )

                    distance_delta = get_point_distance(previous_position, position)

                if frame_index >= self.FRAMES_FOR_SPEED_CALCULATION:
                    stats_slice = movement_stats[
                        frame_index
                        - self.FRAMES_FOR_SPEED_CALCULATION : frame_index
                        + 1
                    ]
                    distance_moved = (
                        sum(
                            [
                                record.get(player_id, {}).get("distance_delta", 0)
                                for record in stats_slice
                            ]
                        )
                        + distance_delta
                    )

                    speed = (
                        distance_moved / self.FRAMES_FOR_SPEED_CALCULATION * self.fps
                    )

                frame_movements[player_id] = MovementRecord(
                    player_id=player_id,
                    distance_delta=distance_delta,
                    speed=speed,
                    position=position,
                )

            movement_stats.append(frame_movements)

        return movement_stats


class MovementRecord(TypedDict):
    player_id: int
    distance_delta: float
    speed: float
    position: tuple[float, float]
