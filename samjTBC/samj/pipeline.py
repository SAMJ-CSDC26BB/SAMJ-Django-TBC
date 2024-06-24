# samj/pipeline.py

import logging

from social_core.pipeline.partial import partial

from .models import GlobalSettings

logger = logging.getLogger(__name__)


def create_global_settings(strategy, details, backend, user=None, *args, **kwargs):
    if user and not user.global_settings_id:
        user.global_settings = GlobalSettings.objects.create()
        user.save()


@partial
def set_global_settings(strategy, details, user=None, *args, **kwargs):
    if user and not user.global_settings_id:
        default_settings = GlobalSettings.objects.first()
        if default_settings:
            user.global_settings = default_settings
            user.save()
            logger.info(f"Set global_settings for user {user.id}")
        else:
            logger.warning("No default global_settings found")
