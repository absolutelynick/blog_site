"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from django.core.management.utils import get_random_secret_key


SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())

DEBUG = os.environ.get("DJANGO_DEBUG", "true") == "true"

if DEBUG:
    from api.environment_variables import set_environment_variables

    set_environment_variables()

BASE_DIR = os.path.abspath(os.path.join(__file__, "../.."))

ALLOWED_HOSTS = (
    ["0.0.0.0", "127.0.0.1", "localhost", "dev.blogsite.com"] if DEBUG else ["*"]
)

# Sentry Errors

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_ERROR_KEY", None),
    integrations=[DjangoIntegration()],
    environment="staging" if DEBUG else "production",
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.sites",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "rest_framework.authtoken",
    "social_django",
    "rest_framework",
    "bootstrap4",
    "core",
    "blog",
    "users",
    "api",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_otp.middleware.OTPMiddleware",
]

OTP_TOTP_ISSUER = "Google"

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {
        "NAME": "api.validators.password_validator.NumberValidator",
        "OPTIONS": {"min_digits": 2},
    },
    {
        "NAME": "api.validators.password_validator.UppercaseValidator",
        "OPTIONS": {"min_digits": 1},
    },
    {
        "NAME": "api.validators.password_validator.LowercaseValidator",
        "OPTIONS": {"min_digits": 2},
    },
    {
        "NAME": "api.validators.password_validator.SymbolValidator",
        "OPTIONS": {"min_digits": 2},
    },
]

# Authenticating users from outside apps and services

AUTHENTICATION_BACKENDS = [
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.twitter.TwitterOAuth",
    "social_core.backends.google.GoogleOAuth2",
    # Default django login
    "django.contrib.auth.backends.ModelBackend",
]

# https://apps.twitter.com/app/new
SOCIAL_AUTH_TWITTER_KEY = os.environ.get("SOCIAL_AUTH_TWITTER_KEY", None)
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get("SOCIAL_AUTH_TWITTER_SECRET", None)

# https://developers.facebook.com/
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY", None)
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET", None)

# https://console.developers.google.com/apis/credentials
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", None)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get(
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", None
)


SOCIAL_AUTH_USER_FIELDS = ["email", "username"]
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

LOGIN_REDIRECT_URL = "home"

AUTH_USER_MODEL = "users.User"

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Email setup

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-repl@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", None)
EMAIL_PORT = 587
EMAIL_USE_TLS = True

