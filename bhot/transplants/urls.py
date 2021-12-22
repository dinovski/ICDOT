from django.urls import path

from bhot.transplants.views import (
    transplant_create_view,
    transplant_delete_view,
    transplant_detail_view,
    transplant_table_view,
    transplant_update_view,
)

app_name = "transplants"
urlpatterns = [
    path("", view=transplant_table_view, name="table"),
    path("create", view=transplant_create_view, name="create"),
    path("detail/<uuid:pk>", view=transplant_detail_view, name="detail"),
    path("update/<uuid:pk>", view=transplant_update_view, name="update"),
    path("delete/<uuid:pk>", view=transplant_delete_view, name="delete"),
]
