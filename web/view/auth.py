from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from web.forms import AuthForm


def main(request):
    return HttpResponse({'ok?': "ok"})


class SoilLoginView(LoginView):
    form_class = AuthForm
    template_name = "web/auth.html"

    def get_success_url(self):
        return reverse("main")
