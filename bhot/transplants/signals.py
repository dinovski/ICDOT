from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate

from bhot.transplants.apps import TransplantsConfig


def populate_transplants_group(sender, **kwargs):

    group_app, created = Group.objects.get_or_create(
        name=f"Access to {TransplantsConfig.name}"
    )

    models = apps.all_models[TransplantsConfig.name]
    for model in models:
        content_type = ContentType.objects.get(
            app_label=TransplantsConfig.name, model=model
        )
        permissions = Permission.objects.filter(content_type=content_type)
        group_app.permissions.add(*permissions)


post_migrate.connect(populate_transplants_group, sender=TransplantsConfig)
