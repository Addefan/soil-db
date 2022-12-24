from django.views.generic import DetailView

from web.models import Plant


class PlantDetailView(DetailView):
    model = Plant
    template_name = "web/plant.html"
    context_object_name = "plant"
    slug_field = "number"
    slug_url_kwarg = "number"

    def get_context_data(self, **kwargs):
        return {
            **super(PlantDetailView, self).get_context_data(**kwargs),
            "latin_name": self.latin_name,
            "name": self.name,
        }

    def get_object(self, queryset=None):
        obj = self.get_queryset()[0]
        self.latin_name = obj.latin_name
        self.name = obj.name
        return obj.to_dict()
