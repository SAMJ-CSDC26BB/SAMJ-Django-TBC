from django.urls import path
from .viewsT.restEndpoint import restEndpoint
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path('restEndpoint/', restEndpoint.as_view()),
    path("home", views.HomeView.as_view(), name="home"),
    path("login", views.login, name="login"),
    path("user", views.UserManagementView.as_view(), name="user"),
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),
    path('user-management/', views.UserManagementView.as_view(), name='user_management'),
]
