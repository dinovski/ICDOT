import uuid

from django.db import models

from bhot.transplants.models.biopsy import Biopsy
from bhot.transplants.models.file_upload import TrackFileUploadMixin
from bhot.users.models import UserScopedModel


class SequencingData(TrackFileUploadMixin, UserScopedModel):
    class Meta:
        verbose_name_plural = "sequencing data"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    biopsy = models.ForeignKey(Biopsy, null=True, on_delete=models.SET_NULL)
    sequencing_date = models.DateField()

    file_ref = models.CharField(max_length=256, blank=True)
    file_path = models.FileField(null=True, editable=False)

    TRACK_FILE_UPLOAD = {"file_ref": "file_path"}
