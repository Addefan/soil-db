from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from eav.models import Attribute, Entity

from web.enums import TaxonLevel
from web.forms import (
    PlantForm,
    AttributeForm,
    AttributeFormView,
    TaxonForm,
)
from web.models import Taxon, Plant

ATTRIBUTE_TYPE = {
    "integer": Attribute.TYPE_INT,
    "string": Attribute.TYPE_TEXT,
    "date": Attribute.TYPE_DATE,
    "float": Attribute.TYPE_FLOAT,
}

TAXON_NAME = {
    "phylum": Taxon.objects.filter(level=TaxonLevel.phylum),
    "class": Taxon.objects.filter(level=TaxonLevel.klass),
    "order": Taxon.objects.filter(level=TaxonLevel.order),
    "family": Taxon.objects.filter(level=TaxonLevel.family),
    "genus": Taxon.objects.filter(level=TaxonLevel.genus),
}


def ajax_response(request):
    response_data = {}
    name = request.POST.get("name_attr")
    type_attr = request.POST.get("type_attr")
    response_data["name_attr"] = name
    response_data["type_attr"] = type_attr
    Attribute.objects.create(name=name, datatype=ATTRIBUTE_TYPE[type_attr])
    return JsonResponse(response_data)


def get_all_taxons(genus):
    """A function returning dictionary with data based on hierarchy of given genus"""
    taxons = {}
    for taxon in genus.get_ancestors(include_self=True):
        taxons[f"{taxon.level}_title"] = taxon.title
        taxons[f"{taxon.level}_latin_title"] = taxon.latin_title

    return taxons


class PlantMixin:
    slug_field = "number"
    slug_url_kwarg = "number"
    template_name = "web/plant_form.html"
    context_object_name = "plant_form"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "form_classification": kwargs["form_classification"]
            if "form_classification" in kwargs.keys()
            else TaxonForm(),
            "attr_form_view": kwargs["attr_form_view"] if "attr_form_view" in kwargs.keys() else AttributeFormView(),
            "attr_form": AttributeForm(),
            "taxon_name": TAXON_NAME,
        }

    def get_initial(self):
        attr_form_view = AttributeFormView(self.request.POST)
        taxon_form = TaxonForm(self.request.POST)
        attr_form_view.is_valid()
        taxon_form.is_valid()
        return {"attr_form_view": attr_form_view, "form_classification": taxon_form}

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                form_classification=TaxonForm(self.request.POST),
                attr_form_view=AttributeFormView(self.request.POST),
            )
        )

    def get_success_url(self):
        return reverse("plant", args=(self.object.number,))


class PlantCreateView(PlantMixin, LoginRequiredMixin, CreateView):
    form_class = PlantForm


class PlantUpdateView(PlantMixin, LoginRequiredMixin, UpdateView):
    form_class = PlantForm
    model = Plant

    def get_context_data(self, **kwargs):
        classification_values = get_all_taxons(self.object.genus)
        form_classification = TaxonForm(classification_values)

        eav_fields_values = Entity(self.object).get_values_dict()
        attr_form_view = AttributeFormView(eav_fields_values)

        return {
            **super().get_context_data(**kwargs),
            "form_classification": form_classification,
            "attr_form_view": attr_form_view,
            "attr_form": AttributeForm(),
            "taxon_name": TAXON_NAME,
            "number": self.kwargs[self.slug_url_kwarg],
        }
