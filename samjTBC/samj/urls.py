from django.urls import path, include

from . import views
from .viewClasses.restEndpoint import restEndpoint
from .views import GitHubLogin, GoogleLogin

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("home", views.HomeView.as_view(), name="home"),

    # Settings
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),
    path('user-management/', views.UserManagementView.as_view(), name='user_management'),

    # Login, Session
    path("authentication/", views.LoginView.as_view(), name="authentication"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("user", views.UserManagementView.as_view(), name="user"),
    path('github_api/', GitHubLogin.as_view(), name='github_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    path('signup/', views.SignupView.as_view(), name='signup'),
    # API
    path('restEndpoint/', restEndpoint.as_view(), name='restEndpoint'),
    path('api/user_management/', views.UserManagementAPIView.as_view(), name='user_management_api'),
    # Support with GitHub REST API
    path('support/', views.CreateIssueView.as_view(), name='support_via_github'),
    path('support/ticket', views.SupportTicketView.as_view(), name='support_ticket'),
]
