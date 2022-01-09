import import_export
import pytest
from model_bakery import baker

from bhot.transplants import resources
from bhot.utils.middleware import current_user_and_scope

ALL_RESOURCES = [
    r
    for r in resources.__dict__.values()
    if isinstance(r, type)
    and issubclass(r, import_export.resources.ModelResource)
    and r._meta.model
]

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("fill_optional", [True, False])
@pytest.mark.parametrize("resource", ALL_RESOURCES)
def test_all_resources_import_export(user, fill_optional, resource):
    instance = resource()
    with current_user_and_scope(user=user):
        baker.make(resource._meta.model, _quantity=5, _fill_optional=fill_optional)
        dataset = instance.export()
        assert len(dataset) == 5
        instance.import_data(dataset)
