import logging
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from django.contrib.auth import get_user_model
from .exceptions import (
    NoAuthToken,
    InvalidAuthToken,
)

User = get_user_model()


class ServiceTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()

        if id_token != settings.SERVICE_TOKEN:
            raise InvalidAuthToken()
        try:
            user = User.objects.get(username="service@turnonheat.com")
        except:
            user = None

        return (user, None)
