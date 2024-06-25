# pipeline.py

import logging

from django.contrib.auth import get_user_model
from social_core.exceptions import AuthAlreadyAssociated

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


def create_user(strategy, details, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = {'username': details.get('username'), 'email': details.get('email')}
    if not fields['email']:
        raise ValueError('The Email field must be set')

    user = strategy.create_user(**fields)
    user.save()  # Ensure user is saved and id is assigned
    return {'is_new': True, 'user': user}


def set_global_settings(backend, user, response, *args, **kwargs):
    if not hasattr(user, 'user_global_settings'):
        GlobalSettings.objects.create(user=user)
        logger.info(f"User {user.id} is new, created global settings")
    else:
        logger.info(f"User {user.id} already has global settings, skipping creation")


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
