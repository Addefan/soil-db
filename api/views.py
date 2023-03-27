from eav.models import Attribute
from rest_framework import generics, views
from rest_framework.response import Response

from api.serializers import PlantSerializer
from web.choices import (
    xlsx_columns_choices,
    attributes_default_choices,
    attributes_custom_choices,
    attribute_taxon_choices,
    xlsx_columns_choices_dict,
)
from web.enums import TaxonLevel
from web.models import Plant, Taxon
from web.tasks_utils import prepare_queryset


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer

    # queryset = Plant.objects.prefetch_related("organization")

    # if type float or int in request, variable need to be tuple (min_val, max_val)
    # slug because from front we send slug english name
    @staticmethod
    def filtering_attr(request, variable, data, type_attr):
        def filtering_text_types(plant):
            return plant[variable] == request.GET[variable]

        def filtering_int_float_types(plant):
            return request.GET[variable][0] <= plant[variable] <= request.GET[variable][1]

        def filtering_taxon_types(plant):
            return plant[translate[variable]] == request.GET[variable]

        if type_attr == "custom":
            if Attribute.objects.get(slug=variable).datatype == "text":
                data = filter(filtering_text_types, data)
            elif (
                Attribute.objects.get(slug=variable).datatype == "int"
                or Attribute.objects.get(slug=variable).datatype == "float"
            ):
                data = filter(filtering_int_float_types, data)
        elif type_attr == "taxon":
            translate = xlsx_columns_choices_dict()
            data = filter(filtering_taxon_types, data)
        return data

    # slug because from front we send slug english name
    def filter_data(self, request, data):
        filters = request.GET
        for variable in filters:
            if variable in [attr.slug for attr in Attribute.objects.all()]:
                data = self.filtering_attr(request, variable, data, "custom")
            elif variable != "organization":
                data = self.filtering_attr(request, variable, data, "taxon")
        return data

    def get_queryset(self, filtering=False, numbers=None):
        plants = Plant.objects.prefetch_related("organization")
        if not filtering:
            return plants
        else:
            return Plant.objects.filter(number__in=numbers)

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        data = prepare_queryset(columns=[choice[0] for choice in xlsx_columns_choices()], qs=qs)
        if request.GET:
            data = self.filter_data(request, data)
        numbers = [instance.get("Уникальный номер") for instance in data]
        filtered_qs = self.get_queryset(True, numbers)
        serializer = PlantSerializer(filtered_qs, many=True)
        return Response(serializer.data)


class AttributesAPIView(views.APIView):
    def get(self, request):
        return Response(attributes_default_choices() | attributes_custom_choices() | attribute_taxon_choices())
