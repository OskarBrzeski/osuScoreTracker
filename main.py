from datetime import datetime, timezone

import src.api as api

if __name__ == "__main__":
    maps = api.get_all_leaderboard_maps(upto=datetime(2009, 1, 1, tzinfo=timezone.utc))

    for map in maps:
        print(
            f"{map.approved_date} | id={map.beatmap_id} | set={map.beatmapset_id} | {map.title}"
        )
