from django.shortcuts import render
from rest_framework import generics

from api.serializers import PlantSerializer
from web.models import Plant


class PlantAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer
    queryset = Plant.objects.all()
