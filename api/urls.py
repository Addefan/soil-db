from django.urls import path

from api.views import PlantAPIView, AttributesAPIView, ChangePasswordAPIView

app_name = "api"

urlpatterns = [
    path("plants/", PlantAPIView.as_view(), name="get_plants"),
    path("attributes/", AttributesAPIView.as_view(), name="get_attributes"),
    path("change_password/", ChangePasswordAPIView.as_view(), name="change_password"),
]
