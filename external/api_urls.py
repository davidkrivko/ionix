from django.urls import path
from external.api import (
    IoniqMiniStatusUpdateApiView,
    IoniqMinitStatusChangeApiView,
    SetRoomTempOnChange,
    SetDeviceOnlineStatus,
    IoniqMaxDataApiView,
    IoniqMaxSystemStatusApiView,
    IoniqMaxForceUpgradeApiView,
    ProcessRelayThermostatDataApiView,
    ProcessPairedMiniDataApiView,
    ProcessPairedThermostatDataApiView,
    ServiceThermostatDataRetrieveApiView,
    ServiceControllerDataRetrieveApiView,
)

urlpatterns = [
    # IoT endpoints
    path("api_room_temp_changes/", SetRoomTempOnChange.as_view()),
    path("api_device_online_status/", SetDeviceOnlineStatus.as_view()),
    path("api_ioniq_mini_status/", IoniqMiniStatusUpdateApiView.as_view()),
    path("api_ioniq_mini_temperature/", IoniqMinitStatusChangeApiView.as_view()),
    path("ioniqmax/data/", IoniqMaxDataApiView.as_view()),
    path("ioniqmax/system/", IoniqMaxSystemStatusApiView.as_view()),
    path("ioniqmax/upgrade/", IoniqMaxForceUpgradeApiView.as_view()),
    # Legacy endpoint
    path("paired/exchange/", ProcessRelayThermostatDataApiView.as_view()),
    # Improved
    path("paired/controller/", ProcessPairedMiniDataApiView.as_view()),
    path("paired/thermostat/", ProcessPairedThermostatDataApiView.as_view()),
    path("service/thermostat/<str:serial_num>/", ServiceThermostatDataRetrieveApiView.as_view()),
    path("service/controller/<str:serial_num>/", ServiceControllerDataRetrieveApiView.as_view()),
]
