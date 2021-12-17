from django.db import models

from bhot.users.models import UserScopedModel


class DonorRecord(UserScopedModel):
    date = models.DateField()
    donor_ref = models.CharField(max_length=256)
