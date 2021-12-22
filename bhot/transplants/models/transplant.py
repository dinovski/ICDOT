import uuid

from django.db import models
from django.urls import reverse
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

    # Recipient information
    recipient_record_date = models.DateField()
    pre_transplant_dialysis = models.BooleanField(blank=True, null=True)
    time_on_dialysis = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.transplant_date} from {self.donor_ref} to {self.recipient_ref}"

    def get_absolute_url(self):
        """Get url for transplant's detail view.

        Returns:
            str: URL for transplant detail.

        """
        return reverse("transplants:detail", kwargs={"pk": self.pk})
