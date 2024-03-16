import sqlite3 as sql

from ossapi import Score


from score_tracker.models.utils import score_into_table_record, auto_connection


@auto_connection
def add_score(cursor: sql.Cursor, score: Score) -> None:
    """Add scroe details to table `scores`"""
    values = score_into_table_record(score)
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
def get_score_in_database_count(cursor: sql.Cursor) -> int:
    result = cursor.execute(
        """
        SELECT COUNT(*) FROM scores;
        """
    ).fetchone()

    return result[0]
