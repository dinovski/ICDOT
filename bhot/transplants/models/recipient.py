from django.db import models

from bhot.users.models import UserScopedModel


class RecipientRecord(UserScopedModel):

    date = models.DateField()
    recipient_ref = models.CharField(max_length=256)
