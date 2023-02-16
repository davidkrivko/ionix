import os

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .views import (
    login_view,
    logout_view,
    restricted_area_view,
    guest_token_validation,
    request_password_reset,
    validate_password_reset_token,
    save_new_password,
    thermostat_login_view,
    thermostat_control_view,
    thermostat_logout_view,
)

urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("app/", restricted_area_view, name="dashboard"),
    path("guest/<str:user_id>/<str:token>/", guest_token_validation, name="guest-page"),
    path(
        "tenant/validate/<str:user_id>/<str:token>/",
        guest_token_validation,
        name="tenant-validate",
    ),
    # reset pass flow
    path("reset/", request_password_reset, name="request-reset"),
    path(
        "validate/<str:user_id>/<str:token>/",
        validate_password_reset_token,
        name="reset-validate",
    ),
    path("newpassword/", save_new_password, name="new-password"),
    # SET OF API URLS FOR BUILT IN JS APPLICATIONS
    path("api/", include("api.api_urls")),
    # Simple user-case - thermostat page
    path("thermostat/", thermostat_login_view, name="thermostat-login"),
    path("thermostat/settings/", thermostat_control_view, name="thermostat-control"),
    path("thermostat/logout/", thermostat_logout_view, name="thermostat-logout"),
]


# SERVE MEDIA FILES ON LOCAL/DEV SERVER
if os.environ.get("ENV_NAME") is None:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
