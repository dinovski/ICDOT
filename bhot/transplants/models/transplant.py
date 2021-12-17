from django.db import models

from bhot.transplants.models.donor import DonorRecord
from bhot.transplants.models.recipient import RecipientRecord
from bhot.users.models import UserScopedModel


class Transplant(UserScopedModel):

    date = models.DateField()
    donor_record = models.ForeignKey(DonorRecord, null=True, on_delete=models.SET_NULL)
    recipient_record = models.ForeignKey(
        RecipientRecord, null=True, on_delete=models.SET_NULL
    )
