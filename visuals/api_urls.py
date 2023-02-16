from django.urls import path
from .api import (
    FetchHeatingCyclesAndWeatherDataApiView,
)


urlpatterns = [ 
    path('heatcycles/', FetchHeatingCyclesAndWeatherDataApiView.as_view()),
]
