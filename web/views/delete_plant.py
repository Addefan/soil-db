from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from web.models import Plant


class PlantDeleteView(DeleteView):
    model = Plant
    slug_field = "number"
    slug_url_kwarg = "number"
    success_url = reverse_lazy("plants")

    def form_valid(self, form):
        if self.request.user.organization != self.object.organization:
            return redirect("plants")
        return super().form_valid(form)
