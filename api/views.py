from datetime import datetime

import pytz
from dateutil.parser import parse
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
from web.models import Plant
from web.tasks_utils import prepare_queryset


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer

    # if type float or int in request, variable need to be tuple (min_val, max_val)
    # slug because from front we send slug english name
    @staticmethod
    def filtering_attr(request, variable, data, type_attr):
        def convert_string_to_datetime(string: str) -> datetime:
            dt_naive = parse(string)
            utc = pytz.utc
            # convert datetime instance to a specific timezone
            return utc.localize(dt_naive)

        def filtering_text_types(plant):
            return plant[obj.name] == request.GET[variable]

        def filtering_int_float_types(plant):
            return request.GET[variable][0] <= plant[obj.name] <= request.GET[variable][1]

        def filtering_date_types(plant):
            # if plant instance doesn't have required attribute, throw it out!
            if plant[obj.name] is None:
                return False

            parameters = request.query_params.getlist(variable)
            floor_value = convert_string_to_datetime(parameters[0])
            ceiling_value = convert_string_to_datetime(parameters[1])

            return floor_value <= plant[obj.name] <= ceiling_value

        def filtering_taxon_organization_types(plant):
            return plant[translate[variable]] == request.GET[variable]

        translate = xlsx_columns_choices_dict()
        if type_attr == "custom":
            obj = Attribute.objects.get(slug=variable)
            func = filtering_text_types
            if obj.datatype == Attribute.TYPE_DATE:
                func = filtering_date_types
            elif obj.datatype == Attribute.TYPE_INT or obj.datatype == Attribute.TYPE_FLOAT:
                func = filtering_int_float_types
            data = filter(func, data)
        else:
            data = filter(filtering_taxon_organization_types, data)
        return data

    # slug because from front we send slug english name
    def filter_data(self, request, data):
        filters = request.GET
        custom_attr = [attr.slug for attr in Attribute.objects.all()]
        for variable in filters:
            if variable in custom_attr:
                data = self.filtering_attr(request, variable, data, "custom")
            elif variable != "organization":
                data = self.filtering_attr(request, variable, data, "taxon")
            elif variable == "organization":
                data = self.filtering_attr(request, variable, data, "organization")
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
        attribute_list = attributes_default_choices()
        attribute_list.extend(attributes_custom_choices())
        attribute_list.extend(attribute_taxon_choices())
        return Response(attribute_list)
