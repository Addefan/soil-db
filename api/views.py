from rest_framework import generics, views
from rest_framework.response import Response

from api.serializers import PlantSerializer
from web.choices import xlsx_columns_choices, attributes_default_choices, attributes_custom_choices
from web.models import Plant
from web.tasks_utils import prepare_queryset


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer
    queryset = Plant.objects.prefetch_related("organization")

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        raw_data = prepare_queryset(columns=[choice[0] for choice in xlsx_columns_choices()], qs=qs)
        data = {instance.get("Уникальный номер"): instance for instance in raw_data}
        serializer = PlantSerializer(qs, many=True, context={"data": data})
        return Response(serializer.data)


class AttributesAPIView(views.APIView):
    def get(self, request):
        return Response(attributes_default_choices() | attributes_custom_choices())
