from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from web.models import Plant

# TODO перетащить в crud
class PlantDeleteView(SuccessMessageMixin, DeleteView):
    model = Plant
    slug_field = "number"
    slug_url_kwarg = "number"
    success_url = reverse_lazy("plants")

    def get_success_message(self, cleaned_data):
        return f"Растение <strong>{self.object.name}</strong> успешно удалено"

    def get(self, request, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        if self.request.user.organization != self.object.organization:
            return redirect("plants")
        return super().form_valid(form)
