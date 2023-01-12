from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.http import HttpResponse
from django.urls import reverse

from web.forms import AuthForm


def main(request):
    return HttpResponse(f"{request.user.is_authenticated}")


class LoginView(DjangoLoginView):
    form_class = AuthForm
    template_name = "web/auth.html"

    def get_success_url(self):
        return reverse("plants")


class LogoutView(DjangoLogoutView):
    def get_next_page(self):
        return reverse("login")
