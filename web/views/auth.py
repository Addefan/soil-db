from django.contrib import messages
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse

from web.forms import AuthForm


def main(request):
    return HttpResponse(f"{request.user.is_authenticated}")


class LoginView(SuccessMessageMixin, DjangoLoginView):
    form_class = AuthForm
    template_name = "web/auth.html"

    def get_success_message(self, cleaned_data):
        return "Вход выполнен успешно!"

    def form_valid(self, form):
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get("next") or reverse("plants")


class LogoutView(DjangoLogoutView):
    def get_next_page(self):
        return reverse("login")
