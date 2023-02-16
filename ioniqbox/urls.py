from django.urls import path, include
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('', include('users.urls')),
    path('api/', include('api.api_urls')),

    path('schema/', get_schema_view(
        title="Ioniqbox",
        description="Internal API's",
        version="1.0.0"
    ), name="openapi-schema"),
]