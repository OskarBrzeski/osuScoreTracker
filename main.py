from datetime import datetime, timezone

import src.api as api
import src.database as db

if __name__ == "__main__":
    db.delete_map_table()
    db.create_map_table()

    maps = api.get_all_leaderboard_maps(upto=datetime(2008, 1, 1, tzinfo=timezone.utc))

    for m in maps:
        db.add_map(api.beatmapv1_into_table_record(m))

    db.remove_all_maps()
