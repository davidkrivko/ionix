# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
import os

SECRET_KEY = "django-insecure-uy&*rtru6(h$ly6!4=lop77$xiz**tcqohda#6rwcrk%&!dija"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Local development
ALLOWED_HOSTS = ["*"]


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_NAME = os.environ.get("REDIS_NAME")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

REDIS_LOCATION_STRING = f"rediss://{REDIS_NAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    "queue": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION_STRING + "/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
        }
    },
    "streams": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION_STRING + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 50},
        }
    },
}


# ASYNC BACKGROUND TASKS
Q_CLUSTER = {
    "name": "IoniqboxAsyncQueue",
    "workers": 4,
    "timeout": 90,
    "retry": 120,
    "django_redis": "queue",
}

# EMAIL BACKENDS
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "local@ioniqbox.com"

AUTH_PASSWORD_VALIDATORS = []


MEDIA_URL = "/media/"
