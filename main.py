from datetime import datetime, timezone

import src.api as api
import src.database as db

if __name__ == "__main__":
    score = api.get_score(4179858, 7051163)

    db.remove_all_scores()
    db.fill_score_table([score])

    # db.delete_map_table()
    # db.create_map_table()

    # maps = api.get_all_leaderboard_maps(upto=datetime(2008, 1, 1, tzinfo=timezone.utc))
    # db.fill_map_table(maps)

    # db.delete_score_table()
    # db.create_score_table()

    # scores = [api.get_score(m.beatmap_id, 7051163) for m in maps]
    # db.fill_score_table(scores)

    # db.remove_all_maps()
