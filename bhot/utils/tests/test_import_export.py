import pytest

from bhot.utils.import_export import (
    ModelResourceWithMultiFieldImport,
    MultiFieldImportField,
)
from bhot.utils.tests.utils_demo.models import Author, Book, Review

pytestmark = pytest.mark.django_db

TEST_DATA = (
    dict(
        first_name="foo",
        last_name="bar",
        title="foo's book",
        desc="desc",
        content="content",
    ),
    dict(
        first_name="spam",
        last_name="eggs",
        title="spam's book",
        desc="desc",
        content="content",
    ),
)


@pytest.fixture
def setup_models():
    for entry in TEST_DATA:
        author, _ = Author.objects.get_or_create(
            first_name=entry["first_name"], last_name=entry["last_name"]
        )
        book, _ = Book.objects.get_or_create(
            author=author, title=entry["title"], desc=entry["desc"]
        )
        review, _ = Review.objects.get_or_create(book=book, content=entry["content"])


def test_import_export_works(setup_models):
    class AuthorResource(ModelResourceWithMultiFieldImport):
        class Meta:
            model = Author
            exclude = ["id"]
            import_id_fields = ["first_name", "last_name"]

    class BookResource(ModelResourceWithMultiFieldImport):
        class Meta:
            model = Book
            exclude = ["id", "author"]
            import_id_fields = ["author", "title"]

        author = MultiFieldImportField(
            resource_class=AuthorResource,
            attribute="author",
        )
        first_name, last_name = author.get_id_fields()

    class ReviewResource(ModelResourceWithMultiFieldImport):
        class Meta:
            model = Review
            exclude = ["id", "book"]
            import_id_fields = ["book"]  # This means only one review per book.
            # That's kind of weird but it's a test, whatever.

        book = MultiFieldImportField(
            resource_class=BookResource,
            attribute="book",
        )
        author, title = book.get_id_fields()
        first_name, last_name = author.get_id_fields()

    # Check that export is working.

    dataset = ReviewResource().export()
    assert len(dataset) == len(TEST_DATA)
    for test in TEST_DATA:
        # "desc" is the only thing we do not expect to see in the review data.
        expected = {k: v for k, v in test.items() if k != "desc"}
        assert any(expected == dict(r) for r in dataset.dict)

    # Check that import is working.

    # Change on cell.
    dataset[0] = tuple("new content" if x == "content" else x for x in dataset[0])
    result = ReviewResource().import_data(dataset, raise_errors=True, dry_run=False)
    assert result.total_rows == len(TEST_DATA)  # both books have been updated.
    assert Book.objects.count() == len(TEST_DATA)  # nothing has been created.
    assert Review.objects.get(book__author__first_name="foo").content == "new content"

    # Update with a missing column, we expect data not to change.
    del dataset["content"]
    result = ReviewResource().import_data(dataset, raise_errors=True, dry_run=False)
    assert result.total_rows == len(TEST_DATA)  # both books have been updated.
    assert Book.objects.count() == len(TEST_DATA)  # nothing has been created.
    assert Review.objects.get(book__author__first_name="foo").content == "new content"

    # If we remove a column used for id_fields we expect nothing to load.
    del dataset["first_name"]
    with pytest.raises(KeyError):
        result = ReviewResource().import_data(dataset, raise_errors=True, dry_run=False)


def test_prefix():

    field = MultiFieldImportField(Author)
    assert field.attribute_prefix == ""

    field = MultiFieldImportField(Author, attribute="foo")
    assert field.attribute_prefix == "foo__"

    field = MultiFieldImportField(Author, attribute="foo", attribute_prefix="bar")
    assert field.attribute_prefix == "bar"

    field = MultiFieldImportField(Author, attribute_prefix="bar")
    assert field.attribute_prefix == "bar"
