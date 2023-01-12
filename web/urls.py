from django.urls import path

from web.views import (
    ProfileFormView,
    PlantDeleteView,
    PlantDetailView,
    PlantCreateView,
    ajax_response,
    SoilLoginView,
    PlantsListView,
    PlantUpdateView,
)

urlpatterns = [
    path("plants/", PlantsListView.as_view(), name="plants"),  # TODO: сейчас заглушка
    path("profile/", ProfileFormView.as_view(), name="profile"),
    path("login/", SoilLoginView.as_view(), name="login"),
    path("plants/add/", PlantCreateView.as_view(), name="plants_add"),
    path("plants/<int:number>", PlantDetailView.as_view(), name="plant"),
    path("plants/<int:number>/update", PlantUpdateView.as_view(), name="plant_update"),
    path("plants/<int:number>/delete", PlantDeleteView.as_view(), name="plants_delete"),
    path("ajax_response/", ajax_response, name="ajax_response"),
]
