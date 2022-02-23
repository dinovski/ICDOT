import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from bhot.users.models import UserScopedModel


class Transplant(UserScopedModel):

    # WARNING: We use views/forms with fields='__all__'.
    # Please make sure when adding fields here that it is okay for users to both
    # see and edit them without it being a security problem for the app!

    class Sex(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        OTHER = "O", _("Other")

    class DonorCriteria(models.TextChoices):
        SCD = "SCD", _("Standard Donor Criteria")
        ECD = "ECD", _("Expanded Donor Criteria")

    # set general class for units; assign to specific models (eg. donor_proteinuria_units)
    class ProteinuriaUnits(models.TextChoices):
        G_G = "g/g", _("g/g")
        G_24H = "g/g", _("g/g")
        MG_DL = "mg/dL", _("mg/dL")
        G_L = "g/L", _("g/L")
        MG_MMOL = "mg/mmol", _("mg/mmol")
        G_MMOL = "g/mmol", _("g/mmol")

    # Main information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transplant_date = models.DateField()
    donor_ref = models.CharField(max_length=256)
    recipient_ref = models.CharField(max_length=256)

    # Donor information
    donor_record_date = models.DateField()
    donor_sex = models.CharField(
        max_length=1,
        choices=Sex.choices,
        blank=True,
    )
    donor_criteria = models.CharField(
        max_length=100,
        choices=DonorCriteria.choices,
        blank=True,
    )
    donor_egfr = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(500.0)],
        blank=True,
        null=True,
        verbose_name="Donor eGFR (mL/min/1.73m2)",
    )
    donor_proteinuria = models.FloatField(
        blank=True,
        null=True,
    )
    donor_proteinuria_units = models.CharFiles(
        choices=ProteinuriaUnits.choices,
    )

    # Recipient information
    recipient_record_date = models.DateField()
    pre_transplant_dialysis = models.BooleanField(blank=True, null=True)
    time_on_dialysis = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.transplant_date} from {self.donor_ref} to {self.recipient_ref}"
