from django.contrib import admin
from django.urls import path

from web.view import SoilLoginView, main

urlpatterns = [path("login/", SoilLoginView.as_view(), name="login"), path("", main, name="main")]
