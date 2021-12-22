from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from bhot.transplants.models import Biopsy, Histology, SequencingData, Transplant
from bhot.transplants.resources import (
    BiopsyResource,
    HistologyResource,
    SequencingDataResource,
    TransplantResource,
)


@admin.register(Transplant)
class TransplantAdmin(ImportExportModelAdmin):
    resource_class = TransplantResource


@admin.register(Biopsy)
class BiopsyAdmin(ImportExportModelAdmin):
    resource_class = BiopsyResource


@admin.register(Histology)
class HistologyAdmin(ImportExportModelAdmin):
    resource_class = HistologyResource


@admin.register(SequencingData)
class SequencingDataAdmin(ImportExportModelAdmin):
    resource_class = SequencingDataResource
