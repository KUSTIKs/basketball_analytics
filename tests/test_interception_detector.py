from trackers.interception_detector import InterceptionDetector
from constants import TeamNumber


def test_get_passes_and_interceptions_basic():
    detector = InterceptionDetector()
    acquirers: list[int | None] = [1, 1, 2, 3, 2, None, 2]
    teams: list[dict[int, TeamNumber]] = [
        {1: TeamNumber.A, 2: TeamNumber.A, 3: TeamNumber.B},
        {1: TeamNumber.A, 2: TeamNumber.A, 3: TeamNumber.B},
        {1: TeamNumber.A, 2: TeamNumber.A, 3: TeamNumber.B},
        {1: TeamNumber.A, 2: TeamNumber.A, 3: TeamNumber.B},
        {1: TeamNumber.A, 2: TeamNumber.A, 3: TeamNumber.B},
        {1: TeamNumber.A, 2: TeamNumber.A, 3: TeamNumber.B},
        {1: TeamNumber.A, 2: TeamNumber.A, 3: TeamNumber.B},
    ]
    passes, interceptions = detector.get_passes_and_interceptions(acquirers, teams)

    assert passes == [None, None, TeamNumber.A, None, None, None, None]
    assert interceptions == [None, None, None, TeamNumber.B, TeamNumber.A, None, None]


def test_get_passes_and_interceptions_none_cases():
    detector = InterceptionDetector()
    acquirers: list[int | None] = [None, 1, None, 2]
    teams: list[dict[int, TeamNumber]] = [
        {1: TeamNumber.A, 2: TeamNumber.B},
        {1: TeamNumber.A, 2: TeamNumber.B},
        {1: TeamNumber.A, 2: TeamNumber.B},
        {1: TeamNumber.A, 2: TeamNumber.B},
    ]
    passes, interceptions = detector.get_passes_and_interceptions(acquirers, teams)

    assert passes == [None, None, None, None]
    assert interceptions == [None, None, None, None]
