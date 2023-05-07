from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from web.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    genus = serializers.StringRelatedField()

    class Meta:
        model = Plant
        exclude = ["digitized_at", "id"]


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError(error.messages)
        return password
