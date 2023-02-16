from django.urls import path
from .api import (
    ControllersApiListView,
    SmartThermostatApiListView,
)


urlpatterns = [ 
    path('controllers/', ControllersApiListView.as_view()),
    path('smart-thermostats/', SmartThermostatApiListView.as_view()),
]
