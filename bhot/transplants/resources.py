from import_export import resources

from bhot.transplants.models import Transplant


class TransplantResource(resources.ModelResource):
    class Meta:
        model = Transplant
        exclude = [f.name for f in Transplant._meta.fields if not f.editable]
        # Because of django_scopes being in effect we do not need to add
        # the user to the id_fields, it will be scoped to the current user,
        # this is actually what we want.
        # TODO: Write some tests for this!
        import_id_fields = ["transplant_date", "donor_ref", "recipient_ref"]
