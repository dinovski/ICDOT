from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TransplantsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bhot.transplants"
    verbose_name = _("Transplants")
