from rest_framework import generics, views, status, filters
from rest_framework.response import Response

from api.filters import PlantFilterBackend
from api.serializers import PlantSerializer, PasswordSerializer, CustomAttributeSerializer
from web.choices import (
    attributes_default_choices,
    attributes_custom_choices,
    attribute_taxon_choices,
)
from web.models import Plant
from web.services.password import create_password_change_request


class CustomAttributeView(views.APIView):
    def post(self, request):
        serializer = CustomAttributeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "error with CustomAttributeView"})
        serializer.save()
        return Response(serializer.data)


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer
    filter_backends = (filters.SearchFilter, PlantFilterBackend)
    search_fields = ("number", "name", "latin_name")
    queryset = Plant.objects.optimize_queries().select_related("organization")


class AttributesAPIView(views.APIView):
    def get(self, request):
        attribute_list = attributes_default_choices()
        attribute_list.extend(attributes_custom_choices())
        attribute_list.extend(attribute_taxon_choices())
        return Response(attribute_list)


class ChangePasswordAPIView(views.APIView):
    def post(self, request):
        serializer = PasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        create_password_change_request(request)
        return Response({"success": True})
