from datetime import datetime, timedelta, timezone
from typing import Final
import os

from dotenv import load_dotenv
import ossapi
from ossapi.ossapi import Beatmap as BeatmapV1


load_dotenv(".env")
API_LEGACY_KEY: Final[str] = os.environ.get("LEGACY_OSU_API_KEY")
API_CLIENT_ID: Final[int] = int(os.environ.get("CLIENT_ID"))
API_CLIENT_SECRET: Final[str] = os.environ.get("CLIENT_SECRET")


API_V1 = ossapi.OssapiV1(API_LEGACY_KEY)


def get_all_leaderboard_maps(
        since: datetime = datetime(2007, 1, 1, tzinfo=timezone.utc),
        upto: datetime = datetime.now(timezone.utc) + timedelta(days=1),
    ) -> list[BeatmapV1]:

    maps: list[BeatmapV1] = []
    map_id_set: set[int] = set()

    while (retrieved := API_V1.get_beatmaps(since=since)):
        for map in retrieved:
            if map.beatmap_id in map_id_set: continue
            if map.approved_date > upto: return maps

            maps.append(map)
            map_id_set.add(map.beatmap_id)
        
        since = maps[-1].approved_date - timedelta(seconds=1)
    
    return maps
