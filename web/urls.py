from django.contrib import admin
from django.urls import path

from web.view.auth import SoilLoginView

urlpatterns = [
    path('login/', SoilLoginView.as_view(), name='login')
]
