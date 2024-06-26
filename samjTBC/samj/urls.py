from django.urls import path, include

from samj.swagger.swagger_config import schema_view
from . import views
from .views import GitHubLogin

from .viewClasses.api_v2_tbc import api_v2_tbc
from .viewClasses.callingNumberManagement_api import callingNumberManagementAPIView
from .viewClasses.callingNumberManagement import callingNumberManagement
from .views import CallForwardingManagementAPIView

from .viewClasses.user_management import UserManagementView
from .viewClasses.user_management_api import UserManagementAPIView
from .views import GitHubLogin, AccountView

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("home", views.HomeView.as_view(), name="home"),

    # Settings
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),

    # Tables
    path("user-management/", UserManagementView.as_view(), name="user_management"),
    path('destination_management/', views.DestinationManagementView.as_view(), name='destination_management'),
    path('callingNumberManagement/', callingNumberManagement.as_view(), name='callingNumberManagement'),
    path("tbc/", views.TbcView.as_view(), name="tbc"),

    # Login, Session
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path('account/', AccountView.as_view(), name='account'),
    path("user", UserManagementView.as_view(), name="user"),
    path("login/github/", GitHubLogin.as_view(), name="github_login"),
    path("social-auth/", include("social_django.urls", namespace="social")),

    # API
    path("api/v2/tbc/", api_v2_tbc.as_view(), name="api_v2_tbc"),
    path("api/user_management/", UserManagementAPIView.as_view(), name="user_management_api"),
    path('api/destination_management/', views.DestinationManagementAPIView.as_view(), name='destination_management_api'),
    path('api/callingNumberManagement/', callingNumberManagementAPIView.as_view(), name='callingNumberManagement_api'),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('api/call_forwarding_management/', CallForwardingManagementAPIView.as_view(),
         name='call_forwarding_management'),
    path('api/edit_create_tbc_entry/', CallForwardingManagementAPIView.as_view(), name='edit_create_tbc_entry'),

    # Support with GitHub REST API
    path("support/", views.CreateIssueView.as_view(), name="support_via_github"),
    path("support/tickets", views.SupportTicketView.as_view(), name="support_ticket"),
]
