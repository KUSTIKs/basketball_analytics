from constants import TeamNumber


class InterceptionDetector:
    def get_passes_and_interceptions(
        self, acquirers: list[int | None], teams: list[dict[int, TeamNumber]]
    ):
        passes: list[TeamNumber | None] = []
        interceptions: list[TeamNumber | None] = []

        for i in range(len(acquirers)):
            current_acquirer = acquirers[i]
            prev_acquirer = acquirers[i - 1] if i > 0 else None

            current_team = teams[i].get(current_acquirer) if current_acquirer else None
            prev_team = teams[i - 1].get(prev_acquirer) if prev_acquirer else None

            if (
                current_acquirer != prev_acquirer
                and current_team == prev_team
                and current_acquirer is not None
            ):
                passes.append(current_team)
            else:
                passes.append(None)

            if (
                current_acquirer != prev_acquirer
                and current_team != prev_team
                and current_acquirer is not None
                and prev_acquirer is not None
            ):
                interceptions.append(current_team)
            else:
                interceptions.append(None)

        return passes, interceptions
