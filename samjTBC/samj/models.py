import pytz
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Permission, Group, AbstractUser
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
# Create your models here.
from django.db import models


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
    def create_user(self, email, password=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email' or 'username'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deleted', 'Deleted'),
    ]

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
    global_settings = models.OneToOneField('GlobalSettings', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='user_global_settings')
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name="%(app_label)s_%(class)s_related")
    user_permissions = models.ManyToManyField(Permission, related_name="%(app_label)s_%(class)s_related")

    def save(self, *args, **kwargs):
        if not self.pk and not self.global_settings_id:
            self.global_settings = GlobalSettings.objects.create()
        super().save(*args, **kwargs)


class GlobalSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_global_settings')
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
