from eav.models import Entity, Value
from rest_framework import serializers

from web.models import Plant


# class EntitySerializer(serializers.ModelSerializer):
#     eav_fields = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Entity
#         fields = ['id', 'name', 'eav_fields']
#
#     def get_eav_fields(self, obj):
#         request = self.context['request']
#         eav_data = {}
#         values = Value.objects.filter(entity=obj)
#         for value in values:
#             if value.attribute.entity_type == request.query_params.get('entity_type'):
#                 attribute_name = value.attribute.name
#                 eav_data[attribute_name] = value.value
#         return eav_data


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ("number", "digitized_at", "latin_name", "name", "organization", "genus")

    def to_representation(self, instance):
        instance = super(PlantSerializer, self).to_representation(instance)
        plants = self.context.get("plants")
        eav_fields = self.context.get("eav_fields")
        for field in eav_fields:
            instance.setdefault(field.attribute.name, field.value)
        return instance
