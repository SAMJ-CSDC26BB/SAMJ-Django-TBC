from django.http import HttpResponseRedirect
from django.shortcuts import render

from .auth.appleOAuth2 import AppleOAuth2


# Create your views here.
def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


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
