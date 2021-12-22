from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from bhot.transplants.models import Biopsy, Histology, SequencingData, Transplant
from bhot.transplants.resources import TransplantResource


@admin.register(Transplant)
class TransplantAdmin(ImportExportModelAdmin):
    resource_class = TransplantResource


@admin.register(Biopsy)
class BiopsyAdmin(admin.ModelAdmin):
    pass


@admin.register(Histology)
class HistologyAdmin(admin.ModelAdmin):
    pass


@admin.register(SequencingData)
class SequencingDataAdmin(admin.ModelAdmin):
    pass
