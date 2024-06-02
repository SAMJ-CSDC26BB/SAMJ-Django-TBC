from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views
from .views import GitHubLogin

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("home", views.HomeView.as_view(), name="home"),
    path("login", views.login, name="login"),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path("user", views.UserManagementView.as_view(), name="user"),
    path("settings", views.GlobalSettingsView.as_view(), name="settings"),
    path('user-management/', views.UserManagementView.as_view(), name='user_management'),
    path('github/', GitHubLogin.as_view(), name='github_login'),
    path('social-auth/', include('social_django.urls', namespace='social')),

]
