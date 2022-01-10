from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TransplantsConfig(AppConfig):
    name = "bhot.transplants"
    verbose_name = _("Transplants")

    def ready(self):
        import bhot.transplants.signals  # noqa F401
