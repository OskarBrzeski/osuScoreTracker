from datetime import datetime, timezone

import src.api as api
import src.database as db

if __name__ == "__main__":
    db.delete_map_table()
    db.create_map_table()
