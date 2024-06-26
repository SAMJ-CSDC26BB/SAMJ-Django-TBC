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
from .models import User, GlobalSettings, DestinationNumber, CallForwarding, CalledNumber
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from .serializer import ExampleSerializer

from django.shortcuts import render
from django.contrib.auth.models import User



from .businessLogic import getDestination
import logging
from django.http import HttpResponse


class HomeView(TemplateView):
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

class TbcView(TemplateView):
    template_name = "tbc.html"

@method_decorator(csrf_exempt, name='dispatch')
class CallForwardingManagementAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logger = logging.getLogger("samj")
        query = CallForwarding.objects.all().values(
            'calledNumber__number',
            'destination__number',
            'startDate',
            'endDate'
        )
        call_forwarding_list = []
        for item in query:
            call_forwarding_list.append(item)
        call_forwarding_list_wrapped = {'call_forwardings': call_forwarding_list}

        return JsonResponse(call_forwarding_list_wrapped)

    def post(self, request, *args, **kwargs):
        try:
            logger = logging.getLogger('samj')
            logger.info("XXXXXX")
            logger.info("put triggered")
            data = json.loads(request.body)
            logger.info(data)
            called_number = data.get('called_number')
            destination_number = data.get('destination_number')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            called_number_instance = CalledNumber.objects.get(number=called_number)
            destination_instance = DestinationNumber.objects.get(number=destination_number)

            call_forwarding = CallForwarding.objects.create(
                calledNumber=called_number_instance,
                destination=destination_instance,
                startDate=start_date,
                endDate=end_date,
            )

            return JsonResponse({'message': 'Call Forwarding created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except CalledNumber.DoesNotExist:
            return JsonResponse({'error': f'Called Number with number {called_number} does not exist'}, status=404)
        except DestinationNumber.DoesNotExist:
            return JsonResponse({'error': f'Destination Number with number {destination_number} does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


    def put(self, request, *args, **kwargs):
        logger = logging.getLogger("samj")

        try:
            data = json.loads(request.body)
            logger.info(data)
            called_number = data.get('called_number')
            destination_number = data.get('destination_number')
            if not called_number or not destination_number:
                return JsonResponse({'error': 'Called number and destination number are required for updating a call forwarding entry'}, status=400)
            try:
                call_forwarding = CallForwarding.objects.get(
                    calledNumber=CalledNumber.objects.get(number=called_number),
                    destination=DestinationNumber.objects.get(number=destination_number)
                )
                logger.info(call_forwarding)
            except Exception as e:
                return JsonResponse({'error': 'Call Forwarding entry not found'}, status=404)

            call_forwarding.startDate = data.get('start_date', call_forwarding.startDate)
            call_forwarding.endDate = data.get('end_date', call_forwarding.endDate)
            call_forwarding.save()
            return JsonResponse({'message': 'Call Forwarding updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        logger = logging.getLogger("samj")
        logger.info("delete request triggered")

        try:
            data = json.loads(request.body)
            call_forwarding_id = data.get('id')
            if not call_forwarding_id:
                return JsonResponse({'error': 'ID is required for deleting a call forwarding entry'}, status=400)
            try:
                call_forwarding = CallForwarding.objects.get(id=call_forwarding_id)
            except CallForwarding.DoesNotExist:
                return JsonResponse({'error': 'Call Forwarding entry not found'}, status=404)

            call_forwarding.delete()
            return JsonResponse({'message': 'Call Forwarding deleted successfully'}, status=204)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def edit_create_tbc_entry(request):
        logger = logging.getLogger('samj')
        logger.info("XXXXXXXXX")

        called_numbers = CalledNumber.objects.all()
        destinations = DestinationNumber.objects.all()

        context = {
        'calledNumbers': called_numbers,
        'destinations': destinations,
        }

        logger.info("XXXXXXXXX")
        logger.info(context)
        return render(request, 'edit_create_TbcEntry.html', context)

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









class DestinationManagementView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'destination_management.html')

@method_decorator(csrf_exempt, name='dispatch')
class DestinationManagementAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logger = logging.getLogger("samj")
        query = DestinationNumber.objects.all().values('number', 'name')
        destinationList = []
        for item in query:
            destinationList.append(item)
        destinations_list_wrapped = {'destinations': destinationList}
        logger.info(destinations_list_wrapped)
        
        return JsonResponse(destinations_list_wrapped) 

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            destination = DestinationNumber(
                name=data.get('name'),
                number=data.get('number'),
            )
            destination.save()
            return JsonResponse({'message': 'Destination created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            destination_number = data.get('number')
            destination_name = data.get('name')
            if not destination_number:

                return JsonResponse({'error': 'Number is required for updating a destination'}, status=400)
            try:
                destination = DestinationNumber.objects.get(number=destination_number)
            except Exception as e:
                return JsonResponse({'error': 'Destination not found'}, status=404)

            destination.name = data.get('name', destination.name)
            destination.number = data.get('number', destination.number)
            destination.save()
            return JsonResponse({'message': 'Destination updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        logger = logging.getLogger("samj")
        logger.info("delete request triggered")

        try:
            user = request.user
            data = json.loads(request.body)
            destination_id = data.get('id')
            if not destination_id:
                return JsonResponse({'error': 'ID is required for deleting a destination'}, status=400)
            try:
                destination = DestinationNumber.objects.get(id=destination_id, user=user)
            except DestinationNumber.DoesNotExist:
                return JsonResponse({'error': 'Destination not found'}, status=404)

            destination.delete()
            return JsonResponse({'message': 'Destination deleted successfully'}, status=204)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

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

# views.py
from django.http import JsonResponse

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