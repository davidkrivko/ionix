from django.urls import path
from .api import (
    ChangeRoomNameApiView,
    CheckLastTemperatureApiView,
    FetchUpdateRoomNameApiView,
    ChangeZoneNameApiView,
)


urlpatterns = [
    path('room/changename/', ChangeRoomNameApiView.as_view()),
    path('apartment/', FetchUpdateRoomNameApiView.as_view()),
    path('gettemp/', CheckLastTemperatureApiView.as_view()),
    path('zone/changename/', ChangeZoneNameApiView.as_view()),
]
