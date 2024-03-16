import csv
import os
import sqlite3 as sql

from score_tracker.models.utils import auto_connection
from score_tracker.models.scores import add_score


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
