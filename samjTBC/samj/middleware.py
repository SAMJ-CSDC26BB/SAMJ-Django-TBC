from django.utils.deprecation import MiddlewareMixin

from .models import GlobalSettings


class EnsureGlobalSettingsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            GlobalSettings.objects.get_or_create(user=request.user)
