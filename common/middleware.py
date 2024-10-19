import pytz
from django.utils import timezone
from django.conf import settings

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone_cookie = request.COOKIES.get('timezone')

        if timezone_cookie and timezone_cookie in pytz.all_timezones:
            timezone.activate(pytz.timezone(timezone_cookie))
        else:
            timezone.activate(pytz.timezone(settings.TIME_ZONE))

        response = self.get_response(request)

        if timezone_cookie and timezone_cookie not in pytz.all_timezones:
            response.delete_cookie('timezone')

        timezone.deactivate()
        return response
