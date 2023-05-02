from eav.models import Value
from rest_framework import serializers

from web.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    genus = serializers.StringRelatedField()

    class Meta:
        model = Plant
        exclude = ["digitized_at", "id"]


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = "__all__"


class FullPlantModelSerializer(PlantSerializer):
    eav_values = ValueSerializer(read_only=True, many=True)

    class Meta(PlantSerializer.Meta):
        exclude = []
