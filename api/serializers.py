from rest_framework import serializers

from web.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    genus = serializers.StringRelatedField()

    class Meta:
        model = Plant
        fields = "__all__"

    # def to_representation(self, instance):
    #     instance = super(PlantSerializer, self).to_representation(instance)
    #     return self.context["data"].get(instance["number"], {})
