from django.views.generic import ListView

from web.models import Plant


class PlantsListView(ListView):
    template_name = "web/plants.html"
    model = Plant
    context_object_name = "plants"
