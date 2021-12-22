from bhot.utils.import_export import MultiFieldImportField


class MockResource:
    pass


def test_field():
    assert MultiFieldImportField(
        resource_class=MockResource,
        field_prefix="prefix__",
    )
