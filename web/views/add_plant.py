from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from eav.models import Attribute

from web.forms import (
    PlantForm,
    AttributeForm,
    AttributeFormView,
    TaxonForm,
)
from web.models import Taxon

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


class PlantCreateFormView(CreateView):
    form_class = PlantForm
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
        print(self.request.POST)
        attr_form_view = AttributeFormView(self.request.POST)
        taxon_form = TaxonForm(self.request.POST)
        if attr_form_view.is_valid():
            print(attr_form_view.cleaned_data)
        if taxon_form.is_valid():
            print(taxon_form.cleaned_data)
        return {"attr_form_view": attr_form_view, "form_classification": taxon_form}

    def get_success_url(self):
        return reverse("plant", args=(self.object.id,))


def ajax_response(request):
    response_data = {}
    print(request.POST)
    name = request.POST.get("name_attr")
    type_attr = request.POST.get("type_attr")
    print(name, type_attr)
    response_data["name_attr"] = name
    response_data["type_attr"] = type_attr
    Attribute.objects.create(name=name, datatype=ATTRIBUTE_TYPE[type_attr])
    return JsonResponse(response_data)
