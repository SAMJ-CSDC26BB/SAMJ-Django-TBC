import pytz
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
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
    setting_name = models.CharField(max_length=100, default='Global Settings')


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


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        global_settings = GlobalSettings.objects.create()
        global_settings.save()  # Save the GlobalSettings object to the database
        user.global_settings = global_settings
        user.save(using=self._db)  # Save the user object after assigning the global_settings
        return user


class User(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(Group, related_name="%(app_label)s_%(class)s_related")
    user_permissions = models.ManyToManyField(Permission, related_name="%(app_label)s_%(class)s_related")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    # USERNAME_FIELD = 'username'
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deleted', 'Deleted'),
    ]
    objects = CustomUserManager()

    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(primary_key=True, max_length=50, unique=True)
    email = models.EmailField(max_length=50, validators=[MinLengthValidator(1)], blank=False, null=False, unique=True)
    fullname = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False, null=False)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(1)], blank=False, null=False)
    number = models.CharField(max_length=50, validators=[MinLengthValidator(1)], blank=False, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')
    global_settings = models.ForeignKey(GlobalSettings, on_delete=models.CASCADE, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # This is a new object, so it doesn't have a primary key yet
            self.global_settings = GlobalSettings.objects.create()
        super().save(*args, **kwargs)
