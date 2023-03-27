from eav.models import Attribute
from rest_framework import generics, views
from rest_framework.response import Response

from api.serializers import PlantSerializer
from web.choices import (
    xlsx_columns_choices,
    attributes_default_choices,
    attributes_custom_choices,
    attribute_taxon_choices,
)
from web.models import Plant
from web.tasks_utils import prepare_queryset


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer

    # queryset = Plant.objects.prefetch_related("organization")

    # if type float or int in request, variable need to be tuple (min_val, max_val)
    @staticmethod
    def filtering_custom_attr(request, variable, raw_data):
        def filtering_text_types(plant):
            return plant[variable] == request.GET[variable]

        def filtering_int_float_types(plant):
            return request.GET[variable][0] <= plant[variable] <= request.GET[variable][1]

        if Attribute.objects.get(name=variable).datatype == "text":
            raw_data = filter(filtering_text_types, raw_data)
        elif (
            Attribute.objects.get(name=variable).datatype == "int"
            or Attribute.objects.get(name=variable).datatype == "float"
        ):
            raw_data = filter(filtering_int_float_types, raw_data)
        return raw_data

    # slug because from front we send slug english name
    def filter_raw_data(self, request, raw_data):
        filters = request.GET
        for param in filters:
            if param in [attr.slug for attr in Attribute.objects.all()]:
                raw_data = self.filtering_custom_attr(request, param, raw_data)
            elif param != "organization":
                raw_data = self.filtering_taxon_attr(request, param, raw_data)
        return raw_data

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
            data = self.filter_raw_data(request, data)
        numbers = [instance.get("Уникальный номер") for instance in data]
        filtered_qs = self.get_queryset(True, numbers)
        serializer = PlantSerializer(filtered_qs, many=True)
        return Response(serializer.data)


class AttributesAPIView(views.APIView):
    def get(self, request):
        return Response(attributes_default_choices() | attributes_custom_choices() | attribute_taxon_choices())
