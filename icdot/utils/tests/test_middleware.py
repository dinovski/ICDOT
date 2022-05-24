from django_scopes import get_scope

from icdot.utils.middleware import CurrentUserMiddleware


class MockRequest:
    def __init__(self, user):
        self.user = user


class MockUser:
    @property
    def is_superuser(self):
        raise AssertionError(
            "User scope is not expected to depend on superuser status."
        )


def test_middleware_forwards_request():
    user = MockUser()

    def validate(request):
        assert request.user is user
        assert get_scope() == dict(_enabled=True, user=user)

    CurrentUserMiddleware(validate)(MockRequest(user=user))


def test_anonymous_users_do_not_get_context():
    user = None

    def validate(request):
        assert request.user is None
        assert not get_scope().get("_enabled")

    CurrentUserMiddleware(validate)(MockRequest(user=user))
