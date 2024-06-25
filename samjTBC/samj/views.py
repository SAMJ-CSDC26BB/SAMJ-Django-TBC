import json
import logging
import re

from allauth.account.forms import UserForm
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from samj.github_api.github_api import GitHubAPI
from .forms import GitHubIssueForm, CustomUserCreationForm, UpdateUserForm
from .forms import GlobalSettingsForm
from .models import User, GlobalSettings
from .serializer import ExampleSerializer

logger = logging.getLogger(__name__)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"


class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        logger.info('LoginView GET request')
        if request.user.is_authenticated:
            logger.info('User is authenticated, redirecting to home')
            return redirect('home')
        else:
            return render(request, "./authentication/login/login.html")

    def post(self, request, *args, **kwargs):
        logger.info('LoginView POST request')
        username_or_email = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            logger.info(f'User {user} authenticated successfully')
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            logger.warning('Invalid username or password')
            messages.error(request, 'Invalid username or password.')
            return render(request, "./authentication/login/login.html")


class CustomGitHubOAuth2Adapter(GitHubOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        extra_data = super().complete_login(request, app, token, **kwargs)

        # Extract user info from extra_data
        user_info = extra_data.user
        username = user_info.get('login')
        email = user_info.get('email')
        name = user_info.get('name')

        # Create a new GlobalSettings instance and a new User instance in a transaction
        with transaction.atomic():
            global_settings = GlobalSettings.objects.create()

            user = User(
                username=username,
                fullname=name,
                email=email,
                global_settings=global_settings  # Associate the GlobalSettings instance with the user
            )
            user.save()

        return extra_data


class GitHubLogin(SocialLoginView):
    adapter_class = CustomGitHubOAuth2Adapter
    callback_url = "home"
    client_class = OAuth2Client


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logger.info('LogoutView GET request')
        auth_logout(request)
        if request.user.is_authenticated:
            logger.error('Logout failed.')
        else:
            logger.info('User logged out successfully')
            messages.error(request, 'Logout was not successful. Please try again.')
        return redirect('login')


class SignupView(TemplateView):
    def get(self, request, *args, **kwargs):
        logger.info('SignupView GET request')
        form = CustomUserCreationForm()
        return render(request, 'authentication/signup/signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        logger.info('SignupView POST request')
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Do not save the model yet
            user.fullname = f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
            user.save()  # Now save the model after setting fullname
            logger.info(f'User {form.cleaned_data["username"]} signed up successfully')
            messages.success(request, 'Signup successful. You can now login.')
            return redirect('home')
        else:
            logger.warning(f'Signup of User {form.cleaned_data["username"]} was not successful')
            messages.error(request, 'Signup was not successful. Please try again.')
            return render(request, 'authentication/signup/signup.html', {'form': form})


class AccountView(View):
    def get(self, request, *args, **kwargs):
        form = UpdateUserForm(instance=request.user)
        return render(request, 'authentication/account/account.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'authentication/account/account.html', {'form': form})


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

    def patch(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            if not username:
                return JsonResponse({'error': 'Username is required for updating a user'}, status=400)
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Fields that may be updated
            updatable_fields = ['fullname', 'password', 'number', 'status', 'role']

            password = data.get('password')
            # Validate and update password if provided
            if password:
                is_valid, message = validate_password(password)
                if not is_valid:
                    return JsonResponse({'error': message}, status=400)
                user.password = password

            # Update other fields
            for field in updatable_fields:
                if field in data:
                    setattr(user, field, data[field])

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


@method_decorator(login_required, name='dispatch')
class GlobalSettingsView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        global_settings, created = GlobalSettings.objects.get_or_create(user=request.user)
        form = GlobalSettingsForm(instance=global_settings)
        return render(request, 'global_settings/global_settings.html', {'form': form})

    def post(self, request, *args, **kwargs):
        global_settings, created = GlobalSettings.objects.get_or_create(user=request.user)
        form = GlobalSettingsForm(request.POST, instance=global_settings)
        if form.is_valid():
            form.save()
            return redirect('settings')
        return render(request, 'global_settings/global_settings.html', {'form': form})


# GitHub Issue Form
def format_line(name, data):
    return f"- {name}: {data}" if data else ""


def create_issue_body(form):
    contact_details = {
        "Name": form.cleaned_data['name'],
        "E-Mail": form.cleaned_data['email'],
        "Telephone": form.cleaned_data['telephone'],  # the telephone number which might be affected
    }

    issue_details = {
        "URL": form.cleaned_data['url'],  # where the Issue happens
        "Short Description": form.cleaned_data['short_description'],  # Brief summary of the issue in one sentence
        "Detailed Description": form.cleaned_data['detailed_description'],
        # Provide a detailed description of the issue. Include any relevant background information.
        "Steps to Reproduce": form.cleaned_data['steps_to_reproduce'],  # Steps to reproduce the issue
        "Expected Results": form.cleaned_data['expected_results'],  # What you expected to happen
        "Actual Results": form.cleaned_data['actual_results'],  # What actually happened
    }

    contact_lines = [f"- {key}: {value}" for key, value in contact_details.items() if value]
    issue_lines = [f"- {key}: {value}" for key, value in issue_details.items() if value]

    body = "Contact Details (optional):\n" + "\n".join(contact_lines) + "\n\nIssue Details:\n" + "\n".join(issue_lines)
    body = "```yaml\n" + body + "\n```"

    return body


class CreateIssueView(FormView):
    template_name = './support/create_support.html'
    form_class = GitHubIssueForm
    success_url = '/support/tickets'  # update this to your desired URL

    def form_valid(self, form):
        title = f"[SUPPORT][BUG] {form.cleaned_data['title']}"
        body = create_issue_body(form)

        github_api = GitHubAPI()
        github_api.create_github_issue(title, body=body, labels='bug')

        return super().form_valid(form)


class SupportTicketView(TemplateView):
    template_name = './support/support_ticket.html'
    logger = logging.getLogger(__name__)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        github_api = GitHubAPI()
        self.logger.info('Fetching GitHub issues')
        issues = github_api.list_github_issues(labels='bug', state='all')
        parsed_issues = []
        for issue in issues:
            parsed_issue = {
                'url': issue['html_url'],
                'title': issue['title'],
                'user': issue['user']['login'],
                'labels': [label['name'] for label in issue['labels']],
                'state': issue['state'],
                'created_at': issue['created_at'],
                'body': issue['body'],
            }
            parsed_issues.append(parsed_issue)
        context['issues'] = parsed_issues
        self.logger.info(f'Fetched {len(parsed_issues)} issues from GitHub')
        return context


class ExampleAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Summary of the endpoint",
        responses={200: ExampleSerializer()},
    )
    def get(self, request):
        data = {'field1': 'value', 'field2': 123}
        serializer = ExampleSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
