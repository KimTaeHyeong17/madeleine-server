from django.utils.deprecation import MiddlewareMixin


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

class DisableCSRFOnDebug(object):
    def process_request(self, request):
        if settings.DEBUG:
            setattr(request, '_dont_enforce_csrf_checks', True)