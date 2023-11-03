import src.api as api
import src.database as db


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

    if response == "1":
        ...
    elif response == "2":
        ...
    elif response == "3":
        ...


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