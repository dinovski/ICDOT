from contextlib import ExitStack

from django.http import HttpRequest
from django.urls import get_script_prefix
from django_scopes import scope, scopes_disabled

from bhot.utils.threadlocal import current_user


def ignore_scopes_in_admin_middleware(get_response, admin_path: str = "admin/"):
    def middleware(request: HttpRequest):
        if request.path.startswith(get_script_prefix() + admin_path):
            with scopes_disabled():
                return get_response(request)

        return get_response(request)

    return middleware


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        with ExitStack() as stack:
            stack.enter_context(current_user(user))
            if user is not None:
                stack.enter_context(scope(user=user))
            return self.get_response(request)
