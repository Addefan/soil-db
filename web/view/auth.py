from django.contrib.auth.views import LoginView
from django.shortcuts import render

from web.forms import AuthForm


class SoilLoginView(LoginView):
    form_class = AuthForm
    success_url = ''    # TODO: success_url = main page
    template_name = "web/auth.html"
