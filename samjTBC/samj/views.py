import json
import logging
import re

from allauth.account.forms import UserForm
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
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

from samj.github_api.github_api import GitHubAPI
from .forms import GitHubIssueForm
from .forms import GlobalSettingsForm
from .models import User, GlobalSettings

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
        form = UserCreationForm()
        return render(request, 'authentication/signup/signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        logger.info('SignupView POST request')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f'User {form.username} signed up successfully')
            messages.success(request, 'Signup successful. You can now authentication.')
            return redirect('login')
        else:
            logger.warning(f'Signup of User {form.username} was not successful')
            messages.error(request, 'Signup was not successful. Please try again.')
            return render(request, 'authentication/signup/signup.html', {'form': form})


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
    callback_url = "home"
    client_class = OAuth2Client


# GitHub Issue Form
class CreateIssueView(FormView):
    template_name = './support/create_support.html'
    form_class = GitHubIssueForm
    success_url = '/support/tickets'  # update this to your desired URL

    def format_line(self, name, data):
        return f"- {name}: {data}" if data else ""

    def create_issue_body(self, form):
        url = form.cleaned_data['url']
        short_description = form.cleaned_data['short_description']
        detailed_description = form.cleaned_data['detailed_description']
        steps_to_reproduce = form.cleaned_data['steps_to_reproduce']
        expected_results = form.cleaned_data['expected_results']
        actual_results = form.cleaned_data['actual_results']
        name_line = self.format_line("Name", form.cleaned_data['name'])
        email_line = self.format_line("E-Mail", form.cleaned_data['email'])
        telephone_line = self.format_line("Telephone", form.cleaned_data['telephone'])

        body = f"""```yaml
        {name_line}
        {email_line}
        {telephone_line}
        - URL: {url}
        - Short Description: {short_description}
        - Detailed Description: {detailed_description}
        - Steps to Reproduce: {steps_to_reproduce}
        - Expected Results: {expected_results}
        - Actual Results: {actual_results}
        ```"""

        return body

    def form_valid(self, form):
        title = form.cleaned_data['title']
        body = self.create_issue_body(form)

        github_api = GitHubAPI()
        github_api.create_github_issue(title, body=body, labels='bug')

        return super().form_valid(form)


class SupportTicketView(TemplateView):
    template_name = './support/support_ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        github_api = GitHubAPI()
        issues = github_api.list_github_issues()
        context['issues'] = issues
        return context
