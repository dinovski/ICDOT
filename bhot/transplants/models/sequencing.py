import uuid

from django.db import models

from bhot.transplants.models.biopsy import Biopsy
from bhot.users.models import UserScopedModel


class SequencingData(UserScopedModel):
    class Meta:
        verbose_name_plural = "sequencing data"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    biopsy = models.ForeignKey(Biopsy, null=True, on_delete=models.SET_NULL)
    sequencing_date = models.DateField()
