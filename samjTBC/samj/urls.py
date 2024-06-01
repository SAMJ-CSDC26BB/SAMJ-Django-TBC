from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("home", views.HomeView.as_view(), name="home"),
    path("login", views.login, name="login"),
    path("settings", views.GlobalSettingsView.as_view(), name="settings")
]
