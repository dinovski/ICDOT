import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from bhot.transplants.models.transplant import Transplant
from bhot.users.models import UserScopedModel


class Biopsy(UserScopedModel):
    class Meta:
        verbose_name_plural = "biopsies"

    class ProteinuriaUnit(models.TextChoices):
        GRAM_PER_GRAM = "g/g", _("g/g")
        GRAM_PER_24H = "g/24h", _("g/24h")
        GRAM_PER_LITER = "g/L", _("g/L")
        MILLIGRAM_PER_MILLIMOLE = "mg/mmol", _("mg/mmol")
        GRAM_PER_MILLIMOLE = "g/mmol", _("g/mmol")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transplant = models.ForeignKey(Transplant, null=True, on_delete=models.SET_NULL)
    biopsy_date = models.DateField()

    proteinuria = models.FloatField(blank=True, null=True)
    proteinuria_unit = models.CharField(
        max_length=32,
        choices=ProteinuriaUnit.choices,
        blank=False,
        default=ProteinuriaUnit.MILLIGRAM_PER_MILLIMOLE,
    )
