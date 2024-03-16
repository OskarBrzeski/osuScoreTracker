from functools import wraps
from time import time
from typing import Callable

last_call_time = time()


def rate_limit(func: Callable) -> Callable:
    """Decorator for rate limiting api calls."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        global last_call_time

        while time() - last_call_time < 1:
            continue

        result = None
        retries = 0
        while result is None:
            if retries > 10:
                raise TimeoutError("Too many unsuccessful requests")
            try:
                last_call_time = time()
                result = func(*args, **kwargs)
            except ConnectionError:
                retries += 1
                print("Connection Error occured")

        return result

    return wrapper
