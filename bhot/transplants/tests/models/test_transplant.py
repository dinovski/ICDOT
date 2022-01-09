from model_bakery import baker

from bhot.transplants.models import Transplant


def test_ref_in_name():
    transplant = baker.prepare(Transplant, donor_ref="foo", recipient_ref="bar")
    assert "foo" in str(transplant)
    assert "bar" in str(transplant)


def test_transplant_get_absolute_url():
    transplant = baker.prepare(Transplant)
    assert transplant.get_absolute_url() == f"/transplants/detail/{transplant.pk}"
