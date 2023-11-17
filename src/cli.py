import src.api as api
import src.database as db


def main() -> None:
    initialise_database()
    start()
    show_options()


def initialise_database() -> None:
    db.create_map_table()
    db.create_score_table()


def start() -> None:
    print("=====================")
    print("    SCORE TRACKER    ")
    print("=====================")


def show_options() -> None:
    print("1. Get all osu!std leaderboard maps into database")
    print("2. Get scores on all maps in database")
    print("3. Export scores into CSV file")
    print()
    response = get_input(["1", "2", "3"])
    print()

    if response == "1":
        map_options()
    elif response == "2":
        ...
    elif response == "3":
        ...


def map_options() -> None:
    print("1. Get all leaderboard maps from beginning")
    print("2. Get all leaderboard maps from most recent in database")
    print("3. Get all ranked maps from beginning")
    print("4. Get all ranked maps from most recent in database")
    print("5. Empty map database")
    print()
    response = get_input(["1", "2", "3", "4", "5"])
    print()

    if response == "1":
        db.remove_all_maps()
        maps = api.get_leaderboard_maps()
        db.fill_map_table(maps)
    elif response == "2":
        since = db.get_latest_leaderboard_map()
        maps = api.get_leaderboard_maps(since=since)
        db.fill_map_table(maps)
    elif response == "3":
        db.remove_all_maps()
        maps = [map for map in api.get_leaderboard_maps() if map.approved in ["1", "2"]]
        db.fill_map_table(maps)
    elif response == "4":
        since = db.get_latest_ranked_map()
        maps = [
            map
            for map in api.get_leaderboard_maps(since=since)
            if map.approved in ["1", "2"]
        ]
        db.fill_map_table(maps)
    elif response == "5":
        db.remove_all_maps()


def get_input(options: list[str]) -> str:
    while response := input("Choose option: "):
        if response in options:
            return response

        print("Please enter valid value.")


def get_user_id() -> int:
    while True:
        result = input("Enter user ID: ")

        if not result.isnumeric():
            print(f"ERROR: {repr(result)} is not an integer.")
        elif int(result) < 1:
            print(f"ERROR: {result} must be 1 or greater.")
        else:
            break

    return result
