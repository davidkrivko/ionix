import os
from pathlib import Path

import logging.config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'do.ionix-staging.com',
    'admin.ionix-staging.com',
    'do-api.ionix-staging.com',
]

CORS_ALLOWED_ORIGINS = ['https://panel.turnonheat.com']


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
        "LOCATION": REDIS_LOCATION_STRING + "/0",
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

AUTH_PASSWORD_VALIDATORS = []

CORS_ORIGIN_ALLOW_ALL = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/david/logging/file.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

logging.config.dictConfig(LOGGING)
