import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from bhot.transplants.models.biopsy import Biopsy
from bhot.transplants.models.file_upload import TrackFileUploadModel
from bhot.transplants.models.transplant import Transplant
from bhot.users.models import UserScopedModel


class SequencingData(UserScopedModel, TrackFileUploadModel):
    class Meta:
        verbose_name_plural = "sequencing data"

    class RunProtocol(models.TextChoices):
        SENSITIVE = "high sensitivity", _("high sensitivity")
        STANDARD = "standard", _("standard")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    biopsy = models.ForeignKey(Biopsy, null=True, on_delete=models.SET_NULL)
    transplant = models.ForeignKey(Transplant, null=True, on_delete=models.SET_NULL)

    run_date = models.DateField()
    run_protocol = models.CharField(
        max_length=50,
        choices=RunProtocol.choices,
    )
    rna_concentration = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        blank=True,
        null=True,
        verbose_name="RNA concentration (ng/ul)",
    )
    rna_integrity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True,
        verbose_name="RNA Integrity Number",
    )
    # RCC file
    file_ref = models.CharField(
        max_length=256,
        blank=False,
    )
    file_path = models.FileField(
        null=True,
        editable=False,
    )

    TRACK_FILE_UPLOAD = {"file_ref": "file_path"}
