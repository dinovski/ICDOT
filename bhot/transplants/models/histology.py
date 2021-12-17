from django.db import models

from bhot.transplants.models.biopsy import Biopsy
from bhot.users.models import UserScopedModel


class Histology(UserScopedModel):
    class Meta:
        verbose_name_plural = "histologies"

    date = models.DateField()
    biopsy = models.ForeignKey(Biopsy, null=True, on_delete=models.SET_NULL)
