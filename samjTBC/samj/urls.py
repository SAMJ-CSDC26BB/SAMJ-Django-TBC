from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("login", views.login, name="login"),
    path("settings", views.GlobalSettingsView.as_view(), name="settings")
]
