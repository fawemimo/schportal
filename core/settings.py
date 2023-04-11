import os
from datetime import timedelta
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-1g!$eks#0s%3^guzn#w_h6v-a!x-c+3y02js5s)9cwsezx@*bj"

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cleanup.apps.CleanupConfig",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "api",
    "mainsite",
    "djoser",
    "tinymce",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    INTERNAL_IPS = ["127.0.0.1"]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

ROOT_URLCONF = "core.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "schportaldb",
        "USER": config("DBUSER"),
        "PASSWORD": config("DBPWD"),
        "HOST": "localhost",
        "PORT": 5432,
    }
}


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:99927",
]


STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "core/static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static")


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "api.User"

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}

DJOSER = {
    # "USER_CREATE_PASSWORD_RETYPE": True,
    "SERIALIZERS": {
        "user_create": "api.serializers.UserCreateSerializer",
        "current_user": "api.serializers.UserSerializer",
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "class": "logging.FileHandler",
            "filename": "mainroot.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
        }
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} ({levelname}) - {name} - {message}",
            "style": "{",
        }
    },
}
# email configurations
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_SSL = True

# TinyMce Config
TINYMCE_SPELLCHECKER = True


# SQUAD CONFIG
if DEBUG:
    SQUAD_SECRET_KEY = config("SQUAD_SECRET_KEY")
else:
    SQUAD_SECRET_KEY = config("SQUAD_SECRET_KEY_PROD")


try:
    from .prod_settings import *
    from .staging_settings import *
    from .test_settings import *
except ImportError:
    pass
