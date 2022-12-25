from django.urls import path

from web.views import ProfileFormView

urlpatterns = [
    path("profile/", ProfileFormView.as_view(), name="profile"),
]
