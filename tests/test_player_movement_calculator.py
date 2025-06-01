from trackers.player_movement_calculator import PlayerMovementCalculator, MovementRecord
from unittest.mock import patch


def test_get_movement_stats_basic():
    calc = PlayerMovementCalculator(fps=10)

    player_positions = [
        {1: (0.0, 0.0), 2: (1.0, 1.0)},
        {1: (1.0, 0.0), 2: (2.0, 1.0)},
        {1: (2.0, 0.0), 2: (3.0, 1.0)},
    ]
    stats = calc.get_movement_stats(player_positions)

    assert stats[0][1]["distance_delta"] == 0
    assert stats[0][2]["distance_delta"] == 0

    assert stats[1][1]["distance_delta"] == 1
    assert stats[1][2]["distance_delta"] == 1

    assert stats[2][1]["distance_delta"] == 1
    assert stats[2][2]["distance_delta"] == 1


def test_get_movement_stats_speed():
    with patch.object(PlayerMovementCalculator, "FRAMES_FOR_SPEED_CALCULATION", 2):
        calc = PlayerMovementCalculator(fps=10)
        player_positions = [
            {1: (0.0, 0.0)},
            {1: (1.0, 0.0)},
            {1: (3.0, 0.0)},
            {1: (6.0, 0.0)},
        ]
        stats = calc.get_movement_stats(player_positions)

        print(stats)

        assert stats[3][1]["speed"] == 30
        assert stats[1][1]["speed"] == 0


def test_get_movement_stats_missing_player():
    calc = PlayerMovementCalculator(fps=10)
    player_positions = [
        {1: (0.0, 0.0)},
        {},
        {1: (1.0, 0.0)},
    ]
    stats = calc.get_movement_stats(player_positions)

    assert 1 not in stats[1]
    assert stats[2][1]["distance_delta"] == 0
