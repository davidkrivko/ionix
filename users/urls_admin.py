from django.conf import settings
from django.urls import path
from django.contrib import admin


urlpatterns = [
    path('', admin.site.urls),
]
