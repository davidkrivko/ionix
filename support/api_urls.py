from django.urls import path
from .api import ListCreateSupportRequest




urlpatterns = [
    path('', ListCreateSupportRequest.as_view()),
]
