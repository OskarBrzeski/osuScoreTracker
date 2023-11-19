from datetime import datetime, timedelta

import src.api as api
import src.database as db


def main() -> None:
    initialise_database()
    user_id = start()
    print()
    while show_options(user_id) != "QUIT":
        continue


def initialise_database() -> None:
    db.create_map_table()
    db.create_score_table()


def start() -> int:
    print("=====================")
    print("    SCORE TRACKER    ")
    print("=====================")
    return get_user_id()


def show_options(user_id: int) -> None:
    print("1. Get all osu!std leaderboard maps into database")
    print("2. Get scores on all maps in database")
    print("3. Export scores into CSV file")
    print("4. Show stats")
    print("5. Quit")
    print()
    response = get_input(["1", "2", "3", "4", "5"])
    print()

    if response == "1":
        map_options()
    elif response == "2":
        score_options(user_id)
    elif response == "3":
        ...
    elif response == "4":
        print(f"Maps in database: {db.get_map_count()}")
        print(f"Scores in database: {db.get_score_count()}")
        print()
    elif response == "5":
        return "QUIT"


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


def score_options(user_id: int) -> None:
    print("1. Get as many scores as possible")
    print("2. Get scores for the next speficied amount of time")
    print("3. Get specified number of scores")
    print("4. Get scores for particular year")
    print("5. Empty score database")
    print()
    response = get_input(["1", "2", "3", "4", "5"])
    print()

    if response == "1":
        map_ids = db.get_all_map_ids_without_score()
        for i, map_id in enumerate(map_ids, start=1):
            print(f"Adding score for map {map_id} | {i}/{len(map_ids)}")
            score = api.get_score(map_id, user_id)
            db.add_score(db._score_into_table_record(score))
        print("Finished adding scores to database")
    elif response == "2":
        duration = get_duration()
        starting_time = datetime.now()
        end_time = starting_time + duration
        map_ids = db.get_all_map_ids_without_score()
        i = 1
        while (now := datetime.now()) < end_time:
            print(f"Adding score for map {map_id[i-1]} | {end_time - now} remaining")
            score = api.get_score(map_ids[i-1], user_id)
            db.add_score(db._score_into_table_record(score))
        print("Finished adding scores to database")
    elif response == "3":
        ...
    elif response == "4":
        year = get_year()
        map_ids = db.get_map_ids_for_year(year)
        for i, map_id in enumerate(map_ids, start=1):
            print(f"Adding score for map {map_id} | {i}/{len(map_ids)}")
            score = api.get_score(map_id, user_id)
            db.add_score(db._score_into_table_record(score))
        print("Finished adding scores to database")
    elif response == "5":
        db.remove_all_scores()


def get_year() -> int:
    while True:
        response = input("Enter year: ")
        
        if not response.isnumeric():
            print(f"ERROR: {repr(response)} is not an integer")
        elif int(response) < 2007 or int(response) > datetime.now().year:
            print(f"ERROR: {response} must be from 2007 to {datetime.now().year}")
        else:
            break
    
    return int(response)


def get_duration() -> timedelta:
    while True:
        response = input("Enter amount of minutes to get scores for: ")
        
        if not response.isnumeric():
            print(f"ERROR: {repr(response)} is not an integer")
        elif int(response) < 1:
            print(f"ERROR: {response} must be 1 or greater")
        else:
            break
    
    return timedelta(minutes=int(response))


def get_input(options: list[str]) -> str:
    while True:
        response = input("Choose option: ")
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
