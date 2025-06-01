import numpy as np
from unittest.mock import patch

from common_types import FrameT
from utils.team_assigner import TeamAssigner
from constants import TeamNumber
from trackers.player_tracker import PlayerTrackT, PlayerTrackMeta


def test_get_teams_assigns_teams_and_uses_cache():
    frames: list[FrameT] = [np.zeros((100, 100, 3), dtype=np.uint8) for _ in range(3)]
    player_tracks: list[PlayerTrackT] = [
        {
            1: PlayerTrackMeta(bbox=(10, 10, 20, 20)),
            2: PlayerTrackMeta(bbox=(30, 30, 40, 40)),
        },
        {
            1: PlayerTrackMeta(bbox=(11, 10, 21, 20)),
            2: PlayerTrackMeta(bbox=(31, 30, 41, 40)),
        },
        {
            1: PlayerTrackMeta(bbox=(12, 10, 22, 20)),
            2: PlayerTrackMeta(bbox=(32, 30, 42, 40)),
        },
    ]

    assigner = TeamAssigner("red", "blue")

    with patch.object(
        assigner,
        "get_player_team",
        side_effect=[TeamNumber.A, TeamNumber.B],
    ) as mock_get_player_team, patch.object(assigner, "load_model"):
        teams = assigner.get_teams(frames, player_tracks)

    assert teams[0][1] == TeamNumber.A
    assert teams[0][2] == TeamNumber.B
    assert teams[1][1] == TeamNumber.A
    assert teams[1][2] == TeamNumber.B
    assert teams[2][1] == TeamNumber.A
    assert teams[2][2] == TeamNumber.B

    assert mock_get_player_team.call_count == 2
