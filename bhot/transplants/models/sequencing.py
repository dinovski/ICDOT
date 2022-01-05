import uuid

from django.core import exceptions
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from bhot.transplants.models.biopsy import Biopsy
from bhot.transplants.models.file_upload import FileUpload
from bhot.users.models import UserScopedModel


class SequencingData(UserScopedModel):
    class Meta:
        verbose_name_plural = "sequencing data"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    biopsy = models.ForeignKey(Biopsy, null=True, on_delete=models.SET_NULL)
    sequencing_date = models.DateField()

    file_ref = models.CharField(max_length=256, blank=True)
    file_path = models.FileField(null=True, editable=False)

    @staticmethod
    @receiver(models.signals.post_save, sender=FileUpload)
    def update_sequencing_data_file_path(sender, instance, **kwargs):
        """Update file_path When uploads matching file_ref occur."""
        SequencingData.objects.filter(file_ref=instance.file_ref).update(
            file_path=instance.file_path
        )

    # When file_ref changes we want to get the new file_path.
    # Remember the original value so we only do this when it changes.
    __original_file_ref = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_file_ref = self.file_ref

    def _set_file_path(self):
        """Save and update file_path if necessary."""
        if self.file_ref == self.__original_file_ref:
            return

        file_upload = FileUpload.objects.get(file_ref=self.file_ref)
        self.file_path = file_upload.file_path if file_upload else None
        self.__original_file_ref = self.file_ref

    def clean(self, *args, **kwargs):
        try:
            self._set_file_path()
        except FileUpload.MultipleObjectsReturned:
            raise exceptions.ValidationError(
                {
                    "file_ref": _(
                        "File reference is ambigious, it matches multiple uploads."
                    )
                }
            )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self._set_file_path()
        super().save(*args, **kwargs)
