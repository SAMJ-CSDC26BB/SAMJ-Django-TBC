from allauth.account.forms import UserForm
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView
from django.shortcuts import render, redirect

from .auth.appleOAuth2 import AppleOAuth2
from .forms import GlobalSettingsForm
from .models import User


def login(request):
    code = request.GET.get('code')
    if code is not None:
        # This is a redirect from Apple with an authorization code
        apple_auth = AppleOAuth2()
        user = apple_auth.do_auth(code)

        if user is not None:
            # Log in the user and redirect to home page
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            # Authentication failed, redirect to login page
            return HttpResponseRedirect('/login')
    else:
        # This is a normal GET request, render the login page
        return render(request, "./login/login.html")


class HomeView(TemplateView):
    template_name = "home.html"


class UserManagementView(TemplateView):
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


class tbcView(TemplateView):
    template_name = "tbc.html"

