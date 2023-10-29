from datetime import datetime, timezone

import src.api as api
import src.database as db

if __name__ == "__main__":
    db.remove_all_scores()
    db.import_scores_from_csv("export/scores.csv")
