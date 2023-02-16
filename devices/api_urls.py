from django.urls import path
from .api import (
    # ThermostatDataBySerialNumber,
    # RetriveThermostatLastStatusApiView,
    # RetriveThermostatControllerStatusApiView,
    # GetLastSetpointApiView,
    # RetrieveIoniqDataApiView,
    # HeatSwitchStatusUpdateApiView,
    # AnalogueThermostatStatusUpdateApiView,
    # BoilerShutdownTempApiView,
    # BoilerListApiView,
    # RetrieveDeviceZoneStatusApiView,
    # BoilerDataApiView,
    # RetrieveBoilerEndswitchFromIoniqDataApiView,
    # FetchTroubleShootingDataApiView,
    # FetchTroubleShootingDataByBoilerApiView,
    # BoilerUpdateApiView,
    # RetriveIoniqLastStatusApiView,
    # RetriveHeatSwitchControllerStatusApiView,
    # RetriveAnalogueThermostatControllerStatusApiView,
    ThermostatDataApiView,
    ThermostatSetTemperatureApiView,
    OwnSmartThermostatsList,
    GetThermostatDataFromStream,
    GetControllerDataFromStream,
    ThermostatNameUpdateView,
)


urlpatterns = [
    # Dashboard v2.0 (2022)
    path("thermostat/set/", ThermostatSetTemperatureApiView.as_view()),
    path("thermostats/", ThermostatDataApiView.as_view()),
    path("thermostat/update/<str:thermostat_pk>/", ThermostatNameUpdateView.as_view()),
    path("v2/thermostats/", OwnSmartThermostatsList.as_view()),
    path("v2/thermostat/data/<str:serial>/", GetThermostatDataFromStream.as_view()),
    path("v2/controller/data/<str:serial>/", GetControllerDataFromStream.as_view()),
    # Legacy from (2021)
    # ioniq controllers
    # path("controller/data/", FetchTroubleShootingDataApiView.as_view()),
    # path("controller/status/", RetriveIoniqLastStatusApiView.as_view()),
    # # thermostat component
    # path("thermostat/status/", RetriveThermostatLastStatusApiView.as_view()),
    # path("thermostats/custom/", ThermostatDataBySerialNumber.as_view()),
    # path("thermostat/setpoint/", GetLastSetpointApiView.as_view()),
    # # heat switch
    # path("heatswitch/update/", HeatSwitchStatusUpdateApiView.as_view()),
    # path(
    #     "heatwswitch/controller/status/",
    #     RetriveHeatSwitchControllerStatusApiView.as_view(),
    # ),
    # path("athermostat/update/", AnalogueThermostatStatusUpdateApiView.as_view()),
    # path(
    #     "athermostat/controller/status/",
    #     RetriveAnalogueThermostatControllerStatusApiView.as_view(),
    # ),
    # # zone state
    # path("zonestatus/", RetrieveDeviceZoneStatusApiView.as_view()),
    # # ioniqdata
    # path("thermostat/iodata/", RetrieveIoniqDataApiView.as_view()),
    # path(
    #     "thermostat/controller/status/",
    #     RetriveThermostatControllerStatusApiView.as_view(),
    # ),
    # # boilers
    # path("boiler/setshuttemp/", BoilerShutdownTempApiView.as_view()),
    # path("boiler/status/<int:pk>/", BoilerDataApiView.as_view()),
    # path("boiler/all/", BoilerListApiView.as_view()),
    # path("boiler/<int:pk>/", BoilerUpdateApiView.as_view()),
    # path("boiler/iodata/", RetrieveBoilerEndswitchFromIoniqDataApiView.as_view()),
    # path(
    #     "boiler/troubleshoot/<int:pk>/",
    #     FetchTroubleShootingDataByBoilerApiView.as_view(),
    # ),
]
