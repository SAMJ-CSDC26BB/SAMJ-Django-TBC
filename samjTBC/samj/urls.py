from django.urls import path
from .views import timeDateAPI
from .views import timeDateTest
from .views import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path('time_date/', timeDateAPI.TimeDateAPI.as_view()),
    path('timeDateTest/', timeDateTest.TimeDateTest.as_view()),
]