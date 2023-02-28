import json
import logging
from datetime import timedelta
from http import HTTPStatus
from uuid import uuid4

import redis
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, RedirectView

from web.forms import ProfileForm
from web.models import Staff
from web.tasks import send_password_changing_email


class ProfileFormView(LoginRequiredMixin, UpdateView):
    template_name = "web/profile.html"
    form_class = ProfileForm
    model = Staff
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user_id = self.request.user.id
        old_password = Staff.objects.get(pk=user_id).password
        new_password = form.cleaned_data.pop("password", None)
        if new_password:
            form.instance.password = old_password
            token = uuid4().hex
            data = {"user_id": user_id, "password": new_password}
            r = redis.Redis(host="localhost", port=6379, db=0)
            r.psetex(token, timedelta(hours=1), json.dumps(data))
            send_password_changing_email.delay(user_id, token)
        response = super().form_valid(form)
        # Checking if the request wasn't sent via jQuery's Ajax
        if not self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return response
        return JsonResponse({"password": bool(new_password)})

    def form_invalid(self, form):
        # Checking if the request wasn't sent via jQuery's Ajax
        if not self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return super().form_invalid(form)
        return JsonResponse(form.errors, status=HTTPStatus.NOT_FOUND)


class ChangePasswordView(RedirectView):
    url = reverse_lazy("profile")

    def get(self, request, *args, **kwargs):
        token = request.GET.get("token", None)
        if not token:
            raise Http404
        r = redis.Redis(host="localhost", port=6379, db=0)
        data = r.getdel(token)
        if not data:
            raise Http404
        data = json.loads(data)
        user = Staff.objects.get(id=data["user_id"])
        if not user == self.request.user:
            raise Http404
        user.password = data["password"]
        user.save()
        update_session_auth_hash(self.request, user)
        messages.success(request, "Вы успешно изменили пароль")
        return super().get(request, *args, **kwargs)
