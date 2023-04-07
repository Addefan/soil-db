from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import FormView, RedirectView, TemplateView

from web.forms import XlsxColumnsForm
from web.tasks import export_to_excel


class PlantsListView(TemplateView, FormView):
    template_name = "web/plants.html"
    form_class = XlsxColumnsForm


class XlsxColumnsView(RedirectView):
    """use RedirectView to define only 'get' request method
    - remaining methods except 'post' have the same response"""

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        form = XlsxColumnsForm(request.POST)
        if form.is_valid():
            data = dict(request.POST)
            export_to_excel.delay(
                receiver=request.user.email,
                columns=data.get("columns"),
                user_id=request.user.id,
            )
        return redirect("plants")
