from django.urls import path
from web.views import PlantDetailView
from web.view.add_plant import PlantCreateFormView, ajax_response

urlpatterns = [
    path("plants/add/", PlantCreateFormView.as_view(), name="plants_add"),
    path("/ajax_response", ajax_response, name="ajax_response"),
    path("plant/<int:number>", PlantDetailView.as_view(), name="plant"),
]
