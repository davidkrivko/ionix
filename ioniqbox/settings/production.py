import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = True if os.environ.get("DEBUG") == "True" else False

ALLOWED_HOSTS = [
    'turnonheat.com',
    'api.turnonheat.com',
    'app.turnonheat.com',
    'ioadmin.turnonheat.com',
    'panel.turnonheat.com',
    ]


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

# ROLLBAR = {
#     'access_token': ROLLBAR_API_KEY,
#     'environment': 'development' if DEBUG else 'production',
#     'root': BASE_DIR,
# }
# import rollbar
# rollbar.init(**ROLLBAR)


CORS_ALLOWED_ORIGINS = ['https://react-app-mauve-zeta.vercel.app']