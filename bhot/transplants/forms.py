from django import forms
from django.utils.translation import gettext as _

from .models import FileUpload, FileUploadBatch


class FileUploadBatchAdminForm(forms.ModelForm):
    class Meta:
        model = FileUploadBatch
        fields = ()

    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label=_("Add multiple files at once"),
        required=False,
    )

    def clean_files(self):
        """Make sure only images can be uploaded."""
        # This is where we would do validation of RCC files.
        # Or file size, etc.

    def save_files(self, batch):
        """Process each uploaded file using their names as references."""
        for upload in self.files.getlist("files"):
            FileUpload(batch=batch, file_path=upload, file_ref=upload.name).save()
