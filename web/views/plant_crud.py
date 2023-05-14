import html
from typing import Callable

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic import DeleteView
from eav.models import Entity

from web.forms import (
    PlantForm,
    AttributeForm,
    AttributeMainForm,
    TaxonForm,
)
from web.models import Plant
from web.models import Taxon


# don't use '@cache' to avoid not reloading suggestions
def get_taxa():
    taxa = Taxon.objects.values("level").annotate(titles=ArrayAgg("title"), latin_titles=ArrayAgg("latin_title"))
    return taxa


def get_all_taxa(genus):
    """A function returning dictionary with data based on hierarchy of given genus"""
    taxa = {}
    for taxon in genus.ancestors(include_self=True):
        taxa[f"{taxon.level}_title"] = taxon.title
        taxa[f"{taxon.level}_latin_title"] = taxon.latin_title

    return taxa


def escape(func: Callable) -> Callable:
    """
    decorator escapes text to prevent XSS attack
    """

    def wrapper(self, cleaned_data: dict) -> str:
        cleaned_data["name"] = html.escape(cleaned_data["name"])
        return func(self, cleaned_data)

    return wrapper


class PlantMixin:
    slug_field = "number"
    slug_url_kwarg = "number"
    template_name = "web/plant_form.html"
    context_object_name = "plant_form"

    def get_context_data(self, **kwargs):
        form_classification = kwargs["form_classification"] if "form_classification" in kwargs.keys() else TaxonForm()
        attr_form_view = kwargs["attr_form_view"] if "attr_form_view" in kwargs.keys() else AttributeMainForm()
        return {
            **super().get_context_data(**kwargs),
            "form_classification": form_classification,
            "attr_form_view": attr_form_view,
            "attr_form": AttributeForm(),
            "taxon_levels": get_taxa(),
        }

    def get_initial(self):
        attr_form_view = AttributeMainForm(self.request.POST)
        taxon_form = TaxonForm(self.request.POST)
        attr_form_view.is_valid()
        taxon_form.is_valid()
        return {
            "attr_form_view": attr_form_view,
            "form_classification": taxon_form,
            "user_organization": self.request.user.organization,
        }

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                form_classification=TaxonForm(self.request.POST),
                attr_form_view=AttributeMainForm(self.request.POST),
            )
        )

    def get_success_url(self):
        return reverse("plant", args=(self.object.number,))


class PlantCreateView(PlantMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = PlantForm

    @escape
    def get_success_message(self, cleaned_data):
        return f"Вы успешно добавили растение <strong>{cleaned_data['name']}</strong>"


class PlantUpdateView(PlantMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    form_class = PlantForm
    model = Plant

    def get_context_data(self, **kwargs):
        classification_values = get_all_taxa(self.object.genus)
        form_classification = TaxonForm(classification_values)

        eav_fields_values = Entity(self.object).get_values_dict()
        attr_form_view = AttributeMainForm(eav_fields_values)

        return {
            **super().get_context_data(**kwargs),
            "form_classification": form_classification,
            "attr_form_view": attr_form_view,
            "attr_form": AttributeForm(),
            "taxon_levels": get_taxa(),
            "number": self.kwargs[self.slug_url_kwarg],
        }

    @escape
    def get_success_message(self, cleaned_data):
        return f"Вы успешно изменили растение <strong>{cleaned_data['name']}</strong>"


class PlantDeleteView(SuccessMessageMixin, DeleteView):
    model = Plant
    slug_field = "number"
    slug_url_kwarg = "number"
    success_url = reverse_lazy("plants")

    def get_success_message(self, cleaned_data):
        return f"Растение <strong>{self.object.name}</strong> успешно удалено"

    def get(self, request, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        if self.request.user.organization != self.object.organization:
            return redirect("plants")
        return super().form_valid(form)
