from datetime import datetime, timedelta

# import score_tracker.api as api
# import score_tracker.database as db

from score_tracker.models.seed import create_map_table, create_score_table
from score_tracker.models.maps import (
    remove_all_maps,
    get_map_count,
    get_ranked_map_count,
    get_latest_leaderboard_map,
    get_latest_ranked_map,
    get_all_map_ids_without_score,
    get_all_map_ids_without_score_in_database,
    get_map_ids_for_year,
)
from score_tracker.models.scores import (
    get_score_in_database_count,
    get_score_count,
    add_score,
    remove_all_scores,
)
from score_tracker.controllers.maps import get_leaderboard_maps, fill_map_table
from score_tracker.controllers.scores import get_score


def main() -> None:
    initialise_database()
    user_id = start()
    while show_options(user_id) != "QUIT":
        continue


def initialise_database() -> None:
    create_map_table()
    create_score_table()


def start() -> int:
    print("=====================")
    print("    SCORE TRACKER    ")
    print("=====================")
    return get_user_id()


def show_options(user_id: int) -> None:
    print()
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
        # export_scores_as_csv(user_id)
    elif response == "4":
        show_stats()
    elif response == "5":
        return "QUIT"


def show_stats():
    print(f"Maps in database: {get_map_count()} | {get_ranked_map_count()}")
    print(f"Scores in database: {get_score_in_database_count()} | {get_score_count()}")


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
        remove_all_maps()
        maps = get_leaderboard_maps()
        fill_map_table(maps)
    elif response == "2":
        since = get_latest_leaderboard_map()
        maps = get_leaderboard_maps(since=since)
        fill_map_table(maps)
    elif response == "3":
        remove_all_maps()
        maps = [map for map in get_leaderboard_maps() if map.approved in ["1", "2"]]
        fill_map_table(maps)
    elif response == "4":
        since = get_latest_ranked_map()
        maps = [
            map
            for map in get_leaderboard_maps(since=since)
            if map.approved in ["1", "2"]
        ]
        fill_map_table(maps)
    elif response == "5":
        remove_all_maps()


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
        map_ids = get_all_map_ids_without_score()
        for i, map_id in enumerate(map_ids, start=1):
            print(f"Adding score for map {map_id} | {i}/{len(map_ids)}")
            score = get_score(map_id, user_id)
            add_score(score)
        print("Finished adding scores to database")
    elif response == "2":
        duration = get_duration()
        starting_time = datetime.now()
        end_time = starting_time + duration
        map_ids = get_all_map_ids_without_score_in_database()
        i = 0
        while (now := datetime.now()) < end_time and i < len(map_ids):
            print(f"Adding score for map {map_ids[i]} | {end_time - now} remaining")
            score = get_score(map_ids[i], user_id)
            add_score(score)
            i += 1
        print("Finished adding scores to database")
    elif response == "3":
        amount = get_positive_integer()
        map_ids = get_all_map_ids_without_score_in_database()
        for i in range(amount):
            print(f"Adding score for map {map_ids[i]} | {i+1}/{amount}")
            score = get_score(map_ids[i], user_id)
            add_score(score)
        print("Finished adding scores to database")
    elif response == "4":
        year = get_year()
        map_ids = get_map_ids_for_year(year)
        for i, map_id in enumerate(map_ids, start=1):
            print(f"Adding score for map {map_id} | {i}/{len(map_ids)}")
            score = get_score(map_id, user_id)
            add_score(score)
        print("Finished adding scores to database")
    elif response == "5":
        remove_all_scores()


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
        result = input("Enter User ID: ")

        if not result.isnumeric():
            print(f"ERROR: {repr(result)} is not an integer.")
        elif int(result) < 1:
            print(f"ERROR: {result} must be 1 or greater.")
        else:
            break

    return int(result)


def get_positive_integer() -> int:
    while True:
        result = input("Enter number: ")

        if not result.isnumeric():
            print(f"ERROR: {repr(result)} is not an integer.")
        elif int(result) < 1:
            print(f"ERROR: {result} must be 1 or greater.")
        else:
            break

    return int(result)
