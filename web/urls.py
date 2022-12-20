from django.contrib import admin
from django.urls import path

from web.view.add_plant import PlantCreateFormView, view_test

urlpatterns = [
    path("plants/add/", PlantCreateFormView.as_view(), name='plants_add'),
    path("", view_test, name='view_test')
]
