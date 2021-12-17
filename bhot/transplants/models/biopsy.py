from django.db import models

from bhot.transplants.models.transplant import Transplant
from bhot.users.models import UserScopedModel


class Biopsy(UserScopedModel):
    class Meta:
        verbose_name_plural = "biopsies"

    date = models.DateField()
    transplant = models.ForeignKey(Transplant, null=True, on_delete=models.SET_NULL)
