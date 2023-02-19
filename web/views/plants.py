from django.db.models import Q
from django.views.generic import ListView

from web.models import Plant


class PlantsListView(ListView):
    template_name = "web/plants.html"
    model = Plant
    context_object_name = "plants"

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            return Plant.objects.filter(Q(name__icontains=search) | Q(latin_name__icontains=search))
        return super().get_queryset()
