import threading
from contextlib import contextmanager

_thread_locals = threading.local()


def clear():
    """Clear all thread local variables."""
    _thread_locals.__dict__.clear()


def set_current_user(user):
    _thread_locals.user = user


def get_current_user():
    return getattr(_thread_locals, "user", None)


@contextmanager
def current_user(user):
    previous = get_current_user()
    set_current_user(user)
    try:
        yield user
    finally:
        set_current_user(previous)
