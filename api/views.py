from rest_framework import generics
from rest_framework.response import Response

from api.serializers import PlantSerializer
from web.choices import xlsx_columns_choices
from web.models import Plant
from web.tasks_utils import prepare_queryset


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer
    queryset = Plant.objects.prefetch_related("organization")

    @staticmethod
    def filtering(request, parament, raw_data):
        def filtering_solve(plant):
            return plant[parament] == request.GET[parament]

        raw_data = filter(filtering_solve, raw_data)
        return raw_data

    def filter_raw_data(self, request, raw_data):
        filters = request.GET
        print(raw_data)
        for parament in filters:
            raw_data = self.filtering(request, parament, raw_data)
        return raw_data

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        raw_data = prepare_queryset(columns=[choice[0] for choice in xlsx_columns_choices()], qs=qs)
        filtered_raw_data = self.filter_raw_data(request, raw_data)
        data = {instance.get("Уникальный номер"): instance for instance in filtered_raw_data}
        serializer = PlantSerializer(qs, many=True, context={"data": data})
        return Response(serializer.data)
