from django.urls import path

from api.views import PlantAPIView, AttributesAPIView, FullPlantModelAPIView

urlpatterns = [
    path("plants/", PlantAPIView.as_view(), name="get_plants"),
    path("attributes/", AttributesAPIView.as_view(), name="get_attributes"),
    path("entire_plants/", FullPlantModelAPIView.as_view(), name="full_plant_model"),
]
