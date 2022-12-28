from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from eav.models import Attribute, Entity

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
    "data": Attribute.TYPE_DATE,
    "float": Attribute.TYPE_FLOAT,
}

TAXON_NAME = {
    "phylum": Taxon.objects.filter(level="Phylum"),
    "class": Taxon.objects.filter(level="Class"),
    "order": Taxon.objects.filter(level="Order"),
    "family": Taxon.objects.filter(level="Family"),
    "genus": Taxon.objects.filter(level="Genus"),
}


def ajax_response(request):
    response_data = {}
    name = request.POST.get("name_attr")
    type_attr = request.POST.get("type_attr")
    response_data["name_attr"] = name
    response_data["type_attr"] = type_attr
    Attribute.objects.create(name=name, datatype=ATTRIBUTE_TYPE[type_attr])
    return JsonResponse(response_data)


def get_all_taxons(genus_id):
    taxons = {}
    obj = Taxon.objects.filter(id=genus_id).first()
    while obj.parent:
        taxons[f"{obj.level}_title"] = obj.title
        taxons[f"{obj.level}_latin_title"] = obj.latin_title
        obj = Taxon.objects.filter(id=obj.parent.id).first()

    return taxons


class PlantMixin:
    template_name = "web/plant_form.html"
    context_object_name = "plant_form"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "form_classification": TaxonForm(),
            "attr_form_view": AttributeFormView(),
            "attr_form": AttributeForm(),
            "taxon_name": TAXON_NAME,
        }

    def get_initial(self):
        attr_form_view = AttributeFormView(self.request.POST)
        taxon_form = TaxonForm(self.request.POST)
        if attr_form_view.is_valid():
            print(attr_form_view.cleaned_data)
        if taxon_form.is_valid():
            print(taxon_form.cleaned_data)
        return {"attr_form_view": attr_form_view, "form_classification": taxon_form}

    def get_success_url(self):
        return reverse("plant", args=(self.object.id,))


class PlantCreateView(PlantMixin, CreateView):
    form_class = PlantForm


class PlantUpdateView(PlantMixin, UpdateView):
    slug_field = "id"
    slug_url_kwarg = "id"
    form_class = PlantForm

    def get_queryset(self):
        return Plant.objects.all()

    def get_context_data(self, **kwargs):
        classification_values = get_all_taxons(self.object.genus.id)
        form_classification = TaxonForm(classification_values)

        eav_fields_values = Entity(self.object).get_values_dict()
        attr_form_view = AttributeFormView(eav_fields_values)

        return {
            **super().get_context_data(**kwargs),
            "form_classification": form_classification,
            "attr_form_view": attr_form_view,
            "attr_form": AttributeForm(),
            "taxon_name": TAXON_NAME,
        }
