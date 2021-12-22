from bhot.transplants.models import Biopsy, Histology, SequencingData, Transplant
from bhot.utils.import_export import (
    ModelResourceWithMultiFieldImport,
    MultiFieldImportField,
)

# Because of django_scopes being in effect we do not need to add
# the user to the id_fields, it will be scoped to the current user,
# this is actually what we want.
# TODO: Write some tests for this!


class TransplantResource(ModelResourceWithMultiFieldImport):
    class Meta:
        model = Transplant
        exclude = [f.name for f in Transplant._meta.fields if not f.editable]
        import_id_fields = ["transplant_date", "donor_ref", "recipient_ref"]


class BiopsyResource(ModelResourceWithMultiFieldImport):
    transplant = MultiFieldImportField(
        resource_class=TransplantResource,
        attribute="transplant",
    )
    transplant_date, donor_ref, recipient_ref = transplant.get_id_fields()

    class Meta:
        model = Biopsy
        exclude = [f.name for f in model._meta.fields if not f.editable]
        import_id_fields = ["transplant", "biopsy_date"]


class HistologyResource(ModelResourceWithMultiFieldImport):

    biopsy = MultiFieldImportField(
        resource_class=BiopsyResource,
        attribute="biopsy",
    )
    transplant, biopsy_date = biopsy.get_id_fields()
    transplant_date, donor_ref, recipient_ref = transplant.get_id_fields()

    class Meta:
        model = Histology
        exclude = [f.name for f in model._meta.fields if not f.editable]
        import_id_fields = ["biopsy", "histology_date"]


class SequencingDataResource(ModelResourceWithMultiFieldImport):

    biopsy = MultiFieldImportField(
        resource_class=BiopsyResource,
        attribute="biopsy",
    )
    transplant, biopsy_date = biopsy.get_id_fields()
    transplant_date, donor_ref, recipient_ref = transplant.get_id_fields()

    class Meta:
        model = SequencingData
        exclude = [f.name for f in model._meta.fields if not f.editable]
        import_id_fields = ["biopsy", "sequencing_date"]
