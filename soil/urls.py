from django.conf import urls
from django.contrib import admin
from django.urls import path, include

from web.views import Page404View, Page500View

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),
    path("api/", include("api.urls")),
]

# requires DEBUG = False
urls.handler404 = Page404View.as_view()
urls.handler500 = Page500View.as_view()
