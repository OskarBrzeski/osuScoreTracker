from ossapi import User

from score_tracker.controllers.api import API
from score_tracker.controllers.utils import rate_limit


@rate_limit
def _user(user_id: int) -> User:
    """Rate-limited variant of `Ossapi.user`."""
    return API.user(user_id)


def user_exists(user_id: int) -> bool:
    return _user(user_id).id == user_id
