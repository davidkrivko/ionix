"""
Django settings for coreapp project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Application definition

CORS_ALLOWED_ORIGINS = ['https://panel-do.ionix-staging.com']


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd-party apps
    "corsheaders",
    "django_hosts",
    "django_q",
    "ebhealthcheck.apps.EBHealthCheckConfig",
    "rest_framework",
    "phonenumber_field",
    "user_visit",
    "drf_yasg",
    "django_filters",
    # built
    "users",
    "devices",
    "api",
    "properties",
    "workers",
    "external",
    "schedules",
    "support",
    "visuals",
]

MIDDLEWARE = [
    "django_hosts.middleware.HostsRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "user_visit.middleware.UserVisitMiddleware",
    "django_hosts.middleware.HostsResponseMiddleware",
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('RDS_DB_NAME'),
        'USER': os.environ.get('RDS_USERNAME'),
        'PASSWORD': os.environ.get('RDS_PASSWORD'),
        'HOST': os.environ.get('RDS_HOSTNAME'),
        'PORT': os.environ.get('RDS_PORT'),
        }
}


ROOT_HOSTCONF = "ioniqbox.hosts"
ROOT_URLCONF = "ioniqbox.urls"
DEFAULT_HOST = "app"

CURRENT_SITE = os.environ.get("CURRENT_SITE")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.normpath(os.path.join(BASE_DIR, "templates")),
        ],
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

WSGI_APPLICATION = "ioniqbox.wsgi.application"

# USER MODEL
AUTH_USER_MODEL = "users.CustomUser"  # Reference to the custom user model

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # "EXCEPTION_HANDLER": "rollbar.contrib.django_rest_framework.post_exception_handler",
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 8,
}


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "apps"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "static/images/")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# IOT POSTGRES
IOT_DB_NAME = os.environ.get("IOT_POSTGRES_DB")
IOT_DB_USER = os.environ.get("IOT_POSTGRES_USERNAME")
IOT_DB_PASSWORD = os.environ.get("IOT_POSTGRES_PASSWORD")
IOT_DB_HOST = os.environ.get("IOT_POSTGRES_HOST")


# THERMOSTAT SECRET
THERMOSTAT_TOKEN = os.environ.get("THERMOSTAT_TOKEN")
SERVICE_TOKEN = os.environ.get("SERVICE_TOKEN")
DEVICE_ONLINE_STATUS_DELTA_SEC = 10

# REDIS STREAM SETTINGS
REDIS_STREAM_MAX_LEN = 21600


Q_CLUSTER = {
    'name': 'IoniqboxAsyncQueue',
    'timeout': 90,
    'retry': 120,
    'django_redis': 'queue',
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smpt.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# ADD DEFAULT EMAIL
DEFAULT_FROM_EMAIL = "alert@ioniqbox.com"
DEFAULT_ADMIN_EMAIL = "admin@twinkle.nyc"


CORS_ORIGIN_ALLOW_ALL = True

