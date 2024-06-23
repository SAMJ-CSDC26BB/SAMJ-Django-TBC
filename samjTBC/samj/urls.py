from django.urls import path
from .viewClasses.api_v2_tbc import api_v2_tbc
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path('api/v2/tbc/', api_v2_tbc.as_view(), name='api_v2_tbc'),
    path("home", views.HomeView.as_view(), name="home"),
    path("login", views.login, name="login"),
    path("user", views.UserManagementView.as_view(), name="user"),
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),
    path('user-management/', views.UserManagementView.as_view(), name='user_management'),
]
