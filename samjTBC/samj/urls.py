from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views
from .views import GitHubLogin, GoogleLogin

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("home", views.HomeView.as_view(), name="home"),
    path("login", views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path("user", views.UserManagementView.as_view(), name="user"),
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),
    path('user-management/', views.UserManagementView.as_view(), name='user_management'),
    path('github/', GitHubLogin.as_view(), name='github_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    path('signup/', views.as_view(template_name='singup.html'), name='signup'),

]
