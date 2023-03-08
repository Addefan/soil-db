from django.shortcuts import render
from django.views.generic import TemplateView

from http import HTTPStatus


class ErrorPageView(TemplateView):
    # override these attributes
    template_name = None
    status_code = None

    def get(self, *args, **kwargs):
        response = render(
            self.request, self.template_name, {"status_code": self.status_code.value}, status=self.status_code
        )
        return response


class Page404View(ErrorPageView):
    template_name = "web/error404.html"
    status_code = HTTPStatus.NOT_FOUND


class Page500View(ErrorPageView):
    template_name = "web/error500.html"
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
