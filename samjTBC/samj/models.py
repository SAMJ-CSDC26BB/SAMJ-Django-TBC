import pytz
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


class CallForwardingRecords(models.Model):
    calledNumber = models.CharField(max_length=50, validators=[MinLengthValidator(1)], null=False, blank=False)
    username = models.CharField(max_length=50, validators=[MinLengthValidator(1)], null=False, blank=False)
    destination = models.ForeignKey("DestinationRecords", on_delete=models.CASCADE, to_field='destination')
    startDate = models.DateField(null=False, blank=False)
    endDate = models.DateField(null=False, blank=False)


class DestinationRecords(models.Model):
    destination = models.CharField(max_length=50, validators=[MinLengthValidator(1)], null=False, blank=False,
                                   primary_key=True)
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)], null=False, blank=False)


class User(models.Model):
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
    fullname = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False, null=False)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(1)], blank=False, null=False)
    number = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')
    global_settings = models.OneToOneField(GlobalSettings, on_delete=models.CASCADE)
