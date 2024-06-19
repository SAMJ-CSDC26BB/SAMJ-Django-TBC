from django.urls import path
from .viewClasses.restEndpoint import restEndpoint
from . import views
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from uritemplate import URITemplate


urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path('restEndpoint/', restEndpoint.as_view(), name='restEndpoint'),
    path("home", views.HomeView.as_view(), name="home"),
    path("login", views.login, name="login"),
    path('api/user_management/', views.UserManagementAPIView.as_view(), name='user_management_api'),
    path("user", views.UserManagementView.as_view(), name="user"),
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),
    path('user-management/', views.UserManagementView.as_view(), name='user_management'),
    path('api_schema', get_schema_view(title='API Schema', description='Guide for the REST API'), name='api_schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger_schema.html',
        extra_context={'schema_url': 'api_schema'}  # Use extra_context here
    ), name='swagger-ui'),
    path('api/endpoint/', restEndpoint.as_view(), name='rest-endpoint'),

]
