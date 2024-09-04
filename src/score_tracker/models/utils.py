import sqlite3 as sql
from functools import wraps
from typing import Callable

from ossapi.ossapi import Beatmap as BeatmapV1
from ossapi.models import Score

type BeatmapTuple = tuple[int, int, int, int, str, str, str, str, int, float, int]
type ScoreTuple = tuple[int, int, int, int, float, int, int, int, float]


def auto_connection(func: Callable) -> Callable:
    """Decorator for automating the connection to the database."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = sql.connect("database.sqlite")
        try:
            cursor = connection.cursor()
            result = func(cursor, *args, **kwargs)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()
        return result

    return wrapper


def beatmapv1_into_table_record(beatmap: BeatmapV1) -> BeatmapTuple:
    """Convert `Beatmap` object into record for sqlite table"""
    return (
        beatmap.beatmap_id,
        beatmap.beatmapset_id,
        int(beatmap.approved_date.timestamp()),
        beatmap.approved,
        beatmap.artist,
        beatmap.title,
        beatmap.version,
        beatmap.creator,
        beatmap.creator_id,
        beatmap.star_rating,
        int(beatmap.total_length),
    )


def score_into_table_record(score: Score | tuple[int, int]) -> ScoreTuple:
    """Convert `Score` object into record for sqlite table"""
    # tuple only used when there is no score on map
    if isinstance(score, tuple):
        return 0, score[0], score[1], 0, 0.0, 0, 0, 0, 0.0

    return (
        score.id,
        score.user_id,
        score.beatmap.id,
        score.score,
        score.accuracy,
        score.max_combo,
        score.mods.value,
        int(score.created_at.timestamp()),
        score.pp,
    )
