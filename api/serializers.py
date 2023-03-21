from rest_framework import serializers

from web.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        exclude = ("genus",)
