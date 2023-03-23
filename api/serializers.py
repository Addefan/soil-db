from rest_framework import serializers

from web.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()

    class Meta:
        model = Plant
        fields = (
            "number",
            "organization",
        )

    def to_representation(self, instance):
        instance = super(PlantSerializer, self).to_representation(instance)
        return self.context.get("data") if instance["number"] in self.context.get("data").keys() else {}
