from datetime import datetime, timezone

import src.api as api
import src.database as db

if __name__ == "__main__":
    db.export_scores_as_csv(7051163)
