from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

DEBUG = settings.DEBUG

schema_view = get_schema_view(
   openapi.Info(
      title="Ioniqbox API",
      default_version='v1',
      description="Ioniqbox API Documentation",
      terms_of_service="https://turnonheat.com/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny, ] if DEBUG else [permissions.IsAuthenticated, ],
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('devices/', include('devices.api_urls')),
    path('users/', include('users.api_urls')),
    path('properties/', include('properties.api_urls')),
    path('staff/', include('staff.api_urls')),
    path('schedules/', include('schedules.api_urls')),
    path('support/', include('support.api_urls')),
    path('visuals/', include('visuals.api_urls')),
]
