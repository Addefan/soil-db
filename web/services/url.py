def build_origin_from_request(request):
    protocol = "https" if request.is_secure() else "http"
    return f"{protocol}://{request.get_host()}"
