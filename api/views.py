from django.db.models import QuerySet
from eav.models import Value, Attribute
from rest_framework import generics
from rest_framework.response import Response

from api.serializers import PlantSerializer
from web.models import Plant, Taxon


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer
    queryset = Plant.objects.prefetch_related("organization")

    @staticmethod
    def get_eav_fields(queryset: QuerySet):
        eav_fields: dict = {}
        for item in queryset:
            if eav_fields.get(item.entity_id) is None:
                eav_fields[item.entity_id] = [item]
            else:
                eav_fields[item.entity_id].append(item)
        return eav_fields

    def get(self, request, *args, **kwargs):
        plants = self.get_queryset()
        attributes = Attribute.objects.all()
        plants_id = [plant.id for plant in plants]
        eav_fields_as_queryset = Value.objects.filter(entity_id__in=plants_id).prefetch_related("attribute")
        eav_fields: dict = self.get_eav_fields(eav_fields_as_queryset)
        taxa = {taxon.id: taxon for taxon in Taxon.objects.all()}
        serializer = PlantSerializer(
            plants, many=True, context={"eav_fields": eav_fields, "taxa": taxa, "attributes": attributes}
        )
        return Response(serializer.data)
