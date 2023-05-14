from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import FormView, RedirectView, TemplateView

from api.serializers import PlantSerializer
from web.forms import XlsxColumnsForm
from web.models import Plant
from web.services.url import build_origin_from_request
from web.tasks import export_to_excel


class PlantsListView(TemplateView, FormView):
    template_name = "web/plants.html"
    form_class = XlsxColumnsForm

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(), "search": self.request.GET.get("search", None)}


class XlsxColumnsView(RedirectView):
    """use RedirectView to define only 'get' request method
    - remaining methods except 'post' have the same response"""

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        form = XlsxColumnsForm(request.POST)
        if form.is_valid():
            origin = build_origin_from_request(request)
            export_to_excel.delay(
                origin=origin,
                user_id=request.user.id,
                columns=form.cleaned_data.get("columns"),
            )
        return redirect("plants")
