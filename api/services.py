from django.http import HttpRequest
from rest_framework.request import Request


def apply_filters_to_queryset(queryset, filter_backends, filters):
    request = Request(HttpRequest())
    request._request.GET = filters
    for backend in filter_backends:
        queryset = backend().filter_queryset(request, queryset, None)
    return queryset
