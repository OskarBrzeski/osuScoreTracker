import csv
import os
import sqlite3 as sql
from datetime import datetime, timezone
from functools import wraps
from typing import Callable

from ossapi import Score
from ossapi.ossapi import Beatmap as BeatmapV1


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
            ranked_type INTEGER,
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
        beatmap.approved,
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
        INSERT OR IGNORE INTO maps VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
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
    for i in range(len(maps) // 1000 + 1):
        for m in maps[i * 1000 : (i + 1) * 1000]:
            add_map(_beatmapv1_into_table_record(m))
        print(f"{min((i+1) * 1000, len(maps))} maps added to database")


@auto_connection
def get_latest_leaderboard_map(cursor: sql.Cursor) -> datetime:
    """Get the datetime of the latest leaderboard map in the `maps` table"""
    timestamp = cursor.execute(
        """
        SELECT ranked_time FROM maps
        ORDER BY ranked_time DESC LIMIT 1;
        """
    ).fetchone()[0]

    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


@auto_connection
def get_latest_ranked_map(cursor: sql.Cursor) -> datetime:
    """Get the datetime of the latest leaderboard map in the `maps` table"""
    timestamp = cursor.execute(
        """
        SELECT ranked_time FROM maps
        WHERE ranked_type = 1 OR ranked_type = 2
        ORDER BY ranked_time DESC LIMIT 1;
        """
    ).fetchone()[0]

    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


@auto_connection
def get_all_map_ids_without_score(cursor: sql.Cursor) -> list[int]:
    map_ids = cursor.execute(
        """
        SELECT map_id FROM maps;
        """
    ).fetchall()

    score_map_ids = cursor.execute(
        """
        SELECT map_id FROM scores
        WHERE score > 0;
        """
    ).fetchall()

    difference = set(row[0] for row in map_ids) - set(row[0] for row in score_map_ids)
    return sorted(list(difference))


@auto_connection
def get_map_ids_for_year(cursor: sql.Cursor, year: int) -> list[int]:
    year_timestamp = int(datetime(year, 1, 1).timestamp())
    next_year_timestamp = int(datetime(year + 1, 1, 1).timestamp())
    map_ids = cursor.execute(
        """
        SELECT map_id FROM maps
        WHERE ranked_time BETWEEN ? AND ?
        ORDER BY map_id ASC;
        """,
        (year_timestamp, next_year_timestamp - 1),
    ).fetchall()

    return [row[0] for row in map_ids]


@auto_connection
def get_map_count(cursor: sql.Cursor) -> int:
    result = cursor.execute(
        """
        SELECT COUNT(*) FROM maps;
        """
    ).fetchone()

    return result[0]


@auto_connection
def create_score_table(cursor: sql.Cursor):
    """Create the table `scores` with all the relevant columns.

    Changes should also be made to _score_into_table_record()"""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scores (
            score_id INTEGER,
            user_id INTEGER,
            map_id INTEGER,
            score INTEGER,
            accuracy REAL,
            max_combo INTEGER,
            mods INTEGER,
            submit_time INTEGER,
            pp REAL,
            PRIMARY KEY (user_id, map_id)
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
        INSERT OR IGNORE INTO scores VALUES (
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


@auto_connection
def get_score_count(cursor: sql.Cursor) -> int:
    result = cursor.execute(
        """
        SELECT COUNT(*) FROM scores
        WHERE score > 0;
        """
    ).fetchone()

    return result[0]


@auto_connection
def export_scores_as_csv(cursor: sql.Cursor, user_id: int) -> None:
    """Creates a CSV file with all stored scores of particular player."""
    scores = cursor.execute(
        """
        SELECT * FROM scores
        WHERE user_id = ?;
        """,
        (user_id,),
    ).fetchall()

    if not os.path.isdir("export"):
        os.mkdir("export")

    with open(f"export/scores-{user_id}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Score ID",
                "User ID",
                "Map ID",
                "Score",
                "Accuracy",
                "Combo",
                "Mods",
                "Time Submitted",
                "pp",
            )
        )
        writer.writerows(scores)


def import_scores_from_csv(csv_path: str) -> None:
    """Adds scores from CSV file into database."""
    with open(csv_path) as file:
        reader = csv.reader(file)
        for row in reader[1:]:
            add_score(tuple(row))
