from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, FormView, RedirectView

from web.forms import XlsxColumnsForm
from web.models import Plant
from web.tasks import prepare_data


class PlantsListView(ListView, FormView):
    template_name = "web/plants.html"
    model = Plant
    context_object_name = "plants"
    form_class = XlsxColumnsForm


class PlantColumnsView(RedirectView):
    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        form = XlsxColumnsForm(request.POST)
        if form.is_valid():
            # TODO handle POST request
            data = dict(request.POST)
            prepare_data(data.get("columns"))
        return
