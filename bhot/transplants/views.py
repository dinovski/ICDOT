import django_tables2 as tables
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from bhot.transplants.models import Transplant


class TransplantTableView(LoginRequiredMixin, tables.SingleTableView):
    class TransplantTable(tables.Table):
        class Meta:
            model = Transplant
            fields = ("transplant_date", "donor_ref", "recipient_ref")

        view = tables.LinkColumn(
            "transplants:detail",
            args=[tables.utils.Accessor("pk")],
            text="View",
            attrs={"a": {"class": "btn btn-primary btn-sm"}},
        )

        edit = tables.LinkColumn(
            "transplants:update",
            args=[tables.utils.Accessor("pk")],
            text="Edit",
            attrs={"a": {"class": "btn btn-secondary btn-sm"}},
        )

    model = Transplant
    table_class = TransplantTable


transplant_table_view = TransplantTableView.as_view()


class TransplantCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transplant
    fields = "__all__"


transplant_create_view = TransplantCreateView.as_view()


class TransplantDetailView(LoginRequiredMixin, DetailView):
    model = Transplant


transplant_detail_view = TransplantDetailView.as_view()


class TransplantUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Transplant
    fields = "__all__"


transplant_update_view = TransplantUpdateView.as_view()


class TransplantDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Transplant
    success_url = reverse_lazy("transplants:table")


transplant_delete_view = TransplantDeleteView.as_view()
