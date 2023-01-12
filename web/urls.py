from django.urls import path

from web.views import PlantDetailView, PlantCreateFormView, ajax_response, SoilLoginView, main, PlantDeleteView

urlpatterns = [
    path("", main, name="main"),  # TODO: сейчас заглушка
    path("profile/", ProfileFormView.as_view(), name="profile"),
    path("login/", SoilLoginView.as_view(), name="login"),
    path("plants/", main, name="plants"),  # TODO: сейчас заглушка
    path("plants/add/", PlantCreateFormView.as_view(), name="plants_add"),
    path("plants/<int:number>", PlantDetailView.as_view(), name="plant"),
    path("plants/<int:number>/delete", PlantDeleteView.as_view(), name="plants_delete"),
    path("ajax_response/", ajax_response, name="ajax_response"),
]
