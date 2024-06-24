from django.urls import path, include

from samj.swagger.swagger_config import schema_view
from . import views
from .viewClasses.api_v2_tbc import api_v2_tbc
from .views import GitHubLogin

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("home", views.HomeView.as_view(), name="home"),

    # Settings
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),
    path("user-management/", views.UserManagementView.as_view(), name="user_management"),

    # Login, Session
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("user", views.UserManagementView.as_view(), name="user"),
    path("login/github/", GitHubLogin.as_view(), name="github_login"),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("accounts/", include("allauth.urls")),
    # API
    path("api/v2/tbc/", api_v2_tbc.as_view(), name="api_v2_tbc"),
    path("api/user_management/", views.UserManagementAPIView.as_view(), name="user_management_api"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    # Support with GitHub REST API
    path("support/", views.CreateIssueView.as_view(), name="support_via_github"),
    path("support/tickets", views.SupportTicketView.as_view(), name="support_ticket"),
]
