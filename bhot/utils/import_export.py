from import_export import fields, resources


class MultiFieldImportField(fields.Field):
    def __init__(self, resource_class, attribute=None, attribute_prefix=None, **kwargs):
        self.resource_class = resource_class
        if attribute_prefix is not None:
            self.attribute_prefix = attribute_prefix
        elif attribute is not None:
            self.attribute_prefix = attribute + "__"
        else:
            self.attribute_prefix = ""
        super().__init__(attribute=attribute, **kwargs)

    def clean(self, data, **kwargs):
        resource = self.resource_class()
        instance_loader = resource._meta.instance_loader_class(resource, dataset=None)
        return resource.get_instance(instance_loader, row=data)

    def get_id_field(self, field_name):
        resource_field = self.resource_class.fields.get(field_name, None)
        if isinstance(resource_field, MultiFieldImportField):
            return MultiFieldImportField(
                resource_class=resource_field.resource_class,
                attribute_prefix=self.attribute_prefix
                + resource_field.attribute
                + "__",
                readonly=True,
            )
        else:
            return fields.Field(
                attribute=self.attribute_prefix + field_name,
                readonly=True,
            )

    def get_id_fields(self):
        return (
            self.get_id_field(field_name)
            for field_name in self.resource_class.Meta.import_id_fields
        )


class ModelResourceWithMultiFieldImport(resources.ModelResource):
    def get_export_fields(self):
        return [
            f for f in self.get_fields() if not isinstance(f, MultiFieldImportField)
        ]

    def import_field(self, field, obj, data, is_m2m=False, **kwargs):
        if not field.attribute:
            return  # Nowhere to save the data to.
        if field.column_name not in data and not isinstance(
            field, MultiFieldImportField
        ):
            return  # Nowhere to get the data from.
        field.save(obj, data, is_m2m, **kwargs)

    def get_instance(self, instance_loader, row):
        """
        If all 'import_id_fields' are present in the dataset, calls
        the :doc:`InstanceLoader <api_instance_loaders>`. Otherwise,
        returns `None`.
        """
        import_id_fields = [self.fields[f] for f in self.get_import_id_fields()]
        for field in import_id_fields:
            if field.column_name not in row and not isinstance(
                field, MultiFieldImportField
            ):
                return instance_loader.get_instance(row)
        return instance_loader.get_instance(row)
