from django.contrib.auth import login
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from web.forms import ProfileForm
from web.models import Staff


class ProfileFormView(UpdateView):
    template_name = "web/profile.html"
    form_class = ProfileForm
    model = Staff
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.request.user)
        # Checking if the request wasn't sent via jQuery's Ajax
        if not self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return response
        return JsonResponse({"success": True})
