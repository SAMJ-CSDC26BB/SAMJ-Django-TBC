from django.utils.deprecation import MiddlewareMixin

from .models import GlobalSettings


class EnsureGlobalSettingsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not hasattr(request.user, 'user_global_settings'):
                GlobalSettings.objects.create(user=request.user)
