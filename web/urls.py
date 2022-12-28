from django.urls import path
from web.views import PlantDetailView, PlantCreateView, ajax_response, SoilLoginView, main, PlantUpdateView

urlpatterns = [
    path("login/", SoilLoginView.as_view(), name="login"),
    path("", main, name="main"),
    path("plants/add/", PlantCreateView.as_view(), name="plants_add"),
    path("/ajax_response", ajax_response, name="ajax_response"),
    path("plants/<int:number>", PlantDetailView.as_view(), name="plant"),
]
