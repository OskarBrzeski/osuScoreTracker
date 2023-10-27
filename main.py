from datetime import datetime, timezone

import src.api as api
import src.database as db

if __name__ == "__main__":
    db.delete_map_table()
    db.create_map_table()

    maps = api.get_all_leaderboard_maps(upto=datetime(2009, 1, 1, tzinfo=timezone.utc))

    db.fill_map_table(maps)

    # db.remove_all_maps()
