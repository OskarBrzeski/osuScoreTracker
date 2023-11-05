import os
from datetime import datetime, timedelta, timezone
from time import time
from typing import Callable, Final, Type

from dotenv import load_dotenv
from ossapi import BeatmapUserScore, GameMode, Ossapi, OssapiV1, Score, User
from ossapi.ossapi import Beatmap as BeatmapV1

load_dotenv(".env")
API_LEGACY_KEY: Final[str] = os.environ.get("LEGACY_OSU_API_KEY")
API_CLIENT_ID: Final[int] = int(os.environ.get("CLIENT_ID"))
API_CLIENT_SECRET: Final[str] = os.environ.get("CLIENT_SECRET")


API_V1 = OssapiV1(API_LEGACY_KEY)
API = Ossapi(API_CLIENT_ID, API_CLIENT_SECRET)


last_call_time = time()


def rate_limit(func: Callable, return_type: Type) -> Callable:
    """Decorator for rate limiting api calls."""

    def wrapper(*args, **kwargs) -> return_type:
        global last_call_time

        while time() - last_call_time < 1:
            continue

        last_call_time = time()
        result = func(*args, **kwargs)

        return result

    return wrapper


_limited_get_beatmaps = rate_limit(API_V1.get_beatmaps, return_type=list[BeatmapV1])


def get_leaderboard_maps(
    since: datetime = datetime(2007, 1, 1, tzinfo=timezone.utc),
    upto: datetime = datetime.now(timezone.utc) + timedelta(days=1),
) -> list[BeatmapV1]:
    """Retrieves all maps approved between `since` and `upto` (UTC)"""

    maps: list[BeatmapV1] = []
    map_id_set: set[int] = set()

    while retrieved := _limited_get_beatmaps(since=since):
        prev_len = len(maps)

        for map in retrieved:
            if map.beatmap_id in map_id_set:
                continue
            if map.mode != 0:
                continue
            if map.approved_date > upto:
                return maps

            maps.append(map)
            map_id_set.add(map.beatmap_id)

        if len(maps) == prev_len:
            break

        since = maps[-1].approved_date - timedelta(seconds=1)
        print(f"Retrieved maps up to {since}: {len(maps)}")

    return maps


_limited_beatmap_user_score = rate_limit(
    API.beatmap_user_score, return_type=BeatmapUserScore
)


def get_score(map_id: int, user_id: int) -> Score | tuple[int, int]:
    """Retrieves a user's best score on a beatmap."""
    try:
        return _limited_beatmap_user_score(map_id, user_id, mode=GameMode.OSU).score
    except ValueError as e:
        return (user_id, map_id)


_limited_user = rate_limit(API.user, return_type=User)


def user_exists(user_id: int) -> bool:
    return _limited_user(user_id).id == user_id
