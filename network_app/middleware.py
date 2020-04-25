from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin


class SetLastRequestMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user and request.user.is_authenticated:
            request.user.last_request = now()
            request.user.save()
        return response
