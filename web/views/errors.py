from django.shortcuts import render
from django.views.generic import TemplateView

from http import HTTPStatus


class ErrorPageView(TemplateView):
    # override these attributes
    template_name = None
    status_code = None
    title = None
    text = None
    image = None

    def get(self, *args, **kwargs):
        response = render(
            self.request,
            self.template_name,
            {"status_code": self.status_code.value, "title": self.title, "text": self.text, "image": self.image},
            status=self.status_code,
        )
        return response


class Page404View(ErrorPageView):
    template_name = "web/404.html"
    status_code = HTTPStatus.NOT_FOUND
    title = "Страница не найдена"
    text = "Возможно, вы неверно указали её адрес или она была перемещена."
    image = "error404.png"


class Page500View(ErrorPageView):
    template_name = "web/500.html"
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    title = "Внутренняя ошибка сервера"
    text = "На сервере произошла непредвиденная ошибка." "<br>" "Пожалуйста, подождите: вскоре она будет исправлена."
    image = "error500.png"
