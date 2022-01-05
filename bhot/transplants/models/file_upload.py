import uuid

from django.core import exceptions
from django.db import models
from django.utils.translation import gettext_lazy as _

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
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="files",
    )

    def __str__(self):
        return self.file_ref


class ModelBaseTrackingFileUpload(models.base.ModelBase):
    def __new__(cls, clsname, bases, attrs):
        newcls = super().__new__(cls, clsname, bases, attrs)
        if newcls.TRACK_FILE_UPLOAD is not None:
            models.signals.post_save.connect(
                newcls._update_file_paths,
                sender=FileUpload,
            )
        return newcls


class TrackFileUploadMixin(metaclass=ModelBaseTrackingFileUpload):

    TRACK_FILE_UPLOAD = None

    # When file_ref changes we want to get the new file_path.
    # Remember the original value so we only do this when it changes.
    __original_file_refs = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_file_refs = {
            attr: getattr(self, attr) for attr in self.TRACK_FILE_UPLOAD
        }

    @classmethod
    def _update_file_paths(cls, sender, instance, **kwargs):
        """Update file paths when uploads matching file refs occur."""
        for refattr, pathattr in cls.TRACK_FILE_UPLOAD.items():
            cls.objects.filter(**{refattr: instance.file_ref}).update(
                **{pathattr: instance.file_path}
            )

    def _set_file_path(self, refattr, pathattr):
        """Save and update file path if necessary."""
        ref = getattr(self, refattr)
        if ref == self.__original_file_refs[refattr]:
            return
        file_upload = FileUpload.objects.get(file_ref=ref)
        setattr(self, pathattr, file_upload.file_path if file_upload else None)
        self.__original_file_refs[refattr] = ref

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        errors = {}
        for refattr, pathattr in self.TRACK_FILE_UPLOAD.items():
            try:
                self._set_file_path(refattr, pathattr)
            except FileUpload.MultipleObjectsReturned:
                errors[refattr] = _(
                    "File reference is ambigious, it matches multiple uploads."
                )
        if errors:
            raise exceptions.ValidationError(errors)

    def save(self, *args, **kwargs):
        for refattr, pathattr in self.TRACK_FILE_UPLOAD.items():
            self._set_file_path(refattr, pathattr)
        super().save(*args, **kwargs)
