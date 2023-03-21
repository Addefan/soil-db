from eav.models import Value
from rest_framework import generics
from rest_framework.response import Response

from api.serializers import PlantSerializer
from web.models import Plant, Taxon


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer
    queryset = Plant.objects.prefetch_related("organization")

    def get(self, request, *args, **kwargs):
        plants = self.get_queryset()
        plants_id = [plant.id for plant in plants]
        eav_fields = Value.objects.filter(entity_id__in=plants_id).prefetch_related("attribute")
        taxa = {taxon.id: taxon for taxon in Taxon.objects.all()}
        serializer = PlantSerializer(plants, many=True, context={"eav_fields": eav_fields, "taxa": taxa})
        return Response(serializer.data)
