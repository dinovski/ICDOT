"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="XoG4J5W9lzXGAugCEq3JedGA1duqrDrubOOZBRZjvhNROMBXVtkjYumLPyhVPnlW",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]
# django_coverage_plugin.DjangoTemplatePlugin requires template debugging.
TEMPLATES[-1]["OPTIONS"]["debug"] = True  # type: ignore[index] # noqa F405

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Your stuff...
# ------------------------------------------------------------------------------

# We need to disable scopes through a monkey-patch, this is because
# they break django's test runner and pytest-django, for more info see:
# https://github.com/raphaelm/django-scopes/blob/53633943/README.md#testing
from django.test import utils  # noqa F402
from django_scopes import scopes_disabled  # noqa F402

utils.setup_databases = scopes_disabled()(utils.setup_databases)
