import uuid

from django.db import models

from bhot.transplants.models.transplant import Transplant
from bhot.users.models import UserScopedModel


class Biopsy(UserScopedModel):
    class Meta:
        verbose_name_plural = "biopsies"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transplant = models.ForeignKey(Transplant, null=True, on_delete=models.SET_NULL)
    biopsy_date = models.DateField()
