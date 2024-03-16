from ossapi import BeatmapUserScore, GameMode, Score

from score_tracker.controllers.api import API
from score_tracker.controllers.utils import rate_limit
from score_tracker.models.scores import add_score


@rate_limit
def _beatmap_user_score(map_id: int, user_id: int, mode: GameMode) -> BeatmapUserScore:
    """Rate-limited variant of `Ossapi.beatmap_user_score`."""
    return API.beatmap_user_score(map_id, user_id, mode=mode)


def get_score(map_id: int, user_id: int) -> Score | tuple[int, int]:
    """Retrieves a user's best score on a beatmap."""
    try:
        return _beatmap_user_score(map_id, user_id, mode=GameMode.OSU).score
    except ValueError:
        return (user_id, map_id)


def fill_score_table(scores: list[Score | tuple[int, int]]) -> None:
    """Add score data to table `scores`"""
    for score in scores:
        add_score(score)
