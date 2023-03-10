from django.urls import path, include
from rest_framework import routers

from .api import (
    ScheduleChoicesListView,
    ###
    ScheduleSubscriberApiView,
    ScheduleSubscriberCreateApiView,
    ScheduleSubscriberDeleteApiView,
    ###
    TenantScheduleSubscriberApiView,
    TenantScheduleSubscriberCreateApiView,
    TenantScheduleSubscriberDeleteApiView,
    ###
    ScheduleSwitchSubscriberApiView,
    SchedulSwitcheSubscriberCreateApiView,
    ScheduleSwitchSubscriberDeleteApiView,
    ###
    ScheduleAnalogueSubscriberApiView,
    ScheduleAnalogueSubscriberCreateApiView,
    ScheduleAnalogueSubscriberDeleteApiView,
    ###
    ZoneSubscriberViewSet,
)


router = routers.DefaultRouter()
router.register("zones", ZoneSubscriberViewSet, basename="zones")


urlpatterns = [
    path('options/<int:weekday>/', ScheduleChoicesListView.as_view()),

    # owner thermostats scheduling
    path('thermostats/', ScheduleSubscriberApiView.as_view()),
    path('thermostats/create/', ScheduleSubscriberCreateApiView.as_view()),
    path('thermostats/delete/', ScheduleSubscriberDeleteApiView.as_view()),
    # tenant thermostat group
    path('tenant/thermostats/', TenantScheduleSubscriberApiView.as_view()),
    path('tenant/thermostats/create/', TenantScheduleSubscriberCreateApiView.as_view()),
    path('tenant/thermostats/delete/', TenantScheduleSubscriberDeleteApiView.as_view()),

    # heat switches CRUD
    path('switches/', ScheduleSwitchSubscriberApiView.as_view()),
    path('switches/create/', SchedulSwitcheSubscriberCreateApiView.as_view()),
    path('switches/delete/', ScheduleSwitchSubscriberDeleteApiView.as_view()),
    # analogue thermostats CRUD
    path('analogue-thermostats/', ScheduleAnalogueSubscriberApiView.as_view()),
    path('analogue-thermostats/create/', ScheduleAnalogueSubscriberCreateApiView.as_view()),
    path('analogue-thermostats/delete/', ScheduleAnalogueSubscriberDeleteApiView.as_view()),

    path('', include(router.urls))
]
