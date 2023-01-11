from http import HTTPStatus

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from web.forms import ProfileForm
from web.models import Staff


class ProfileFormView(LoginRequiredMixin, UpdateView):
    template_name = "web/profile.html"
    form_class = ProfileForm
    model = Staff
    success_url = reverse_lazy("profile")
    login_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.request.user)
        # Checking if the request wasn't sent via jQuery's Ajax
        if not self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return response
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        # Checking if the request wasn't sent via jQuery's Ajax
        if not self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return super().form_invalid(form)
        return JsonResponse(form.errors, status=HTTPStatus.NOT_FOUND)
