import json
import re

from allauth.account.forms import UserForm
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView

from .forms import GlobalSettingsForm
from .models import User, GlobalSettings


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, "./login/login.html")

    def post(self, request, *args, **kwargs):
        username_or_email = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, "./login/login.html")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('login')


class SignupView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'login/signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'login/signup.html', {'form': form})


def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[\W_]", password):
        return False, "Password must contain at least one special character."
    return True, ""


@method_decorator(csrf_exempt, name='dispatch')
class UserManagementAPIView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all().values('username', 'fullname', 'status', 'role', 'number')
        user_list = list(users)
        status_options = [choice for choice in User.STATUS_CHOICES if choice[0] != 'deleted']
        role_options = User.ROLE_CHOICES
        data = {
            'users': user_list,
            'status_options': status_options,
            'role_options': role_options,
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            password = data.get('password')

            # Validate password if provided
            if password:
                is_valid, message = validate_password(password)
                if not is_valid:
                    return JsonResponse({'error': message}, status=400)

            # Create default global settings for the new user
            global_settings = GlobalSettings.objects.create()

            user = User(
                username=data.get('username'),
                fullname=data.get('fullname'),
                password=password,
                number=data.get('number'),
                status=data.get('status', 'active'),
                role=data.get('role', 'user'),
                global_settings=global_settings
            )
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            if not username:
                return JsonResponse({'error': 'Username is required for updating a user'}, status=400)
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            password = data.get('password')

            # Validate password if provided
            if password:
                is_valid, message = validate_password(password)
                if not is_valid:
                    return JsonResponse({'error': message}, status=400)

            user.fullname = data.get('fullname', user.fullname)
            if password:
                user.password = password
            user.number = data.get('number', user.number)
            user.status = data.get('status', user.status)
            user.role = data.get('role', user.role)
            user.save()
            return JsonResponse({'message': 'User updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            if not username:
                return JsonResponse({'error': 'Username is required for deleting a user'}, status=400)
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=204)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class UserManagementView(LoginRequiredMixin, TemplateView):
    template_name = "user_management.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['user_form'] = UserForm()
        context['status_options'] = [choice for choice in User.STATUS_CHOICES if choice[0] != 'deleted']
        context['role_options'] = User.ROLE_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')
        context = self.get_context_data()
        context['user_form'] = form
        return self.render_to_response(context)


class GlobalSettingsView(FormView):
    form_class = GlobalSettingsForm
    template_name = 'global_settings/global_settings.html'

    def form_valid(self, form):
        form.save()
        return redirect('home')


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "127.0.0.1/login"
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "127.0.0.1/login"
    client_class = OAuth2Client


class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
    callback_url = "127.0.0.1/login"
    client_class = OAuth2Client
