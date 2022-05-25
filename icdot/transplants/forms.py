from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from nonrelated_inlines.forms import NonrelatedInlineFormSet

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
        # It might make sense to have this be called in self.save()
        # but in a lot of cases we want this when save() is not
        # actually being called. Keep it stand alone.
        for upload in self.files.getlist("files"):
            FileUpload(batch=batch, file_path=upload, file_ref=upload.name).save()


class FileUploadInlineFormSet(NonrelatedInlineFormSet):
    def _has_changed_forms(self):
        for i, form in enumerate(self.forms):
            had_initial_data = i < self.initial_form_count()
            # Empty forms are unchanged forms beyond those with initial data.
            if form.has_changed() and (had_initial_data or form.data):
                return True
        return False

    def clean(self):
        if self._has_changed_forms() and not self.instance.file_ref:
            raise ValidationError(_("There is no file ref to work with."))
        return super().clean()
