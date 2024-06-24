import pytz
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Permission, Group
from django.core.validators import MinLengthValidator

# Create your models here.
from django.db import models


class GlobalSettings(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    LANGUAGES = [
        ('en', 'English'),
        ('de', 'German'),
        # Add more languages here
    ]
    THEMES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    NOTIFICATIONS = [
        ('on', 'On'),
        ('off', 'Off'),
    ]

    timezone = models.CharField(max_length=50, choices=TIMEZONES, default='UTC')
    language = models.CharField(max_length=2, choices=LANGUAGES, default='en')
    theme = models.CharField(max_length=5, choices=THEMES, default='light')
    notifications = models.CharField(max_length=3, choices=NOTIFICATIONS, default='on')


class CallForwarding(models.Model):
    id = models.AutoField(primary_key=True)
    calledNumber = models.ForeignKey("CalledNumber", on_delete=models.CASCADE, to_field='number')
    destination = models.ForeignKey("DestinationNumber", on_delete=models.CASCADE, to_field='number')
    startDate = models.DateField(null=False, blank=False)
    endDate = models.DateField(null=False, blank=False)


class CalledNumber(models.Model):
    number = models.CharField(max_length=50, validators=[MinLengthValidator(1)], null=False, blank=False,
                              primary_key=True)
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)], null=False, blank=False)


class DestinationNumber(models.Model):
    number = models.CharField(max_length=50, validators=[MinLengthValidator(1)], null=False, blank=False,
                              primary_key=True)
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)], null=False, blank=False)


class User(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(Group, related_name="%(app_label)s_%(class)s_related")
    user_permissions = models.ManyToManyField(Permission, related_name="%(app_label)s_%(class)s_related")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']
    # USERNAME_FIELD = 'username'
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deleted', 'Deleted'),
    ]

    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(primary_key=True, max_length=50)
    email = models.EmailField(max_length=50, validators=[MinLengthValidator(1)], blank=False, null=False)
    fullname = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False, null=False)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(1)], blank=False, null=False)
    number = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')
    global_settings = models.OneToOneField(GlobalSettings, on_delete=models.CASCADE)
