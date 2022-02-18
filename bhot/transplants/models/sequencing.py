import uuid

from django.db import models

from bhot.transplants.models.biopsy import Biopsy
from bhot.transplants.models.file_upload import TrackFileUploadModel
from bhot.users.models import UserScopedModel


class SequencingData(UserScopedModel, TrackFileUploadModel):
    class Meta:
        verbose_name_plural = "sequencing data"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    biopsy = models.ForeignKey(Biopsy, null=True, on_delete=models.SET_NULL)
    sequencing_date = models.DateField()

    file_ref = models.CharField(
        max_length=256,
        blank=True,
        help_text=(
            "<b>This must be set if you want to add a file.</b><br/>"
            "This reference will be matched against files that are uploaded as batches.<br/>"
            "You can also upload a file directly and it will be associated to this reference."
        ),
    )
    file_path = models.FileField(null=True, editable=False)

    TRACK_FILE_UPLOAD = {"file_ref": "file_path"}
