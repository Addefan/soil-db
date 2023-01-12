from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from eav.models import Attribute

from web.enums import TaxonLevel
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
    "phylum": Taxon.objects.filter(level=TaxonLevel.phylum),
    "class": Taxon.objects.filter(level=TaxonLevel.klass),
    "order": Taxon.objects.filter(level=TaxonLevel.order),
    "family": Taxon.objects.filter(level=TaxonLevel.family),
    "genus": Taxon.objects.filter(level=TaxonLevel.genus),
}


class PlantCreateFormView(CreateView):
    form_class = PlantForm
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
        print(self.request.POST)
        attr_form_view = AttributeFormView(self.request.POST)
        taxon_form = TaxonForm(self.request.POST)
        if attr_form_view.is_valid():
            print(attr_form_view.cleaned_data)
        if taxon_form.is_valid():
            print(taxon_form.cleaned_data)
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


class PlantUpdateView(UpdateView):
    pass
