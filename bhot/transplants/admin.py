from django.contrib import admin

from .models import (
    Biopsy,
    DonorRecord,
    Histology,
    RecipientRecord,
    SequencingData,
    Transplant,
)


@admin.register(DonorRecord)
class DonorRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "donor_ref")
    list_filter = ("date",)


@admin.register(RecipientRecord)
class RecipientRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "recipient_ref")
    list_filter = ("date",)


@admin.register(Transplant)
class TransplantAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "donor_record", "recipient_record")
    list_filter = ("date", "donor_record", "recipient_record")


@admin.register(Biopsy)
class BiopsyAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "transplant")
    list_filter = ("date", "transplant")


@admin.register(Histology)
class HistologyAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "biopsy")
    list_filter = ("date", "biopsy")


@admin.register(SequencingData)
class SequencingDataAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "biopsy", "rccfile")
    list_filter = ("date", "biopsy")
