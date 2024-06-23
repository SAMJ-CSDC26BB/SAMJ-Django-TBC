from django.urls import path
from .viewClasses.restEndpoint import restEndpoint
from . import views
from django.views.generic import TemplateView
from .swagger_config import urlpatterns as swagger_urls, schema_view
from django.urls import path, include

from .views import ExampleAPIView  # Replace with your actual app name

from django.urls import path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SAMJ API",
        default_version='v1',
        description="Samjservices:\nTBC: Retrieve Destination Numver based on time",
    ),
    public=True,
)

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path('restEndpoint/', restEndpoint.as_view(), name='restEndpoint'),
    path("home", views.HomeView.as_view(), name="home"),
    path("login", views.login, name="login"),
    path('api/user_management/', views.UserManagementAPIView.as_view(), name='user_management_api'),
    path("user", views.UserManagementView.as_view(), name="user"),
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),
    path('user-management/', views.UserManagementView.as_view(), name='user_management'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
