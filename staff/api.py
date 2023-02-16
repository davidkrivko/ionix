from datetime import timezone
from django_q.tasks import async_task
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from devices.utils import (
    get_thermostat_data, 
    retrieve_status,
    fetch_ioniq_data,
    fetch_devicezone_status,
)
from devices.serializers import (
    ControllerModelSerializer,
    SmartThermostatModelSerializer,
)
from devices.models import (
    IoniqControllerModel,
    SmartThermostatModel,
    BoilerModel,
)
from django.utils import timezone
from django.db.models import F

now = timezone.now


class ControllersApiListView(ListAPIView):
    """Allow staff users to list all controllers
    (ioniq devices)
    """
    permission_classes = [IsAuthenticated]
    queryset = IoniqControllerModel.objects.all()
    serializer_class = ControllerModelSerializer


class SmartThermostatApiListView(ListAPIView):
    """Allow staff users to list all smart thermostats
    """
    permission_classes = [IsAuthenticated]
    queryset = SmartThermostatModel.objects.all()
    serializer_class = SmartThermostatModelSerializer