from sympy import N
from common_types import RectCoordsT
from trackers.ball_tracker import BallTrackT
from trackers.player_tracker import PlayerTrackT
from utils.geometry_utils import (
    get_containment_ratio,
    get_shortest_distance_between_rects,
)


class BallAcquisitionDetector:
    CONTAINMENT_THRESHOLD = 0.5
    DISTANCE_THRESHOLD = 100
    MIN_FRAMES_TO_CONFIRM = 12

    def is_ball_contained(self, ball_bbox: RectCoordsT, player_bbox: RectCoordsT):
        ratio = get_containment_ratio(ball_bbox, player_bbox)

        return ratio > self.CONTAINMENT_THRESHOLD

    def get_best_candidate(self, ball_bbox: RectCoordsT, player_track: PlayerTrackT):
        best_candidate_id: int | None = None
        best_containment_ratio: float | None = None
        best_distance: float | None = None

        for track_id, meta in player_track.items():
            player_bbox = meta.get("bbox")

            containment_ratio = get_containment_ratio(ball_bbox, player_bbox)
            is_unset = best_candidate_id is None

            is_contained = containment_ratio > self.CONTAINMENT_THRESHOLD
            is_better_containment = containment_ratio > (best_containment_ratio or 0)

            if is_contained and (is_unset or is_better_containment):
                best_candidate_id = track_id
                best_containment_ratio = containment_ratio
                continue

            if best_containment_ratio is not None:
                continue

            distance = get_shortest_distance_between_rects(ball_bbox, player_bbox)

            if distance < self.DISTANCE_THRESHOLD and (
                best_distance is None or distance < best_distance
            ):
                best_candidate_id = track_id
                best_distance = distance

        return best_candidate_id

    def get_ball_acquirers(
        self, ball_tracks: list[BallTrackT], player_tracks: list[PlayerTrackT]
    ):
        ball_acquirers: list[int | None] = []
        frames_count = len(ball_tracks)

        streak_counter = 0
        streak_acquirer = None
        active_acquirer = None

        for i in range(frames_count):
            ball_track = ball_tracks[i]
            player_track = player_tracks[i]

            current_acquirer = (
                self.get_best_candidate(ball_track.get("bbox"), player_track)
                if ball_track is not None
                else None
            )

            if current_acquirer == streak_acquirer:
                streak_counter += 1
            else:
                active_acquirer = None
                streak_acquirer = current_acquirer
                streak_counter = 1

            if streak_counter >= self.MIN_FRAMES_TO_CONFIRM:
                active_acquirer = streak_acquirer

            ball_acquirers.append(active_acquirer)

        return ball_acquirers
