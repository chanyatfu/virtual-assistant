from typing import Callable
from threading import Thread


def concurrent(fn: Callable) -> Callable[..., None]:
    """Decorator to run a function in a new thread."""
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
    return wrapper
