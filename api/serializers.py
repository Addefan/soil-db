from eav.models import Attribute
from rest_framework import serializers

from web.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    genus = serializers.StringRelatedField()

    class Meta:
        model = Plant
        exclude = ["digitized_at", "id"]


class CustomAttributeSerializer(serializers.Serializer):
    name_attr = serializers.CharField()
    type_attr = serializers.CharField()
    slug_name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        attr = Attribute.objects.create(name=validated_data["name_attr"], datatype=validated_data["type_attr"])
        validated_data["slug_name"] = attr.slug
        return validated_data
