from django.urls import path

from api.views import PlantAPIView, AttributesAPIView

urlpatterns = [
    path("plants/", PlantAPIView.as_view(), name="get_plants"),
    path("attributes/", AttributesAPIView.as_view(), name="get_attributes"),
]
