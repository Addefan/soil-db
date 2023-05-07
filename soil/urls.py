from celery_yandex_serverless.django import worker_view_factory
from django.conf import urls
from django.contrib import admin
from django.urls import path, include

from soil.celery import app
from web.views import Page404View, Page500View

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),
    path("api/", include("api.urls")),
    path("worker/<str:key>/", worker_view_factory(app)),
]

# requires DEBUG = False
urls.handler404 = Page404View.as_view()
urls.handler500 = Page500View.as_view()
