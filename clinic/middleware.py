from django.utils.cache import add_never_cache_headers


class NoStoreAuthenticatedMiddleware:
    """Prevents browser history from reusing authenticated clinic pages after logout."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, "user", None)
        protected_prefixes = (
            "/dashboard/",
            "/book-appointment/",
            "/set-appointment/",
            "/my-sessions/",
            "/profile/",
            "/doctor/",
            "/secretary/",
            "/schedule-appointment/",
            "/patients/",
            "/patient/",
        )
        if getattr(user, "is_authenticated", False) or request.path.startswith(protected_prefixes):
            add_never_cache_headers(response)
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
        return response
