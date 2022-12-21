from django.contrib import admin
from django.urls import path

from web.views import PlantDetailView

urlpatterns = [path("plant/<int:number>", PlantDetailView.as_view(), name="plant")]
