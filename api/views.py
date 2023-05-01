from datetime import datetime

from dateutil.parser import parse
from django.db.models import Q
from eav.models import Attribute
from rest_framework import generics, views, status
from rest_framework.response import Response

from api.serializers import PlantSerializer, PasswordSerializer
from web.choices import (
    xlsx_columns_choices,
    attributes_default_choices,
    attributes_custom_choices,
    attribute_taxon_choices,
    xlsx_columns_choices_dict,
)
from web.models import Plant
from web.services.password import create_password_change_request
from web.tasks_utils import prepare_queryset


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer

    # TODO сделать через django-filters

    # if type float or int in request, variable need to be tuple (min_val, max_val)
    # slug because from front we send slug english name
    @staticmethod
    def filtering_attr(request, variable, data, type_attr):
        # TODO почему функции внутри функции находятся?
        def convert_string_to_datetime(string: str) -> datetime:
            dt_naive = parse(string)
            return dt_naive

        def filtering_text_types(plant):
            return plant[obj.name] in parameters

        def filtering_int_float_types(plant):
            return float(parameters[0]) <= plant[obj.name] <= float(parameters[1])

        def filtering_date_types(plant):
            # if plant instance doesn't have required attribute, throw it out!
            if plant[obj.name] is None:
                return False

            floor_value = convert_string_to_datetime(parameters[0])
            ceiling_value = convert_string_to_datetime(parameters[1])

            return floor_value <= plant[obj.name] <= ceiling_value

        def filtering_taxon_organization_types(plant):
            return plant[translate[variable]] in parameters

        parameters = request.query_params.getlist(variable)
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
            elif variable == "page":
                continue
            elif variable == "search":
                continue
            elif variable != "organization":
                data = self.filtering_attr(request, variable, data, "taxon")
            elif variable == "organization":
                data = self.filtering_attr(request, variable, data, "organization")
        return data

    def get_queryset(self, filtering=False, numbers=None, search_string=None):
        plants = Plant.objects.prefetch_related("organization")
        if not filtering:
            return plants
        else:
            if numbers:
                return Plant.objects.filter(number__in=numbers)
            elif search_string:
                return Plant.objects.filter(
                    Q(number__icontains=search_string)
                    | Q(name__icontains=search_string)
                    | Q(latin_name__icontains=search_string)
                )

    def get(self, request, *args, **kwargs):
        filtering_flag = True if "search" in request.GET.keys() else False
        if filtering_flag:
            qs = self.get_queryset(filtering=True, search_string=request.GET["search"])
        else:
            qs = self.get_queryset()
        data = prepare_queryset(columns=[choice[0] for choice in xlsx_columns_choices()], qs=qs)
        if request.GET:
            data = self.filter_data(request, data)
        numbers = [instance.get("Уникальный номер") for instance in data]
        filtered_qs = self.paginate_queryset(self.get_queryset(True, numbers))
        serializer = PlantSerializer(filtered_qs, many=True)
        return Response(serializer.data)


class AttributesAPIView(views.APIView):
    def get(self, request):
        attribute_list = attributes_default_choices()
        attribute_list.extend(attributes_custom_choices())
        attribute_list.extend(attribute_taxon_choices())
        return Response(attribute_list)


class ChangePasswordAPIView(views.APIView):
    def post(self, request):
        serializer = PasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        create_password_change_request(request)
        return Response({"success": True})
