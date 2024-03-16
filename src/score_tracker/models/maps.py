from datetime import datetime, timezone
import sqlite3 as sql

from ossapi.ossapi import Beatmap as BeatmapV1

from score_tracker.models.utils import auto_connection
from score_tracker.models.utils import beatmapv1_into_table_record


@auto_connection
def add_map(cursor: sql.Cursor, map: BeatmapV1) -> None:
    """Add map details to table `maps`"""
    values = beatmapv1_into_table_record(map)

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
def get_all_map_ids_without_score_in_database(cursor: sql.Cursor) -> list[int]:
    map_ids = cursor.execute(
        """
        SELECT map_id FROM maps;
        """
    ).fetchall()

    score_map_ids = cursor.execute(
        """
        SELECT map_id FROM scores;
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
def get_ranked_map_count(cursor: sql.Cursor) -> int:
    result = cursor.execute(
        """
        SELECT COUNT(*) FROM maps
        WHERE ranked_type BETWEEN 1 AND 2;
        """
    ).fetchone()

    return result[0]
