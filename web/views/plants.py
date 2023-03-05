from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, FormView, RedirectView

from web.forms import XlsxColumnsForm
from web.models import Plant
from web.tasks import export_to_excel


class PlantsListView(ListView, FormView):
    template_name = "web/plants.html"
    model = Plant
    context_object_name = "plants"
    form_class = XlsxColumnsForm

    def get_queryset(self):
        self.search = self.request.GET.get("search")
        if self.search:
            return Plant.objects.filter(
                Q(number__icontains=self.search) | Q(name__icontains=self.search) | Q(latin_name__icontains=self.search)
            )
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        return {**super().get_context_data(object_list=object_list, **kwargs), "search": self.search}


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
