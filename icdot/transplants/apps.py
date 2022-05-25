from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def make_group_for_app(sender, **kwargs):
    # We can not import those models before this function
    # is called because apps won't have finished loading.
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    group, _ = Group.objects.get_or_create(name=f"Access to {sender.label}")
    group.permissions.add(
        *Permission.objects.filter(
            content_type__in=ContentType.objects.filter(app_label=sender.label)
        )
    )


class TransplantsConfig(AppConfig):
    name = "icdot.transplants"
    verbose_name = _("Transplants")

    def ready(self):
        post_migrate.connect(make_group_for_app, sender=self)
