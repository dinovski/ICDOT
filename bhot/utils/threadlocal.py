import threading
from contextlib import contextmanager

_thread_locals = threading.local()


def set_current_user(user):
    _thread_locals.user = user


def get_current_user():
    return getattr(_thread_locals, "user", None)


@contextmanager
def current_user(user):
    set_current_user(user)
    yield
    set_current_user(None)
