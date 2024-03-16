from datetime import datetime, timezone, timedelta

from ossapi.ossapi import Beatmap as BeatmapV1

from score_tracker.controllers.utils import rate_limit
from score_tracker.controllers.api import API_V1
from score_tracker.models.maps import add_map


@rate_limit
def _get_beatmaps(since: datetime) -> list[BeatmapV1]:
    """Rate-limited variant of `OssapiV1.get_beatmaps`."""
    return API_V1.get_beatmaps(since=since)


def get_leaderboard_maps(
    since: datetime = datetime(2007, 1, 1, tzinfo=timezone.utc),
    upto: datetime = datetime.now(timezone.utc) + timedelta(days=1),
) -> list[BeatmapV1]:
    """Retrieves all maps approved between `since` and `upto` (UTC)"""

    maps: list[BeatmapV1] = []
    map_id_set: set[int] = set()

    while retrieved := _get_beatmaps(since=since):
        prev_len = len(maps)

        for map in retrieved:
            if map.beatmap_id in map_id_set:
                continue
            if map.mode != 0:
                continue
            if map.approved not in ["1", "2", "4"]:
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


def fill_map_table(maps: list[BeatmapV1]) -> None:
    """Add beatmap data to table `maps`"""
    for added, maps_slice in _split_sequence(maps, 1000):
        for map in maps_slice:
            add_map(map)
        print(f"{added} maps added to database")


def _split_sequence(sequence: list, window: int):
    sent = 0
    for i in range(len(sequence) // 1000 + 1):
        current_slice = sequence[i * window : (i + 1) * window]
        sent += len(current_slice)
        yield sent, current_slice
