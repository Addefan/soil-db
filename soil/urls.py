from django.contrib import admin
from django.urls import path, include

from web.views.errors import Page404View, Page500View

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),
    # TODO use custom 404 and 500 pages when DEBUG = False
    path("error404/", Page404View.as_view(), name="page404"),
    path("error500/", Page500View.as_view(), name="page500"),
]
