from django.template.defaulttags import url
from django.urls import path
from .viewClasses.restEndpoint import restEndpoint
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path('restEndpoint/', restEndpoint.as_view(), name='restEndpoint'),
    path("home", views.HomeView.as_view(), name="home"),
    path("login", views.login, name="login"),
    path('api/user_management/', views.UserManagementAPIView.as_view(), name='user_management_api'),
    path("user", views.UserManagementView.as_view(), name="user"),
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),
    path('user-management/', views.UserManagementView.as_view(), name='user_management'),
    path('test/', views.SwaggerSchemaView.as_view(), name='test'),
]
