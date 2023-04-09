from django.urls import path
from django.views.generic import RedirectView

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
    XlsxColumnsView,
    ChangePasswordView,
)

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="plants"), name="main"),
    path("plants/", PlantsListView.as_view(), name="plants"),
    path("profile/", ProfileFormView.as_view(), name="profile"),
    path("profile/change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("plants/add/", PlantCreateView.as_view(), name="plants_add"),
    path("plants/<int:number>", PlantDetailView.as_view(), name="plant"),
    path("plants/<int:number>/update", PlantUpdateView.as_view(), name="plant_update"),
    path("plants/<int:number>/delete", PlantDeleteView.as_view(), name="plants_delete"),
    path("ajax_response/", ajax_response, name="ajax_response"),
    path("plant_columns/", XlsxColumnsView.as_view(), name="plant_columns"),
]
