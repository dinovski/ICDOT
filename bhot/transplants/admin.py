from django.contrib import admin

from .models import Biopsy, Histology, SequencingData, Transplant


@admin.register(Transplant)
class TransplantAdmin(admin.ModelAdmin):
    pass


@admin.register(Biopsy)
class BiopsyAdmin(admin.ModelAdmin):
    pass


@admin.register(Histology)
class HistologyAdmin(admin.ModelAdmin):
    pass


@admin.register(SequencingData)
class SequencingDataAdmin(admin.ModelAdmin):
    pass
