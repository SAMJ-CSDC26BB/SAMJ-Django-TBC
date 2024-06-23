"""
Django settings for samjTBC project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from .logger import CustomFormatter

from pathlib import Path

# Log and Signup URL
LOGIN_URL = 'login'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$zjcwp(2#5js7o=9-@e(b@boja)qb=-7(csf9_541_(egi%u(6"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = [
    "samj",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.apple",
    "social_django"
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'rest_framework_swagger',
    'drf_yasg',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "samjTBC.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "samj/templates"],
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
            ],
        },
    },
]

WSGI_APPLICATION = "samjTBC.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-UK"

TIME_ZONE = "CET"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.apple.AppleIdAuth',
]
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
SITE_ID = 1
# Social  Auth

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'
SOCIAL_AUTH_GITHUB_KEY = 'Ov23ligv0jGdSHhI6DTK'
SOCIAL_AUTH_GOOGLE_KEY = '382133458640-bpt47r6gap2hklct3kfu1gv9u86mume5.apps.googleusercontent.com'

SOCIAL_AUTH_APPLE_ID_REDIRECT_URI = 'https://localhost:8000/social-auth/complete/apple-id'
SOCIAL_AUTH_APPLE_ID_SCOPE = ['email', 'name']
SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME = True  # If you want to use email as username

SOCIAL_AUTH_APPLE_ID_CLIENT = 'at.drozd.SAMJ-TBC'  # Your client_id com.application.your, aka "Service ID"
SOCIAL_AUTH_APPLE_ID_TEAM = 'X2TCD4883M'  # Your Team ID, ie K2232113
SOCIAL_AUTH_APPLE_ID_KEY = 'CG8UPH6YSM'  # Your Key ID, ie Y2P99J3N81K
# do not push these
SOCIAL_AUTH_GITHUB_SECRET = 'e09300b6e16df574923d862cb128ec011763fff9'
SOCIAL_AUTH_GOOGLE_SECRET = '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'
SOCIAL_AUTH_APPLE_ID_SECRET = """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQguTQtZNhfqSA2QMbO
DIE5oGHGjCEh+AWfHCiitP+FbQWgCgYIKoZIzj0DAQehRANCAATTXBErtKRlr68u
Pwa7PB58neorvr5Nz03+O34aq9Vs8vvfo3jhZxPAj9Ak9Kv1cJbO+GRMQ0AW82Zw
ZzQ7gm+D
-----END PRIVATE KEY-----"""

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "APP": {
            "client_id": "YOUR_GITHUB_CLIENT_ID",
            "secret": "YOUR_GITHUB_SECRET_KEY",
            "key": "",
            "redirect_uri": "http://localhost:8000/accounts/github/login/callback/",
        }
    }
}

# Logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s][%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "colored": {
            "()": CustomFormatter,
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        "django_all": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./logs/django_all.log",
            "formatter": "standard",
        },
        "django_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "./logs/django_info.log",
            "formatter": "standard",
        },
        "django_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "./logs/django_error.log",
            "formatter": "standard",
        },
        "samj_all": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./logs/samj_all.log",
            "formatter": "standard",
        },
        "samj_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "./logs/samj_info.log",
            "formatter": "standard",
        },
        "samj_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "./logs/samj_error.log",
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "django_info", "django_error"],
            "level": "DEBUG",
            "propagate": True,
        },
        "samj": {
            "handlers": ["console", "samj_info", "samj_error", "samj_all"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''