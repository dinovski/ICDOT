from contextlib import ExitStack, contextmanager

from django_scopes import scope

from bhot.utils.threadlocal import current_user


@contextmanager
def current_user_and_scope(user):
    with ExitStack() as stack:
        stack.enter_context(current_user(user))
        if user is not None:
            stack.enter_context(scope(user=user))
        yield


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        with current_user_and_scope(user):
            return self.get_response(request)
