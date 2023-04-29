import html
from functools import cache
from typing import Callable

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from eav.models import Attribute, Entity

from web.enums import TaxonLevel
from web.forms import (
    PlantForm,
    AttributeForm,
    AttributeMainForm,
    TaxonForm,
)
from web.models import Taxon, Plant


@cache
def get_taxa():
    # TODO запросить всю таблицу, и в коде сдлеать эту группировку. Куча SQL запросов здесь не нужна
    return {
        "phylum": Taxon.objects.filter(level=TaxonLevel.phylum),
        "class": Taxon.objects.filter(level=TaxonLevel.klass),
        "order": Taxon.objects.filter(level=TaxonLevel.order),
        "family": Taxon.objects.filter(level=TaxonLevel.family),
        "genus": Taxon.objects.filter(level=TaxonLevel.genus),
    }

# TODO функции должны называться как глаголы. Название функции слишком общее, хотя видимо оно работает с созданием
#  атрибута. Значит, это вообще не response, а save_attribute(). И вообще это view, хорошей практикой является
#  заканчивать название view-функций на _view
def ajax_response(request):
    response_data = {}
    # TODO нужен сериализатор
    name = request.POST.get("name_attr")
    type_attr = request.POST.get("type_attr")
    response_data["name_attr"] = name
    response_data["type_attr"] = type_attr
    attr = Attribute.objects.create(name=name, datatype=type_attr)
    response_data["slug_name"] = attr.slug
    return JsonResponse(response_data)


def get_all_taxa(genus):
    """A function returning dictionary with data based on hierarchy of given genus"""
    taxa = {}
    for taxon in genus.ancestors(include_self=True):
        taxa[f"{taxon.level}_title"] = taxon.title
        taxa[f"{taxon.level}_latin_title"] = taxon.latin_title

    return taxa


def escape(func: Callable) -> Callable:
    # TODO комментарий к функции должен быть в """ """
    # decorator escapes text to prevent XSS attack
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
        return {
            **super().get_context_data(**kwargs),
            # TODO вынести в переменную, чтобы строчка не уходила в закат
            "form_classification": kwargs["form_classification"]
            if "form_classification" in kwargs.keys()
            else TaxonForm(),
            # TODO вынести в переменную, чтобы строчка не уходила в закат
            "attr_form_view": kwargs["attr_form_view"] if "attr_form_view" in kwargs.keys() else AttributeMainForm(),
            "attr_form": AttributeForm(),
            "taxon_name": get_taxa(),
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
            "taxon_name": get_taxa(),
            "number": self.kwargs[self.slug_url_kwarg],
        }

    @escape
    def get_success_message(self, cleaned_data):
        return f"Вы успешно изменили растение <strong>{cleaned_data['name']}</strong>"
