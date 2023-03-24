from eav.models import Attribute
from rest_framework import generics
from rest_framework.response import Response

from api.serializers import PlantSerializer
from web.choices import xlsx_columns_choices
from web.models import Plant
from web.tasks_utils import prepare_queryset


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer
    queryset = Plant.objects.prefetch_related("organization")

    # if type str or int in request, variable need to be tuple (min_val, max_val)
    @staticmethod
    def filtering(request, variable, raw_data):
        def filtering_text_types(plant):
            return plant[variable].lower() == request.GET[variable].lower()

        def filtering_int_float_types(plant):
            return request.GET[variable][0] <= plant[variable] <= request.GET[variable][1]

        if Attribute.objects.get(name=variable).datatype == "text":
            raw_data = filter(filtering_text_types, raw_data)
        elif Attribute.objects.get(variable).datatype == "int" or Attribute.objects.get(variable).datatype == "float":
            raw_data = filter(filtering_int_float_types, raw_data)
        return raw_data

    def filter_raw_data(self, request, raw_data):
        filters = request.GET
        for parament in filters:
            raw_data = self.filtering(request, parament, raw_data)
        return raw_data

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        data = prepare_queryset(columns=[choice[0] for choice in xlsx_columns_choices()], qs=qs)
        if len(request.GET) != 0:
            data = self.filter_raw_data(request, data)
        data = {instance.get("Уникальный номер"): instance for instance in data}
        serializer = PlantSerializer(qs, many=True, context={"data": data})
        return Response(serializer.data)
