import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'api-staging.turnonheat.com',
    'ioadmin-staging.turnonheat.com',
    'panel-staging.turnonheat.com',
    '142.93.113.255',
]

CORS_ALLOWED_ORIGINS = ['https://app.turnonheat.com']

ROOT_URLCONF = "ioniqbox.urls"


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

REDIS_LOCATION_STRING = f"redis://{REDIS_HOST}:{REDIS_PORT}"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    "queue": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION_STRING + "/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "OPTIONS": {
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    },
    "streams": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION_STRING + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "OPTIONS": {
            "CONNECTION_POOL_KWARGS": {"max_connections": 50}
        }
    },   
}



#ASYNC BACKGROUND TASKS
Q_CLUSTER = {
    'name': 'IoniqboxAsyncQueue',
    'timeout': 90,
    'retry': 120,
    'django_redis': 'queue',
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.ioniqbox.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# ADD DEFAULT EMAIL
DEFAULT_FROM_EMAIL = "alert@ioniqbox.com"
DEFAULT_ADMIN_EMAIL = "admin@twinkle.nyc"

AUTH_PASSWORD_VALIDATORS = []

CORS_ALLOW_ALL_ORIGINS = True