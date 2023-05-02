from eav.models import Value, Attribute
from rest_framework import serializers

from web.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    genus = serializers.StringRelatedField()

    class Meta:
        model = Plant
        exclude = ["digitized_at", "id"]


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ("datatype", "name")


class ValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)
    _datatypes = ("bool", "csv", "date", "float", "int", "json", "text")

    class Meta:
        model = Value
        exclude = (
            "id",
            "entity_id",
            "entity_uuid",
            "created",
            "modified",
            "generic_value_id",
            "entity_ct",
            "value_enum",
            "generic_value_ct",
        )

    def to_representation(self, instance):
        instance = super(ValueSerializer, self).to_representation(instance)
        for datatype in self._datatypes:
            if instance["attribute"]["datatype"] == datatype:
                continue
            instance.pop(f"value_{datatype}")
        attribute = instance.pop("attribute")
        instance.setdefault(attribute["name"], instance.pop(f"value_{attribute['datatype']}"))
        return instance


class FullPlantModelSerializer(PlantSerializer):
    eav_values = ValueSerializer(read_only=True, many=True)

    def to_representation(self, instance):
        instance = super(FullPlantModelSerializer, self).to_representation(instance)
        eav_values = instance.pop("eav_values")
        for eav_value in eav_values:
            instance.update(eav_value)
        return instance

    class Meta(PlantSerializer.Meta):
        exclude = []
