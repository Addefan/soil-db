from django.urls import path

from web.views import (
    ProfileFormView,
    PlantDeleteView,
    PlantDetailView,
    PlantCreateView,
    ajax_response,
    PlantsListView,
    LoginView,
    PlantUpdateView,
    LogoutView,
)

urlpatterns = [
    path("", PlantsListView.as_view(), name="plants"),
    path("plants/", PlantsListView.as_view(), name="plants"),
    path("profile/", ProfileFormView.as_view(), name="profile"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("plants/add/", PlantCreateView.as_view(), name="plants_add"),
    path("plants/<int:number>", PlantDetailView.as_view(), name="plant"),
    path("plants/<int:number>/update", PlantUpdateView.as_view(), name="plant_update"),
    path("plants/<int:number>/delete", PlantDeleteView.as_view(), name="plants_delete"),
    path("ajax_response/", ajax_response, name="ajax_response"),
]
