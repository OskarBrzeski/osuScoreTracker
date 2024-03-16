import sqlite3 as sql

from score_tracker.models.utils import auto_connection


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


@auto_connection
def delete_map_table(cursor: sql.Cursor) -> None:
    """Delete the table `maps`"""
    cursor.execute(
        """
        DROP TABLE IF EXISTS maps;
        """
    )


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


@auto_connection
def delete_score_table(cursor: sql.Cursor):
    """Delete the table `scores`"""
    cursor.execute(
        """
        DROP TABLE IF EXISTS scores;
        """
    )
