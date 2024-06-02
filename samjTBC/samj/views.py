from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView
from django.shortcuts import render, redirect

from .auth.appleOAuth2 import AppleOAuth2
from .forms import GlobalSettingsForm


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


class GlobalSettingsView(FormView):
    form_class = GlobalSettingsForm
    template_name = 'global_settings/global_settings.html'

    def form_valid(self, form):
        form.save()
        return redirect('home')
