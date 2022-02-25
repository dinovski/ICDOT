from django.apps import apps
from django.db import models


def _test_models_do_not_use_confusing_char_fields():
    for model in apps.get_app_config("transplants").get_models():
        for field in model._meta.get_fields():
            if not isinstance(field, models.CharField):
                continue
            assert not (
                field.blank and field.null
            ), f"""
                {model=} defines {field=}.

                Using both blank and null is confusing as there are
                two ways of having 'no value' in the database. However
                if you have a good reason for doing so just remove
                this failing test.
                """
