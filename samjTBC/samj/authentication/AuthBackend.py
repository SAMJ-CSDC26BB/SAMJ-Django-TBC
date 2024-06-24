import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from samj.models import GlobalSettings, User

logger = logging.getLogger(__name__)


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            logger.warning(f"Authentication failed for username/email: {username}. User does not exist.")
            return None

        if user.check_password(password):
            return user

        logger.warning(f"Authentication failed for username/email: {username}. Incorrect password.")
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            logger.warning(f"Get user failed for user_id: {user_id}. User does not exist.")
            return None


class UserManagementAPIView(APIView):
    def post(self, request, format=None):
        data = request.data
        global_settings = GlobalSettings.objects.create()  # or get existing settings

        user = User(
            username=data.get('username'),
            fullname=data.get('fullname'),
            number=data.get('number'),
            status=data.get('status', 'active'),
            role=data.get('role', 'user'),
            global_settings=global_settings
        )
        user.set_password(data.get('password'))  # Hash the password before storing it
        user.save()

        logger.info(f"User {user.username} created successfully")

        return Response({"message": "User created successfully"})
