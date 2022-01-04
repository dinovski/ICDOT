import uuid

from django.db import models

from bhot.users.models import UserScopedModel


class FileUploadBatch(UserScopedModel):
    class Meta:
        verbose_name_plural = "file upload batches"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class FileUpload(UserScopedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    file_ref = models.CharField(max_length=256)
    file_path = models.FileField()

    batch = models.ForeignKey(
        FileUploadBatch,
        null=True,
        on_delete=models.SET_NULL,
        related_name="files",
    )
