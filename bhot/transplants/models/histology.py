import uuid

from django.db import models

from bhot.transplants.models.biopsy import Biopsy
from bhot.users.models import UserScopedModel


class Histology(UserScopedModel):
    class Meta:
        verbose_name_plural = "histologies"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    biopsy = models.ForeignKey(Biopsy, null=True, on_delete=models.SET_NULL)
    histology_date = models.DateField()
