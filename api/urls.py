from django.urls import path

from api.views import PlantAPIView, AttributesAPIView, CustomAttributeView

urlpatterns = [
    path("plants/", PlantAPIView.as_view(), name="get_plants"),
    path("attributes/", AttributesAPIView.as_view(), name="get_attributes"),
    path("custom_attributes/", CustomAttributeView.as_view(), name="custom_attributes"),
]
