from http import HTTPStatus

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, RedirectView

from web.forms import ProfileForm
from web.models import Staff
from web.services.password import create_password_change_request, process_password_change_request
from web.services.url import build_origin_from_request


class ProfileFormView(LoginRequiredMixin, UpdateView):
    template_name = "web/profile.html"
    form_class = ProfileForm
    model = Staff
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        # Checking if the request wasn't sent via jQuery's Ajax
        if not self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return response
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        # Checking if the request wasn't sent via jQuery's Ajax
        if not self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return super().form_invalid(form)
        return JsonResponse(form.errors, status=HTTPStatus.NOT_FOUND)


class ChangePasswordView(RedirectView):
    url = reverse_lazy("profile")

    def get(self, request, *args, **kwargs):
        changed = process_password_change_request(request)

        if not changed:
            raise Http404

        messages.success(request, "Вы успешно изменили пароль")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        new_password = request.POST.get("password")
        user_id = request.user.id

        try:
            validate_password(new_password)
        except ValidationError as error:
            # TODO нужны сериализаторы
            errors = {"password": error.messages}
            return JsonResponse(errors, status=HTTPStatus.NOT_FOUND)

        origin = build_origin_from_request(request)
        create_password_change_request(new_password, user_id, origin)

        return JsonResponse({"success": True})
