import sqlite3 as sql

from ossapi import Score
from ossapi.ossapi import Beatmap as BeatmapV1


def auto_connection(func):
    """Decorator for automating the connection to the database."""

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


@auto_connection
def create_map_table(cursor: sql.Cursor) -> None:
    """Create the table `maps` with all the relevant columns.

    Changes should also be made to _beatmapv1_into_table_record()"""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS maps (
            map_id INTEGER PRIMARY KEY,
            set_id INTEGER,
            ranked_time INTEGER,
            artist TEXT,
            title TEXT,
            diff_name TEXT,
            mapper TEXT, 
            mapper_id INTEGER,
            diff_rating REAL,
            length INTEGER
        );
        """
    )


def _beatmapv1_into_table_record(beatmap: BeatmapV1) -> tuple:
    """Convert `Beatmap` object into record for sqlite table"""
    return (
        beatmap.beatmap_id,
        beatmap.beatmapset_id,
        int(beatmap.approved_date.timestamp()),
        beatmap.artist,
        beatmap.title,
        beatmap.version,
        beatmap.creator,
        beatmap.creator_id,
        beatmap.star_rating,
        int(beatmap.total_length),
    )


@auto_connection
def delete_map_table(cursor: sql.Cursor) -> None:
    """Delete the table `maps`"""
    cursor.execute(
        """
        DROP TABLE IF EXISTS maps;
        """
    )


@auto_connection
def add_map(cursor: sql.Cursor, values: tuple) -> None:
    """Add map details to table `maps`"""
    cursor.execute(
        """
        INSERT INTO maps VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        );
        """,
        values,
    )


@auto_connection
def remove_all_maps(cursor: sql.Cursor) -> None:
    """Remove all maps from table `maps`"""
    cursor.execute(
        """
        DELETE FROM maps;
        """
    )


def fill_map_table(maps: list[BeatmapV1]) -> None:
    """Add beatmap data to table `maps`"""
    for m in maps:
        add_map(_beatmapv1_into_table_record(m))


@auto_connection
def create_score_table(cursor: sql.Cursor):
    """Create the table `scores` with all the relevant columns.
    
    Changes should also be made to _score_into_table_record()"""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scores (
            score_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            map_id INTEGER,
            score INTEGER,
            accuracy REAL,
            max_combo INTEGER,
            mods INTEGER,
            submit_time INTEGER,
            pp REAL
        );
    """
    )


def _score_into_table_record(score: Score | tuple[int, int]) -> tuple:
    """Convert `Score` object into record for sqlite table"""
    if isinstance(score, tuple):
        return (0, score[0], score[1], 0, 0.0, 0, 0, 0, 0.0)
    
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


@auto_connection
def delete_score_table(cursor: sql.Cursor):
    """Delete the table `scores`"""
    cursor.execute(
        """
        DROP TABLE IF EXISTS scores;
        """
    )


@auto_connection
def add_score(cursor: sql.Cursor, values: tuple) -> None:
    """Add scroe details to table `scores`"""
    cursor.execute(
        """
        INSERT INTO scores VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        );
        """,
        values,
    )


@auto_connection
def remove_all_scores(cursor: sql.Cursor) -> None:
    """Remove all scores from table `scores`"""
    cursor.execute(
        """
        DELETE FROM scores;
        """
    )


def fill_score_table(scores: list[Score | tuple[int, int]]) -> None:
    """Add score data to table `scores`"""
    for s in scores:
        add_score(_score_into_table_record(s))
