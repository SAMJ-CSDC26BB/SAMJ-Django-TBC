# pipeline.py

import logging

from django.contrib.auth import get_user_model
from social_core.exceptions import AuthAlreadyAssociated
from social_core.pipeline.partial import partial

from samj.models import GlobalSettings

logger = logging.getLogger(__name__)

User = get_user_model()


def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            raise AuthAlreadyAssociated(
                backend, 'This {0} account is already in use.'.format(provider)
            )
        elif not user:
            user = social.user
    return {'social': social, 'user': user, 'is_new': user is None}


@partial
def create_user(backend, details, response, user=None, *args, **kwargs):
    print(details)  # Add this line to inspect the details
    if user:
        return {'is_new': False}

    email = details.get('email')
    if email:
        # Check if a user with this email already exists
        user = backend.strategy.storage.user.get_user(email=email)
        if user:
            return {'is_new': False, 'user': user}

    return {
        'is_new': True,
        'user': backend.strategy.create_user(
            email=email,
            username=details.get('username'),
            first_name=details.get('first_name'),
            last_name=details.get('last_name'),
            # Include any additional fields here if needed
        )
    }


def set_global_settings(backend, user, *args, **kwargs):
    if user.global_settings_id is None:
        global_settings = GlobalSettings.objects.create()
        user.global_settings = global_settings
        user.save()
    logger.info(f"User {user.id} - Global settings ID: {user.global_settings_id}")
    return {'user': user}


def associate_by_email(backend, details, user=None, *args, **kwargs):
    """Return user entry with same email address as one returned on details."""
    if user:
        return None

    email = details.get('email')
    if not email:
        return None

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None

    return {'user': user}
