from django.urls import path

from api.views import PlantAPIView

urlpatterns = [path("get/", PlantAPIView.as_view(), name="get_plants")]
