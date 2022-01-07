from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TransplantsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bhot.utils.tests.utils_demo"
    verbose_name = _("Demo app for testing utils")
