from django.urls import path, include
from . import views
from .views import GitHubLogin, GoogleLogin
from .viewClasses.api_v2_tbc import api_v2_tbc
from .viewClasses.usermanagement_api import UserManagementAPIView
from .viewClasses.usermanagement import UserManagementView
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
    path("home", views.HomeView.as_view(), name="home"),

    # Settings
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),
    path('user-management/', UserManagementView.as_view(), name='user_management'),

    # Login, Session
    path("login/", views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("user", UserManagementView.as_view(), name="user"),
    path("tbc/", views.TbcView.as_view(), name="tbc"),
    path('api/destination_management/', views.DestinationManagementAPIView.as_view(), name='destination_management_api'),
    path('destination_management/', views.DestinationManagementView.as_view(), name='destination_management'),
    path('github/', GitHubLogin.as_view(), name='github_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    path('signup/', views.SignupView.as_view(), name='signup'),
    # API
    path('api/v2/tbc/', api_v2_tbc.as_view(), name='api_v2_tbc'),
    path('api/user_management/', UserManagementAPIView.as_view(), name='user_management_api'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
