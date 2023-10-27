import sqlite3 as sql


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
    
    Changes should also be made to src.api.beatmapv1_into_table_record()"""
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
